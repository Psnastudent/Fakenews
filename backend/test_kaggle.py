import sys
sys.path.insert(0, '.')
from app.services.kaggle_classifier import predict_kaggle, load_kaggle_model

print('Training model on Kaggle dataset...')
model = load_kaggle_model()
if model:
    print('Model ready!')
    tests = [
        'NASA confirmed Earth will be dark for 6 days due to a rare solar storm event.',
        'The Federal Reserve raised interest rates by 25 basis points at its latest meeting.',
        'Scientists discover that vaccines cause autism according to hidden government documents.',
        'Apple reported record quarterly revenue of 90 billion dollars beating analyst expectations.',
    ]
    for t in tests:
        r = predict_kaggle(t)
        verdict = r['verdict'].upper()
        conf = r['confidence']
        print(f"  [{verdict:8}] conf={conf:.2%}  {t[:75]}")
else:
    print('Model training failed')
