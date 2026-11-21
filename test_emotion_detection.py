"""Unit tests for the Watson emotion detector and Flask interface."""
import unittest
from unittest.mock import Mock, patch

from EmotionDetection.emotion_detection import emotion_detector
from server import app


class TestEmotionDetector(unittest.TestCase):
    """Check emotion scores and error handling."""

    def setUp(self):
        self.client = app.test_client()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_each_dominant_emotion(self, post):
        cases = {
            "anger": {"anger": 0.8, "disgust": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.0},
            "disgust": {"anger": 0.0, "disgust": 0.8, "fear": 0.0, "joy": 0.0, "sadness": 0.0},
            "fear": {"anger": 0.0, "disgust": 0.0, "fear": 0.8, "joy": 0.0, "sadness": 0.0},
            "joy": {"anger": 0.0, "disgust": 0.0, "fear": 0.0, "joy": 0.8, "sadness": 0.0},
            "sadness": {"anger": 0.0, "disgust": 0.0, "fear": 0.0, "joy": 0.0, "sadness": 0.8},
        }
        for dominant, emotions in cases.items():
            with self.subTest(dominant=dominant):
                post.return_value = Mock(
                    status_code=200,
                    json=lambda emotions=emotions: {
                        "emotionPredictions": [{"emotion": emotions}]
                    },
                )
                result = emotion_detector("Example text")
                self.assertEqual(result["dominant_emotion"], dominant)
                self.assertEqual(result[dominant], 0.8)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_http_400(self, post):
        post.return_value = Mock(status_code=400)
        self.assertIsNone(emotion_detector("invalid")["dominant_emotion"])

    def test_empty_text(self):
        self.assertIsNone(emotion_detector(" ")["dominant_emotion"])

    def test_blank_get_returns_error_message(self):
        response = self.client.get("/emotionDetector", query_string={"textToAnalyze": "  "})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Invalid text! Please try again!", response.data)

    def test_home_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Emotion Detector", response.data)


if __name__ == "__main__":
    unittest.main()
