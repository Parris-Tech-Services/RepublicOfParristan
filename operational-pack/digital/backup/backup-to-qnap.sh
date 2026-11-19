#!/usr/bin/env bash
# Nightly backup of the Docker Nextcloud (Option B) to the QNAP.
# Assumes the QNAP share is mounted at /mnt/qnap-backup (e.g. via /etc/fstab, CIFS).
# Cron (2am nightly):  0 2 * * * /opt/parristan/backup-to-qnap.sh >> /var/log/parristan-backup.log 2>&1
# If using UCS App Center instead, back up the whole UCS VM with your hypervisor's snapshot/export tool.
set -euo pipefail

COMPOSE_DIR="/opt/parristan/digital/nextcloud"
DEST="/mnt/qnap-backup/parristan/$(date +%F)"
KEEP_DAYS=14

mountpoint -q /mnt/qnap-backup || { echo "QNAP not mounted, aborting."; exit 1; }
mkdir -p "$DEST"
cd "$COMPOSE_DIR"
set -a; source .env; set +a

echo "$(date) maintenance on"
docker compose exec -T -u www-data app php occ maintenance:mode --on

trap 'docker compose exec -T -u www-data app php occ maintenance:mode --off' EXIT

echo "$(date) dumping database"
docker compose exec -T db mariadb-dump -unextcloud -p"$DB_PASSWORD" --single-transaction nextcloud | gzip > "$DEST/nextcloud-db.sql.gz"

echo "$(date) copying files"
docker run --rm -v nextcloud_nextcloud:/src:ro -v "$DEST":/dst alpine \
  tar czf /dst/nextcloud-files.tar.gz -C /src .

find /mnt/qnap-backup/parristan -mindepth 1 -maxdepth 1 -type d -mtime +"$KEEP_DAYS" -exec rm -rf {} +
echo "$(date) backup complete: $DEST"
