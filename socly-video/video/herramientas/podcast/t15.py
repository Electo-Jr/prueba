import json, subprocess, numpy as np
from faster_whisper import WhisperModel
FF = "/usr/bin/ffmpeg"
SRC = "/home/user/prueba/socly-video/trabajo/podcast/IMG_7540.MOV"
a, b = 14, 58
raw = subprocess.run([FF, "-loglevel", "error", "-ss", str(a), "-to", str(b), "-i", SRC, "-vn", "-ac", "1", "-ar", "16000", "-af", "volume=3,highpass=f=80", "-f", "f32le", "-"], capture_output=True, check=True).stdout
audio = np.clip(np.frombuffer(raw, dtype=np.float32), -1, 1)
m = WhisperModel("medium", device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio, language="es", word_timestamps=True, vad_filter=False, condition_on_previous_text=False, temperature=0.0, no_speech_threshold=0.9)
w = [{"w": x.word.strip(), "s": round(x.start + a, 2), "e": round(x.end + a, 2)} for s in segs for x in (s.words or [])]
json.dump(w, open("../../podcast/medium/clip15.json", "w", encoding="utf-8"), ensure_ascii=False)
print(' '.join(f"{x['w']}@{x['s']}" for x in w))
