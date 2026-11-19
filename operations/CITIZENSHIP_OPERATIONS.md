# Citizenship and Registrar Operations

**Status:** Draft operational system and a tested offline register are supplied. An appointed registrar, approved membership policy and real citizens' entries are not yet recorded as operational.

## What membership means

Citizenship means voluntary membership in Parristan's micronational association; it **does not** confer Australian or foreign legal nationality, passports for travel, immigration status or tax immunity.

## Five founding members

The organiser reports that Joshua Parris, Glenn Peterson, Matthew John Lucas Walker, Fred Carbunkle and Jane Carbunkle have agreed to found Parristan. Their names are already in the [founder record](../docs/FOUNDERS.md). Do not assume a private membership database exists or assign membership numbers until a registrar records consent dates using an authorised device.

## Actual administrative steps

1. Approve the eligibility rules, consent wording, registrar role, minimum record fields, access permissions, withdrawal/deletion rules and appeals pathway.
2. Choose a **local, protected storage location outside any Git repository**. The provided program refuses to put its SQLite database inside this repository. Use OS-level disk encryption and restricted account access where available; SQLite itself is not encrypted.
3. Initialise the local file with the tool below; the command does **not** enrol anyone automatically.
4. For each genuine consent, register chosen/public name and real consent date. For larger populations add a separate protected contact/verification method under the adopted privacy procedure; don't rely on name equality to establish identity.
5. Before an election, use a verified human-maintained eligibility list and deduplicate people (not GitHub handles). Keep votes secret and publish only turnout totals.
6. Run periodic aggregate membership summaries, maintain withdrawal procedures and back up the private database in appropriately protected storage.

## Runnable commands

Requires Python 3.11+ and no third-party packages. These are **examples only**; use an absolute path outside the checkout, and ensure the directory is protected.

```bash
python tools/parristan_registry.py --db /secure/private/parristan.sqlite3 init
python tools/parristan_registry.py --db /secure/private/parristan.sqlite3 add --name "Sample Member" --consent-date 2026-11-19
python tools/parristan_registry.py --db /secure/private/parristan.sqlite3 summary
python tools/parristan_registry.py --db /secure/private/parristan.sqlite3 list
python tools/parristan_registry.py --db /secure/private/parristan.sqlite3 remove --id <member-uuid>
```

The example name is fictional and **must not** be interpreted as an actual recorded citizen. A command-line argument containing a member name may enter shell history; administrators may prefer a locally restricted terminal. The program's generated membership IDs are internal association identifiers, **not government-issued legal identity numbers**.

## Suggested minimal private record

Member UUID, chosen/public name, date consent was actually recorded, registration timestamp and active status. Do not store home addresses, dates of birth, personal narratives or identity-document scans unless a specific, lawful necessity is established. Do not commit `*.sqlite3` or membership data.

## Applications and appeals

Publish a privacy notice before accepting applications; specify why fields are collected, who can access them, how to withdraw, how decisions are appealed and when records are deleted. Do not accept applications through a GitHub issue form or make a public spreadsheet of citizens.

**Done only when:** an authorised registrar and real privacy process exist, actual member records are entered with evidentiary consent, data storage is protected, and the enrollment/withdrawal workflow has been exercised on an authorised device.
