#!/usr/bin/env bash
set -euo pipefail
set -x  # verbose logs

echo "==> Node/npn versions"
node -v
npm -v

echo "==> CI install"
npm ci

echo "==> List files"
ls -la

echo "==> Print tsconfig.json"
cat tsconfig.json || true

echo "==> Build (no TypeScript 'tsc -b', let Vite handle it)"
# If you want strict typechecking, we can add vite-plugin-checker later.
npx vite build --debug
