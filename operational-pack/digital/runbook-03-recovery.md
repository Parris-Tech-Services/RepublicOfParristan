# Runbook 03: Recovery

Test this once, then once a year (suggested: Audit Day).

## UCS (Option A)
1. Restore the latest UCS VM export or snapshot in the hypervisor.
2. Boot, log in to the portal, and confirm users and Nextcloud open.

## Docker Nextcloud (Option B)
```bash
cd /opt/parristan/digital/nextcloud
docker compose down
docker volume rm nextcloud_nextcloud nextcloud_db
docker compose up -d db && sleep 20
B=/mnt/qnap-backup/parristan/<YYYY-MM-DD>
gunzip -c $B/nextcloud-db.sql.gz | docker compose exec -T db mariadb -unextcloud -p"$DB_PASSWORD" nextcloud
docker run --rm -v nextcloud_nextcloud:/dst -v $B:/src:ro alpine tar xzf /src/nextcloud-files.tar.gz -C /dst
docker compose up -d
docker compose exec -u www-data app php occ maintenance:mode --off
```

## ParriBuntu laptop
Reinstall Ubuntu, rerun `build-parribuntu.sh`, re-enrol in MeshCentral. Files come back from Nextcloud.

## Done when
- [ ] A test file deleted before restore is back after restore
