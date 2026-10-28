#!/usr/bin/env bash
# One-time setup for a fresh session: Python deps + Kokoro voice model (Apache-2.0, GitHub release).
set -e
pip install -q --break-system-packages kokoro-onnx soundfile numpy pillow requests 2>/dev/null || pip install -q kokoro-onnx soundfile numpy pillow requests
CACHE="${R2R_CACHE:-$HOME/.cache/rich2ruin}"
mkdir -p "$CACHE"
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s "$CACHE/kokoro-v1.0.onnx" ] || curl -sSL -o "$CACHE/kokoro-v1.0.onnx" $REL/kokoro-v1.0.onnx
[ -s "$CACHE/voices-v1.0.bin" ] || curl -sSL -o "$CACHE/voices-v1.0.bin" $REL/voices-v1.0.bin
which ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
echo "setup ok"
