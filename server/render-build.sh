#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Python deps"
pip install --no-cache-dir -r requirements.txt

# Choose a writable dir for NLTK data inside the repo (or Render’s project dir)
export NLTK_DATA="$PWD/.nltk_data"
mkdir -p "$NLTK_DATA"

echo "==> Downloading NLTK resources into $NLTK_DATA"
python - <<'PY'
import os, nltk
dl = os.environ.get("NLTK_DATA")
assert dl, "NLTK_DATA not set"
nltk.download('punkt', download_dir=dl)
nltk.download('stopwords', download_dir=dl)
print("NLTK data downloaded to:", dl)
PY
