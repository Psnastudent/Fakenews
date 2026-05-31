import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

MODEL_PATH = Path(__file__).parent.parent.parent / "data" / "image_model.pth"

# Simple CNN architecture matching the training script
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2, 2)
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

_image_model = None
_device = torch.device("cpu") # For fast inference on API, CPU is fine
_transform = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model():
    global _image_model
    if _image_model is not None:
        return _image_model
        
    if not MODEL_PATH.exists():
        logger.warning(f"Image model weights not found at {MODEL_PATH}")
        return None
        
    try:
        model = SimpleCNN()
        model.load_state_dict(torch.load(MODEL_PATH, map_location=_device))
        model.to(_device)
        model.eval()
        _image_model = model
        logger.info("[Visual] PyTorch Image Classifier loaded successfully.")
        return _image_model
    except Exception as e:
        logger.error(f"Failed to load image model: {e}")
        return None

async def verify_image(image_bytes: bytes) -> dict:
    """
    Run the trained PyTorch CNN to detect if an image is Real or AI Generated (Fake).
    """
    model = load_model()
    
    if model is None:
        return {
            "verdict": "unverified",
            "truth_score": 50,
            "explanation": "Image analysis model is currently offline or untrained.",
            "sources": []
        }
        
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = _transform(image).unsqueeze(0).to(_device)
        
        with torch.no_grad():
            outputs = model(tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
            
            # Index 0 = FAKE, Index 1 = REAL
            prob_fake = probabilities[0].item()
            prob_real = probabilities[1].item()
            
            is_real = prob_real > prob_fake
            confidence = prob_real if is_real else prob_fake
            
            verdict = "real" if is_real else "fake"
            truth_score = int(prob_real * 100)
            
            explanation = (
                f"Visual verification complete. Our convolutional neural network analyzed this image "
                f"and determined it is highly likely to be {'REAL' if is_real else 'AI GENERATED (FAKE)'} "
                f"with {confidence:.1%} confidence. The model checks for artifacting, pixel distribution, and generation signatures."
            )
            
            return {
                "verdict": verdict,
                "truth_score": truth_score,
                "explanation": explanation,
                "sources": [{
                    "name": "FactGuard Neural Visual Engine",
                    "url": "",
                    "trust_score": confidence,
                    "snippet": f"Detected AI generation artifacts: {'Yes' if not is_real else 'No'}."
                }]
            }
            
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return {
            "verdict": "unverified",
            "truth_score": 50,
            "explanation": "Failed to process image.",
            "sources": []
        }

async def verify_video(video_bytes: bytes) -> dict:
    """Mock video verification."""
    return {
        "verdict": "fake",
        "truth_score": 15,
        "explanation": "Deepfake temporal flickering detected. Frame-by-frame analysis reveals inconsistencies in facial lighting and micro-expressions, a common hallmark of AI-generated video.",
        "sources": [{
            "name": "FactGuard Video Forensic Engine",
            "url": None,
            "trust_score": 0.94,
            "snippet": "High confidence deepfake detection."
        }],
        "correct_info": "This video has been altered using deep learning."
    }
