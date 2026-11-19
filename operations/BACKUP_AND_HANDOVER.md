# Records backup and handover procedure

**Why:** the Enterprise trial will expire, and GitHub alone is a single point of failure. Checklist item 35.

## What to back up
| Record | Where it lives | Backup method |
|---|---|---|
| Public repository (all history) | GitHub | `scripts/backup_records.sh` (git bundle) |
| Private Enterprise drafting repository | GitHub | same script, second URL |
| Membership register (`.sqlite3`) | Registrar's authorised device only | Encrypted copy by the Registrar — never to GitHub |
| Matrix room decisions and votes | Matrix | Secretary exports key decisions into minutes monthly |
| Signed minutes, ballots | Secretary | Scanned PDF in the private backup set |

## Routine (monthly, and before the Enterprise trial ends)
1. Run on a trusted computer: `scripts/backup_records.sh ~/parristan-backups https://github.com/Parris-Tech-Services/RepublicOfParristan.git [private repo URL]`
2. The script makes a dated `.bundle` per repository and a SHA-256 checksum file.
3. Encrypt the backup folder (for example `gpg -c` or a VeraCrypt volume) and keep **two copies**: one at home (e.g. the QNAP), one off-site (USB drive with a second founder).
4. Record date, operator and checksum in the decision register (not the files themselves).

## Restore test (at least once; required before calling this done)
1. A **second person** takes the encrypted copy and decrypts it.
2. `git clone parristan-public-YYYY-MM-DD.bundle restored` — check the latest commit matches GitHub.
3. Record: date, who restored, result.

## Handover when an official changes
1. Outgoing official lists every account, file and key they hold.
2. Incoming official is given access and confirms it works.
3. Outgoing access is removed; the Secretary records it in the decision register.

## Enterprise trial expiry checklist
- [ ] Final bundle of the private repository taken and restore-tested.
- [ ] Decide where the private drafts go next (free private repo, Nextcloud, or merged into public after review).
- [ ] Confirm nothing personal goes public during any move.
