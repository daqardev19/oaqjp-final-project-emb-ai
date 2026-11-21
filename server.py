"""Flask web interface for the emotion detector."""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the application form."""
    return render_template("index.html")


@app.post("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return a readable result."""
    text_to_analyze = request.form.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400
    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return "The text could not be analyzed. Please try different text.", 400
    emotion_names = ("anger", "disgust", "fear", "joy", "sadness")
    formatted = ", ".join(
        f"{emotion}: {result[emotion]}" for emotion in emotion_names
    )
    dominant = result["dominant_emotion"]
    return (
        f"For the given statement, the system response is {formatted}. "
        f"The dominant emotion is {dominant}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
