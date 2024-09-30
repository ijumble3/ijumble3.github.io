# transcribe.py
import sys
import json
from vosk import Model, KaldiRecognizer
import wave

def transcribe(audio_path):
    model = Model("model")  # Path to your Vosk model /home/ubuntu/.local/lib/python3.10/site-packages
    wf = wave.open(audio_path, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit(1)

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            results.append(res)
    res = json.loads(rec.FinalResult())
    results.append(res)

    # Combine results
    transcript = " ".join([res.get('text', '') for res in results])
    print(transcript)

if __name__ == "__main__":
    audio_file = sys.argv[1]
    transcribe(audio_file)
