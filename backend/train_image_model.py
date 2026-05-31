import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TrainImageModel")

# Paths
DATA_DIR = Path(r"D:\miniproject\train")
MODEL_SAVE_PATH = Path(r"D:\miniproject\backend\data\image_model.pth")
BATCH_SIZE = 128
EPOCHS = 5 # Small number of epochs for speed, typically enough for 100k simple CNN
LR = 0.001

class CIFakeDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        fake_dir = root_dir / "FAKE"
        real_dir = root_dir / "REAL"
        
        fake_files = []
        real_files = []
        if fake_dir.exists():
            fake_files = [f for f in os.listdir(fake_dir) if f.endswith(('.jpg', '.jpeg', '.png'))][:2000] # Use subset
            for f in fake_files:
                self.image_paths.append(fake_dir / f)
                self.labels.append(0) # 0 = FAKE
                
        if real_dir.exists():
            real_files = [f for f in os.listdir(real_dir) if f.endswith(('.jpg', '.jpeg', '.png'))][:2000] # Use subset
            for f in real_files:
                self.image_paths.append(real_dir / f)
                self.labels.append(1) # 1 = REAL
                    
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        # Input: 3x32x32
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # 32x16x16
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2), # 64x8x8
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)  # 128x4x4
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 4 * 4, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 2)
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

def main():
    logger.info("Initializing dataset...")
    
    transform = transforms.Compose([
        transforms.Resize((32, 32)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dataset = CIFakeDataset(DATA_DIR, transform=transform)
    if len(dataset) == 0:
        logger.error(f"No images found in {DATA_DIR}. Aborting training.")
        return
        
    logger.info(f"Loaded {len(dataset)} images.")
    
    # Split into train/val (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
    
    # We will use pin_memory and num_workers for speed if possible
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    model = SimpleCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    logger.info("Starting training...")
    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            if i % 100 == 99:
                logger.info(f"Epoch {epoch+1}/{EPOCHS}, Batch {i+1}/{len(train_loader)}, Loss: {running_loss/100:.4f}")
                running_loss = 0.0
                
        # Validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                
        acc = 100 * correct / total
        logger.info(f"Epoch {epoch+1}/{EPOCHS} Validation Accuracy: {acc:.2f}%")
        
    # Save model
    MODEL_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    logger.info(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == "__main__":
    main()
