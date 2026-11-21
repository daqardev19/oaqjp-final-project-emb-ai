"""Watson NLP based emotion detection."""

import requests

URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"


def emotion_detector(text_to_analyze):
    """Return emotion scores and the dominant emotion for input text."""
    empty_result = {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return empty_result.copy()

    response = requests.post(
        URL,
        json={"raw_document": {"text": text_to_analyze}},
        headers={"grpc-metadata-mm-model-id": MODEL_ID},
        timeout=30,
    )
    if response.status_code == 400:
        return empty_result.copy()
    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    scores = {
        name: emotions[name]
        for name in ("anger", "disgust", "fear", "joy", "sadness")
    }
    scores["dominant_emotion"] = max(scores, key=scores.get)
    return scores
