# Runbook 02: National File Store and Calendar (Nextcloud + Collabora)

## Option A (recommended): install via UCS App Center
1. UCS portal → **App Center** → search **Nextcloud** → Install.
2. App Center → search **Collabora Online** → Install.
3. UCS users are automatically able to log in to Nextcloud. Activate users per app under Users → (user) → Apps → Nextcloud.
4. Open Nextcloud from the UCS portal and log in as a founder.
5. Create the shared folders:
   - `Republic/Assembly` (minutes)
   - `Republic/Treasury` (Parri ledger; Treasurer + President only)
   - `Republic/Register` (citizen register; Founders only)
   - `Republic/Gazette`
6. Calendars: create `National Calendar` and add Founding Day (19 Nov), Harvest Fair, the Great LAN.

## Option B: standalone with Docker (if not using UCS apps)
Use `nextcloud/docker-compose.yml` in this folder:
```bash
cd digital/nextcloud
cp .env.example .env      # then edit every password in .env
docker compose up -d
```
Then open `http://<host-ip>:8080`. To use UCS logins, enable the **LDAP user and group backend** app in Nextcloud and point it at `ucs01` (port 7389 on UCS, base DN from UCS → Domain → LDAP directory).

For Collabora: in Nextcloud, install **Nextcloud Office**, set the server URL to `http://<host-ip>:9980`.

## Done when
- [ ] Each founder can log in to Nextcloud with their UCS account
- [ ] Shared folders exist with correct permissions
- [ ] A `.odt` opens and edits in the browser
- [ ] National Calendar shared with all citizens
