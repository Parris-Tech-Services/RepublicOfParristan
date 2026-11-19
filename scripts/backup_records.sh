#!/usr/bin/env bash
# Make dated git bundles of Parristan repositories with checksums.
# Usage: scripts/backup_records.sh DEST_DIR REPO_URL [REPO_URL...]
# Encrypt DEST_DIR afterwards. Never write backups inside a repository.
set -euo pipefail
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 DEST_DIR REPO_URL [REPO_URL...]" >&2; exit 2
fi
dest=$1; shift
mkdir -p "$dest"
dest=$(cd "$dest" && pwd)
stamp=$(date +%Y-%m-%d)
work=$(mktemp -d); trap 'rm -rf "$work"' EXIT
for url in "$@"; do
  name=$(basename "$url" .git | tr '[:upper:]' '[:lower:]')
  git clone --quiet --mirror "$url" "$work/$name.git"
  out="$dest/$name-$stamp.bundle"
  git -C "$work/$name.git" bundle create "$out" --all >/dev/null 2>&1
  git bundle verify "$out" >/dev/null 2>&1
  echo "Wrote $out"
done
( cd "$dest" && sha256sum ./*-"$stamp".bundle > "checksums-$stamp.sha256" )
echo "Checksums: $dest/checksums-$stamp.sha256"
echo "Next: encrypt $dest and store two copies (see operations/BACKUP_AND_HANDOVER.md)."
