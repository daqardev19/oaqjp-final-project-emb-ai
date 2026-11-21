"""Flask web interface for the emotion detector."""
# Static analysis: run `pylint server.py EmotionDetection` from the project root.
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/")
def home():
    """Render the application form."""
    return render_template("index.html")


@app.get("/emotionDetector")
# The route name follows the assignment's camelCase endpoint convention.
# pylint: disable=invalid-name
def emotionDetector():
    """Analyze submitted text and return a readable result."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    result = emotion_detector(text_to_analyze)
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
