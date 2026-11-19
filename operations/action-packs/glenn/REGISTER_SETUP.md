# Glenn — set up the register (about 15 minutes)

Do this on **your own computer**, after the consent replies arrive. Nothing here goes into GitHub or chat.

## 1. Make a private, encrypted folder
- **Windows:** create a VeraCrypt volume (veracrypt.fr), or turn on BitLocker for the drive, and make a folder inside, e.g. `P:\parristan-register\`.
- **Linux:** a folder in your encrypted home, e.g. `~/parristan-register/`, or a VeraCrypt volume.

## 2. Write the consents file
In that private folder, create `founders.csv` in a text editor. Use the names exactly as each founder confirmed, in founding order, with the dates they gave:

```text
name,consent_date
Joshua Parris,2026-11-19
Glenn Peterson,2026-11-19
Matthew John Lucas Walker,2026-11-19
Fred Carbunkle,2026-11-19
Jane Carbunkle,2026-11-19
```

Only include people whose written consent reply you have. You can run the import again later for the rest; it skips anyone already registered.

## 3. Run three commands
From the repository folder (Windows: use `py -3` instead of `python3`):

```bash
python3 tools/parristan_registry.py --db ~/parristan-register/members.sqlite3 init
python3 tools/parristan_registry.py --db ~/parristan-register/members.sqlite3 import --csv ~/parristan-register/founders.csv
python3 tools/parristan_registry.py --db ~/parristan-register/members.sqlite3 report
```

Expected output of the import:

```text
P-0001  Joshua Parris              added
P-0002  Glenn Peterson             added
P-0003  Matthew John Lucas Walker  added
P-0004  Fred Carbunkle             added
P-0005  Jane Carbunkle             added
```

The tool refuses to put the database or read the CSV inside the repository, as a safety catch.

## 4. Back up
- Copy `members.sqlite3` into the encrypted monthly backup (see [../../BACKUP_AND_HANDOVER.md](../../BACKUP_AND_HANDOVER.md)).
- Give the backup password to one other officer (suggested: Jane, as Secretary) privately, so the register survives if your computer dies.

## 5. Report back
Send Josh (or the assistant) **only** the `report` line, e.g. `{'total': 5, 'active': 5, ...}`, and the date. That gets recorded publicly as "5 founding members registered", which ticks checklist items 12 and 13.
