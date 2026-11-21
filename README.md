# Final project

## Emotion Detector

A Flask application that analyzes English text with the Watson NLP EmotionPredict service and returns anger, disgust, fear, joy, sadness, and the dominant emotion.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python server.py
```
Open http://127.0.0.1:5000 and submit a sentence. The Watson NLP course endpoint must be reachable for live predictions.

## Tests and static analysis

```powershell
python -m unittest -v
pylint server.py EmotionDetection
```

## Package use

```python
from EmotionDetection import emotion_detector
print(emotion_detector("I am excited about this project"))
```

Expected keys: `anger`, `disgust`, `fear`, `joy`, `sadness`, and `dominant_emotion`. A 400 response or blank input is handled without attempting to select a dominant emotion.
