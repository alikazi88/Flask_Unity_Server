from flask import Flask, request, jsonify
import vosk
import json

app = Flask(__name__)

# Path to the Vosk model directory
model_path = "vosk-model-small-en-us-0.15"

# Initialize the Vosk model
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    audio_data = request.data
    try:
        # Recognize speech from audio data
        recognizer.AcceptWaveform(audio_data)
        result = recognizer.Result()
        result_dict = json.loads(result)
        transcription = result_dict.get("text", "")
        return jsonify({"transcription": transcription})
    except Exception as e:
        print(f"Recognition error: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
