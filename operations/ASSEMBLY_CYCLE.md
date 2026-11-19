# Running an Assembly meeting, start to finish

**For:** the Secretary (Jane Carbunkle), or anyone acting as Secretary.
**Tool:** `tools/assembly_cycle.py` (Python 3, no installs). On Windows use `py -3` instead of `python3`.

One meeting goes through eight steps. The tool keeps a record in `assembly/meetings/<date>.json` and **won't let you skip a step**. For example, you can't record votes before quorum is confirmed, or publish minutes nobody has approved.

| # | Step | Command | Rule it checks |
|---|---|---|---|
| 1 | Schedule | `schedule` | Open actions from earlier meetings are carried forward automatically |
| 2 | Send notice | `notice`, then `record-notice` | Notice at least **24 hours** before the meeting (Gazette 2026-009) |
| 3 | Attendance | `attendance` | Quorum of **3**; an absent chair or Secretary needs a stand-in who is present |
| 4 | Motions | `motion` | Passes if YES > NO; abstentions don't count; at least 3 must vote; votes can't exceed people present |
| 5 | Notes and actions | `note`, `action` | Action owners must be Assembly members |
| 6 | Close | `close` | Produces the draft minutes |
| 7 | Approve minutes | `approve-minutes` | A later meeting or written vote; must carry |
| 8 | Publish | `publish` | Writes the Gazette notice, web page, decision register, data export, decisions and administration pages and the actions page together |

## Worked example: first monthly meeting

```bash
# 1. Schedule (Sydney time)
python3 tools/assembly_cycle.py schedule --at "2026-12-08 19:30" --place "by video call"

# Optional extra agenda item (goes before Other business)
python3 tools/assembly_cycle.py agenda-add 2026-12-08 --title "National symbols vote: date and ballot" --lead "President"

# 2. Print the notice, paste it into Matrix and email it from secretary@ to assembly@
python3 tools/assembly_cycle.py notice 2026-12-08
python3 tools/assembly_cycle.py record-notice 2026-12-08 --sent-at "2026-12-01 09:00" --channel Matrix --channel assembly@parristan.org

# 3. On the night: who's there
python3 tools/assembly_cycle.py attendance 2026-12-08 \
  --present "Joshua Parris" --present "Glenn Peterson" --present "Matthew Walker" \
  --present "Fred Carbunkle" --present "Jane Carbunkle"

# 4. Each motion (item number from the agenda; totals only, never who voted which way)
python3 tools/assembly_cycle.py motion 2026-12-08 --item 5 \
  --text "That the 2026-27 budget of A\$114 be adopted." --short "2026-27 budget adopted" \
  --yes 5 --no 0 --abstain 0 --mover "Fred Carbunkle" --seconder "Jane Carbunkle"

# 5. Notes and actions
python3 tools/assembly_cycle.py note 2026-12-08 --item 4 --text "President reported on the five goals."
python3 tools/assembly_cycle.py action 2026-12-08 --owner "Glenn Peterson" --task "Number founding members" --due 2026-12-20

# 6. Close and review the draft
python3 tools/assembly_cycle.py close 2026-12-08 --at "2026-12-08 20:40"
python3 tools/assembly_cycle.py minutes 2026-12-08

# 7. After members approve the draft (written vote in Matrix, or at the next meeting)
python3 tools/assembly_cycle.py approve-minutes 2026-12-08 --on 2026-12-10 \
  --method "written vote in the official channel" --yes 5 --no 0

# 8. Publish, check, and push
python3 tools/assembly_cycle.py publish 2026-12-08 --on 2026-12-10
python3 scripts/validate_gazette.py && python3 scripts/validate_public_records.py
git add -A && git commit -m "Gazette: minutes of 8 December 2026 Assembly" && git push
```

After the push reaches `main`, GitHub Pages redeploys https://parristan.org automatically.

Between meetings:

```bash
python3 tools/assembly_cycle.py status                                # where every meeting is up to
python3 tools/assembly_cycle.py action-done A-2026-12-08-1 --on 2026-12-18   # updates the public actions page
```

## Mistakes and corrections

- **Before `close`:** edit `assembly/meetings/<date>.json` directly and save. It's plain text.
- **After `close`, before approval:** fix the JSON. Members approve whatever is in the file.
- **After publishing:** don't edit the published notice. Publish a correction notice (Gazette preservation policy) and note it on the [Corrections page](../docs/corrections.html).

## What stays out of these files

No phone numbers, addresses, private papers, or how any individual voted. Secret ballots (elections) are run by the Returning Officer, not this tool.

## Recovery

The meeting files are ordinary Git files, so they are included in the monthly git-bundle backup in [BACKUP_AND_HANDOVER.md](BACKUP_AND_HANDOVER.md). A clone restored from a bundle contains every meeting record and every published notice, and the validators confirm they still agree.
