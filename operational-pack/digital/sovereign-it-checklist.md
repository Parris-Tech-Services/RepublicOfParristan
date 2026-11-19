# Parristan Sovereign IT Checklist

Modelled on the French Gendarmerie (GendBuntu: Ubuntu, LibreOffice, Firefox, Thunderbird, central desktop lifecycle management) and Schleswig-Holstein (LibreOffice, Linux, Nextcloud, Open-Xchange/Thunderbird, Univention directory, OpenTalk, open telephony, an Open Source Program Office).

Note: GendBuntu itself is not publicly distributed, so ParriBuntu copies the approach on stock Ubuntu LTS.

## Phase 0: Governance
- [ ] Pass the Open Source Act (`government/open-source-act.md`)
- [ ] Appoint Chief Digital Officer (Office of Sovereign Systems)
- [ ] Confirm host: The Shed / ForgeGrid coordinator

## Phase 1: Identity (`runbook-01-identity-ucs.md`)
- [ ] UCS installed as the national directory
- [ ] One account per citizen
- [ ] Groups: Founders, Ministers, Junior-Citizens, Constabulary

## Phase 2: Communications
- [ ] Domain registered for national addresses
- [ ] Mail server (UCS mail app or Mailcow)
- [ ] Thunderbird on every national machine
- [ ] Video: Jitsi (simple) or OpenTalk

## Phase 3: Collaboration (`runbook-02-nextcloud.md`)
- [ ] Nextcloud running, logins via UCS
- [ ] Collabora Online for shared editing
- [ ] Founding documents stored as ODF

## Phase 4: National desktop (`parribuntu/`)
- [ ] ParriBuntu built on Ubuntu 24.04 LTS
- [ ] Branding applied (flag wallpaper)
- [ ] Deployed to national laptops
- [ ] Managed via MeshCentral / Action1
- [ ] Junior citizen profiles with parental controls

## Phase 5: State services
- [ ] Treasury Parri ledger (`.ods` in Nextcloud)
- [ ] Citizen portal (Gazette + online citizenship form)
- [ ] Optional: FreePBX internal phones

## Phase 6: Security and continuity (`backup/`)
- [ ] Nightly backup to QNAP
- [ ] Full-disk encryption on national laptops
- [ ] Recovery runbook tested once
