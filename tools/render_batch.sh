#!/usr/bin/env bash
# render several specs one process each (frees ffmpeg readers between reels)
export R2R_CACHE=${R2R_CACHE:-$HOME/.cache/rich2ruin}
for r in "$@"; do
  rm -rf "build/$r/scenes"
  python3 engine/engine.py "specs/$r.json" render 2>&1 | grep -- "->" || echo "FAILED $r"
done
echo BATCH_DONE
