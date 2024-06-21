import pyaudio
import json
import vosk
import sys

# Path to the Vosk model
model_path = "vosk-model-small-en-us-0.15"

# Load the Vosk model
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for live audio input
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8000)

stream.start_stream()

print("Listening...")

try:
    while True:
        data = stream.read(8000, exception_on_overflow=False)
        print(f"Received audio data: {len(data)} bytes")

        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            print("Transcription:", result_dict.get("text", ""))
        else:
            partial_result = recognizer.PartialResult()
            partial_result_dict = json.loads(partial_result)
            print("Partial transcription:", partial_result_dict.get("partial", ""))
except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Terminating...")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
