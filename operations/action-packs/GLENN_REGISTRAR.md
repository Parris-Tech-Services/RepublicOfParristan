# Glenn Peterson — Registrar pack (membership register)

**Goal:** a private register on your own device, with the five founders recorded from written consent and numbered P-0001 to P-0005 (Gazette 2026-008 says numbers 1–5 go to founders). Nothing from the register ever goes into GitHub.

## Step 1 — Approve the policy
Read [../drafts/MEMBERSHIP_POLICY.md](../drafts/MEMBERSHIP_POLICY.md). Change anything you disagree with, then put a motion in the Matrix room:

> **Motion:** That the Assembly adopts the Membership Policy and Privacy Notice as drafted in operations/drafts/MEMBERSHIP_POLICY.md [with these changes: …]. Voting closes in 48 hours.

## Step 2 — Ask each founder for written consent
Send from `registrar@parristan.org` to each founder **individually** (not to assembly@):

> **Subject: Your founding membership — please confirm**
>
> Hi [name],
>
> As Registrar I'm setting up the private membership register. Please reply to confirm:
>
> 1. The name you want on the register: ______
> 2. "I consent to being recorded as a founding member of the Republic of Parristan, and I have read the privacy notice." (attached / linked)
> 3. The date you agreed to found Parristan (if unsure, 19 November 2026).
>
> The register only holds your name, consent date, member number and status. It's kept on my device, encrypted, and never published. You can ask to see, correct or remove your record at any time.
>
> Thanks,
> Glenn Peterson, Registrar

Keep each reply email in the `registrar@` mailbox — that's your evidence.

## Step 3 — Set up the register on your computer
Needs Python 3. Pick a folder **outside** the repository, ideally inside an encrypted drive or a VeraCrypt volume.

```bash
python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 init
```

For each founder, **in the order the consents arrive or in agreed founding order**:

```bash
python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 add --name "Full Name" --consent-date 2026-11-19
python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 number --id <the Member ID it printed>
```

Check:

```bash
python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 list
python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 report
```

## Step 4 — Back up and give Matthew the roll
- Copy the `.sqlite3` file into the encrypted backup (see [../BACKUP_AND_HANDOVER.md](../BACKUP_AND_HANDOVER.md)).
- For the election, export the roll and email it to `returningofficer@` only:
  ```bash
  python3 tools/parristan_registry.py --db /path/to/private/members.sqlite3 roll --as-of 2026-11-20
  ```

## Tell the records
Only the **report** output (counts, no names) and the date go into the public record. Reply "register set up, 5 founders numbered on <date>" and checklist items 12–13 will be updated.
