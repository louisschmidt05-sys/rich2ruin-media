"""Render narration lines with Chatterbox TTS (Resemble AI, MIT licence) on the GitHub runner.
voice_jobs.json: {"jobs": [{"id": "21_florida_v3", "lines": ["...", "..."], "exaggeration": 0.5, "cfg": 0.5}]}
Writes voices/<id>/<voice>/line_NN.wav (24 kHz mono). Skips jobs whose files already exist with the same text."""
import json, os, hashlib
import soundfile as sf
import torch
from chatterbox.tts import ChatterboxTTS

torch.manual_seed(7)
model = ChatterboxTTS.from_pretrained(device="cpu")
jobs = json.load(open("voice_jobs.json"))["jobs"]
for job in jobs:
    name = job.get("voice", "cb_default")
    out = os.path.join("voices", job["id"], name)
    os.makedirs(out, exist_ok=True)
    ref = job.get("ref")
    for i, text in enumerate(job["lines"]):
        h = hashlib.sha1(f'{text}|{job.get("exaggeration",0.5)}|{job.get("cfg",0.5)}|{ref}'.encode()).hexdigest()[:10]
        wav_p, tag_p = os.path.join(out, f"line_{i:02d}.wav"), os.path.join(out, f"line_{i:02d}.txt")
        if os.path.exists(wav_p) and os.path.exists(tag_p) and open(tag_p).read().strip() == h:
            continue
        kw = dict(exaggeration=job.get("exaggeration", 0.5), cfg_weight=job.get("cfg", 0.5))
        if ref:
            kw["audio_prompt_path"] = ref
        wav = model.generate(text, **kw)
        sf.write(wav_p, wav.squeeze(0).numpy(), model.sr)
        open(tag_p, "w").write(h)
        print(job["id"], i, round(wav.shape[-1] / model.sr, 2), "s", flush=True)
