#!/usr/bin/env bash
set -euo pipefail

echo "==> Python version"
python --version
pip --version || true

echo "==> Upgrade pip/setuptools/wheel"
pip install --upgrade pip setuptools wheel

echo "==> Installing Python deps (prefer wheels)"
# Force wheels for numpy / scikit-learn to avoid building from source
pip install --only-binary=:all: numpy==2.1.3 scikit-learn==1.5.2
pip install --no-cache-dir -r requirements.txt

# NLTK data into a local folder Render can read at runtime
export NLTK_DATA="$PWD/.nltk_data"
mkdir -p "$NLTK_DATA"
python - <<'PY'
import os, nltk
d = os.environ.get("NLTK_DATA")
assert d, "NLTK_DATA not set"
nltk.download('punkt', download_dir=d)
nltk.download('stopwords', download_dir=d)
print("NLTK data downloaded to:", d)
PY
