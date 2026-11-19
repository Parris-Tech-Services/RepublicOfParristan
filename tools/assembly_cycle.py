#!/usr/bin/env python3
"""Run one Assembly meeting cycle end to end, from notice to published record.

    schedule -> notice -> agenda -> attendance/quorum -> motions -> actions
             -> draft minutes -> approve minutes -> publish to the Gazette

Each meeting is one JSON file in assembly/meetings/<YYYY-MM-DD>.json. The file is
the working record; every command checks the meeting is in the right stage and
refuses to skip steps. Publishing writes the Gazette notice, its web page, the
Gazette index, the decision register, docs/data/decisions.json, the decisions
and administration pages, and the public actions page in one consistent step.

Rules applied (adopted standing procedures, Gazette 2026-009, Motion 4):
  * meetings need at least 24 hours' notice in the official channel;
  * quorum is at least 3 members present and voting;
  * a motion passes when YES votes exceed NO votes (abstentions not counted).

Only public information belongs in these files: names, offices, motions, vote
totals and actions. Never record contact details, private papers or how an
individual voted. Standard library only.
"""
import argparse
from datetime import datetime, timedelta
import html
import json
from pathlib import Path
import re
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("Australia/Sydney")
NOTICE_HOURS = 24
STAGES = ["scheduled", "noticed", "held", "minutes_drafted", "minutes_approved", "published"]
DEFAULT_AGENDA = [
    ("Welcome, attendance and apologies", "Chair"),
    ("Minutes of the previous meeting", "Secretary"),
    ("Actions from previous meetings", "Secretary"),
    ("President's report", "President"),
    ("Treasurer's report", "Treasurer"),
    ("Registrar's report", "Registrar"),
    ("Chief Digital Officer's report", "Chief Digital Officer"),
    ("Other business", "Chair"),
    ("Date of next meeting", "Chair"),
]


class CycleError(ValueError):
    """A step was attempted out of order or with invalid input."""


# ---------------------------------------------------------------- storage

def meetings_dir(root):
    return Path(root) / "assembly" / "meetings"


def meeting_path(root, meeting_id):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meeting_id):
        raise CycleError("Meeting ID must be the meeting date, YYYY-MM-DD.")
    return meetings_dir(root) / f"{meeting_id}.json"


def load(root, meeting_id):
    path = meeting_path(root, meeting_id)
    if not path.is_file():
        raise CycleError(f"No meeting {meeting_id}. Run 'schedule' first.")
    return json.loads(path.read_text(encoding="utf-8"))


def save(root, meeting):
    path = meeting_path(root, meeting["id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(meeting, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def roster(root):
    return json.loads((Path(root) / "assembly" / "roster.json").read_text(encoding="utf-8"))


def member_names(root):
    return [m["name"] for m in roster(root)["members"]]


def all_meetings(root):
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted(meetings_dir(root).glob("*.json"))]


def require_stage(meeting, *allowed):
    if meeting["stage"] not in allowed:
        raise CycleError(
            f"Meeting {meeting['id']} is at stage '{meeting['stage']}'; "
            f"this step needs: {', '.join(allowed)}.")


def advance(meeting, stage):
    if STAGES.index(stage) > STAGES.index(meeting["stage"]):
        meeting["stage"] = stage


def parse_local(value):
    """Parse 'YYYY-MM-DD HH:MM' (or ISO) as Sydney local time."""
    try:
        dt = datetime.fromisoformat(value.replace(" ", "T"))
    except ValueError:
        raise CycleError(f"Use date and time as 'YYYY-MM-DD HH:MM', not '{value}'.") from None
    return dt.replace(tzinfo=TZ) if dt.tzinfo is None else dt.astimezone(TZ)


def fmt_dt(value):
    dt = datetime.fromisoformat(value).astimezone(TZ)
    return dt.strftime("%A %-d %B %Y, %-I:%M ") + dt.strftime("%p").lower() + " " + dt.tzname()


def fmt_date(value):
    return datetime.fromisoformat(value).strftime("%-d %B %Y")


def check_names(root, names, what):
    known = set(member_names(root))
    unknown = [n for n in names if n not in known]
    if unknown:
        raise CycleError(f"Not on the Assembly roster ({what}): {', '.join(unknown)}. "
                         f"Roster: {', '.join(sorted(known))}.")


# ---------------------------------------------------------------- steps

def schedule(root, date_time, place, title=None, chair="Joshua Parris", secretary="Jane Carbunkle"):
    start = parse_local(date_time)
    meeting_id = start.date().isoformat()
    if meeting_path(root, meeting_id).exists():
        raise CycleError(f"Meeting {meeting_id} already exists.")
    check_names(root, [chair, secretary], "chair/secretary")
    carried = [dict(a, carried_from=m["id"]) for m in all_meetings(root)
               for a in m["actions"] if a["status"] == "open"]
    meeting = {
        "schema_version": 1,
        "id": meeting_id,
        "title": title or "Monthly Assembly Meeting",
        "stage": "scheduled",
        "starts_at": start.isoformat(),
        "place": place,
        "chair": chair,
        "secretary": secretary,
        "notice": {"sent_at": None, "channels": []},
        "agenda": [{"n": i, "title": t, "lead": lead, "notes": ""}
                   for i, (t, lead) in enumerate(DEFAULT_AGENDA, 1)],
        "carried_actions": [a["id"] for a in carried],
        "attendance": {"present": [], "apologies": [], "quorum": None},
        "motions": [],
        "actions": [],
        "closed_at": None,
        "minutes_approval": None,
        "publication": None,
    }
    save(root, meeting)
    return meeting


def add_agenda_item(root, meeting_id, title, lead, before_other_business=True):
    meeting = load(root, meeting_id)
    require_stage(meeting, "scheduled")
    items = meeting["agenda"]
    pos = next((i for i, a in enumerate(items) if a["title"] == "Other business"), len(items)) \
        if before_other_business else len(items)
    items.insert(pos, {"n": 0, "title": title, "lead": lead, "notes": ""})
    for i, a in enumerate(items, 1):
        a["n"] = i
    save(root, meeting)
    return meeting


def record_notice(root, meeting_id, sent_at, channels):
    meeting = load(root, meeting_id)
    require_stage(meeting, "scheduled")
    sent = parse_local(sent_at)
    start = datetime.fromisoformat(meeting["starts_at"])
    if start - sent < timedelta(hours=NOTICE_HOURS):
        raise CycleError(
            f"Notice sent {fmt_dt(sent.isoformat())} is less than {NOTICE_HOURS} hours before "
            f"the meeting ({fmt_dt(meeting['starts_at'])}). Standing procedures (Gazette 2026-009) "
            "require 24 hours' notice. Reschedule the meeting or give notice earlier.")
    if not channels:
        raise CycleError("Name at least one channel, e.g. Matrix or assembly@parristan.org.")
    meeting["notice"] = {"sent_at": sent.isoformat(), "channels": channels}
    advance(meeting, "noticed")
    save(root, meeting)
    return meeting


def record_attendance(root, meeting_id, present, apologies=(), acting_chair=None, acting_secretary=None):
    meeting = load(root, meeting_id)
    require_stage(meeting, "noticed", "held")
    check_names(root, list(present) + list(apologies), "attendance")
    if set(present) & set(apologies):
        raise CycleError("Someone is listed as both present and an apology.")
    for role, acting in (("chair", acting_chair), ("secretary", acting_secretary)):
        if acting:
            if acting not in present:
                raise CycleError(f"Acting {role} {acting} must be present.")
            meeting[role] = acting
        elif meeting[role] not in present:
            raise CycleError(f"The {role} ({meeting[role]}) is not present; name an acting {role} "
                             f"(--acting-{role}). Members present choose one (Gazette 2026-014, item 2).")
    minimum = roster(root)["quorum_minimum"]
    meeting["attendance"] = {"present": list(present), "apologies": list(apologies),
                             "quorum": len(present) >= minimum}
    advance(meeting, "held")
    save(root, meeting)
    return meeting


def motion_result(yes, no, abstain, present, minimum=3):
    for v in (yes, no, abstain):
        if not isinstance(v, int) or v < 0:
            raise CycleError("Vote counts must be whole numbers, zero or more.")
    voting = yes + no + abstain
    if voting > present:
        raise CycleError(f"{voting} votes recorded but only {present} members present.")
    if voting < minimum:
        return "Lost — fewer than three members voted (Gazette 2026-009)"
    return "Carried" if yes > no else "Lost"


def record_motion(root, meeting_id, agenda_item, text, short_title, yes, no, abstain,
                  mover=None, seconder=None):
    meeting = load(root, meeting_id)
    require_stage(meeting, "held")
    att = meeting["attendance"]
    if not att["quorum"]:
        raise CycleError("No quorum was recorded, so the meeting cannot make decisions.")
    if not any(a["n"] == agenda_item for a in meeting["agenda"]):
        raise CycleError(f"No agenda item {agenda_item}.")
    for who in (mover, seconder):
        if who and who not in att["present"]:
            raise CycleError(f"{who} is not recorded as present.")
    result = motion_result(yes, no, abstain, len(att["present"]))
    motion = {"n": len(meeting["motions"]) + 1, "agenda_item": agenda_item, "text": text.strip(),
              "short_title": short_title.strip(), "mover": mover, "seconder": seconder,
              "yes": yes, "no": no, "abstain": abstain, "result": result}
    meeting["motions"].append(motion)
    save(root, meeting)
    return motion


def add_note(root, meeting_id, agenda_item, note):
    meeting = load(root, meeting_id)
    require_stage(meeting, "held")
    for a in meeting["agenda"]:
        if a["n"] == agenda_item:
            a["notes"] = (a["notes"] + "\n" + note.strip()).strip()
            save(root, meeting)
            return a
    raise CycleError(f"No agenda item {agenda_item}.")


def add_action(root, meeting_id, owner, task, due):
    meeting = load(root, meeting_id)
    require_stage(meeting, "held")
    check_names(root, [owner], "action owner")
    datetime.fromisoformat(due)  # validates YYYY-MM-DD
    action = {"id": f"A-{meeting_id}-{len(meeting['actions']) + 1}", "owner": owner,
              "task": task.strip(), "due": due, "status": "open", "done_on": None}
    meeting["actions"].append(action)
    save(root, meeting)
    return action


def complete_action(root, action_id, done_on):
    datetime.fromisoformat(done_on)
    for meeting in all_meetings(root):
        for a in meeting["actions"]:
            if a["id"] == action_id:
                if a["status"] == "done":
                    raise CycleError(f"{action_id} is already done.")
                a["status"], a["done_on"] = "done", done_on
                save(root, meeting)
                return a
    raise CycleError(f"No action {action_id}.")


def close_meeting(root, meeting_id, closed_at):
    meeting = load(root, meeting_id)
    require_stage(meeting, "held")
    closed = parse_local(closed_at)
    if closed <= datetime.fromisoformat(meeting["starts_at"]):
        raise CycleError("The meeting must close after it starts.")
    meeting["closed_at"] = closed.isoformat()
    advance(meeting, "minutes_drafted")
    save(root, meeting)
    return meeting


def approve_minutes(root, meeting_id, approved_on, method, yes, no, abstain):
    """Minutes are approved by a later meeting or a written vote (Gazette 2026-009)."""
    meeting = load(root, meeting_id)
    require_stage(meeting, "minutes_drafted")
    approved = datetime.fromisoformat(approved_on).date()
    if approved < datetime.fromisoformat(meeting["closed_at"]).date():
        raise CycleError("Minutes can't be approved before the meeting closed.")
    result = motion_result(yes, no, abstain, len(member_names(root)))
    if result != "Carried":
        raise CycleError(f"Approval vote {yes}-{no}-{abstain}: {result}. Correct the minutes and vote again.")
    meeting["minutes_approval"] = {"approved_on": approved.isoformat(), "method": method,
                                   "yes": yes, "no": no, "abstain": abstain}
    advance(meeting, "minutes_approved")
    save(root, meeting)
    return meeting


# ---------------------------------------------------------------- rendering

def render_notice(root, meeting_id):
    m = load(root, meeting_id)
    lines = [f"Subject: Notice — {m['title']}, {fmt_date(m['starts_at'])}", "",
             f"The Assembly of the Republic of Parristan will meet ({m['title']}) on",
             f"{fmt_dt(m['starts_at'])}, {m['place']}.", "",
             f"Chair: {m['chair']}. Minutes: {m['secretary']}.", "", "AGENDA"]
    lines += [f"{a['n']}. {a['title']}" for a in m["agenda"]]
    if m["carried_actions"]:
        lines += ["", "Open actions carried forward: " + ", ".join(m["carried_actions"])]
    lines += ["", "Quorum: at least three members (Gazette 2026-009).",
              "Send items for other business to secretary@parristan.org.", "",
              m["secretary"], "Secretary, Republic of Parristan"]
    return "\n".join(lines) + "\n"


def _carried(root, m):
    index = {a["id"]: a for mt in all_meetings(root) for a in mt["actions"]}
    return [index[i] for i in m["carried_actions"] if i in index]


def render_minutes(root, meeting_id):
    m = load(root, meeting_id)
    att = m["attendance"]
    status = ("CONFIRMED" if m["minutes_approval"] else "DRAFT — not yet approved")
    out = [f"# Minutes — {m['title']}, {fmt_date(m['starts_at'])}", "", f"**Status:** {status}", "",
           "**Republic of Parristan · Assembly**", "",
           f"- **Opened:** {fmt_dt(m['starts_at'])}",
           f"- **Closed:** {fmt_dt(m['closed_at']) if m['closed_at'] else '—'}",
           f"- **Place:** {m['place']}",
           f"- **Chair:** {m['chair']} · **Minutes:** {m['secretary']}",
           f"- **Notice:** sent {fmt_dt(m['notice']['sent_at']) if m['notice']['sent_at'] else '—'}"
           + (f" via {', '.join(m['notice']['channels'])}" if m['notice']['channels'] else ""),
           f"- **Present ({len(att['present'])}):** {', '.join(att['present']) or '—'}",
           f"- **Apologies:** {', '.join(att['apologies']) or 'none'}",
           f"- **Quorum (at least 3):** {'met' if att['quorum'] else 'NOT met'}", ""]
    for a in m["agenda"]:
        out += [f"## {a['n']}. {a['title']}", ""]
        if a["title"] == "Actions from previous meetings":
            carried = _carried(root, m)
            out += [f"- {c['id']} — {c['owner']}: {c['task']} ({c['status']})" for c in carried] or ["No open actions."]
            out.append("")
        if a["notes"]:
            out += [a["notes"], ""]
        for mo in (x for x in m["motions"] if x["agenda_item"] == a["n"]):
            who = ", ".join(filter(None, [f"moved {mo['mover']}" if mo["mover"] else "",
                                          f"seconded {mo['seconder']}" if mo["seconder"] else ""]))
            out += [f"**Motion {mo['n']}:** {mo['text']}", "",
                    f"{('(' + who + ') ') if who else ''}YES {mo['yes']} · NO {mo['no']} · "
                    f"ABSTAIN {mo['abstain']} — **{mo['result']}**", ""]
    out += ["## Actions", "", "| ID | Owner | Action | Due | Status |", "| --- | --- | --- | --- | --- |"]
    out += [f"| {x['id']} | {x['owner']} | {x['task']} | {x['due']} | {x['status']} |" for x in m["actions"]] \
        or ["| — | — | No new actions | — | — |"]
    out.append("")
    if m["minutes_approval"]:
        ap = m["minutes_approval"]
        out.append(f"Minutes confirmed {fmt_date(ap['approved_on'])} by {ap['method']} "
                   f"(YES {ap['yes']} · NO {ap['no']} · ABSTAIN {ap['abstain']}).")
    else:
        out.append("Draft minutes taken by the Secretary, for confirmation.")
    out += ["", "*No personal contact details or individual voting choices are recorded.*"]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- publishing

def _next_notice_number(root, year):
    ids = [p.name[:8] for p in (Path(root) / "gazette").glob("20??/*.md")]
    nums = [int(i[5:]) for i in ids if i.startswith(str(year))]
    return f"{year}-{(max(nums) + 1 if nums else 1):03d}"


def _replace_once(text, old, new, where):
    if old not in text:
        raise CycleError(f"Publishing aborted: expected anchor not found in {where}.")
    return text.replace(old, new, 1)


def publish(root, meeting_id, published_on=None):
    """Write every public record for an approved meeting, all or nothing."""
    root = Path(root)
    m = load(root, meeting_id)
    require_stage(m, "minutes_approved")
    published_on = published_on or datetime.now(TZ).date().isoformat()
    pub_date = fmt_date(published_on)
    if published_on < m["minutes_approval"]["approved_on"]:
        raise CycleError("Can't publish before the minutes were confirmed.")
    year = published_on[:4]
    number = _next_notice_number(root, year)
    slug = f"{number}-assembly-meeting-{m['id']}"
    data_path = root / "docs/data/decisions.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    last = max(int(d["id"].split("-")[-1]) for d in data["decisions"])
    decisions = []
    for i, mo in enumerate(m["motions"], 1):
        decisions.append({
            "id": f"FA-2026-{last + i:03d}", "date": m["id"], "meeting": m["title"],
            "title": f"{mo['short_title']} ({mo['result'].split(' —')[0]})",
            "result": f"{mo['yes']} YES / {mo['no']} NO / {mo['abstain']} ABSTAIN — {mo['result']}",
            "yes": mo["yes"], "no": mo["no"], "abstain": mo["abstain"],
            "notice": number, "source": f"gazette/{year}/{slug}.md"})
    minutes_md = render_minutes(root, meeting_id)
    files = {}  # path -> new content; written only after everything renders

    # 1. Gazette notice (Markdown): approved minutes plus publication header
    rel_minutes = f"../../assembly/meetings/{m['id']}.json"
    files[root / f"gazette/{year}/{slug}.md"] = (
        f"# Gazette No. {number} — {m['title']}, {fmt_date(m['starts_at'])}\n\n"
        f"**Published:** {pub_date}\n"
        f"**Authority:** Standing procedures, Gazette 2026-009; minutes confirmed "
        f"{fmt_date(m['minutes_approval']['approved_on'])}\n"
        f"**Record:** [meeting record (JSON)]({rel_minutes}); civic/association record, not Australian public law.\n\n"
        + minutes_md.split("\n", 1)[1])

    # 2. Gazette index row
    idx_path = root / "gazette/INDEX.md"
    idx = idx_path.read_text(encoding="utf-8")
    rows = re.findall(r"^\| \[\d{4}-\d{3}\]\(.*$", idx, flags=re.MULTILINE)
    carried = sum(1 for x in m["motions"] if x["result"] == "Carried")
    row = (f"| [{number}]({year}/{slug}.md) | {pub_date} | {m['title']}, {fmt_date(m['starts_at'])} "
           f"| Published — minutes confirmed; {carried} of {len(m['motions'])} motions carried |")
    files[idx_path] = _replace_once(idx, rows[-1], rows[-1] + "\n" + row, "gazette/INDEX.md")

    # 3. Decision register rows
    reg_path = root / "institutions/DECISION_REGISTER.md"
    reg = reg_path.read_text(encoding="utf-8")
    reg_rows = re.findall(r"^\| FA-\d{4}-\d{3} \|.*$", reg, flags=re.MULTILINE)
    new_rows = "\n".join(
        f"| {d['id']} | {fmt_date(m['id'])} | {mo['text']} | **{mo['yes']} YES / {mo['no']} NO / "
        f"{mo['abstain']} ABSTAIN** — {mo['result']} | [Gazette {number}](../gazette/{year}/{slug}.md) |"
        for d, mo in zip(decisions, m["motions"]))
    files[reg_path] = _replace_once(reg, reg_rows[-1], reg_rows[-1] + ("\n" + new_rows if new_rows else ""),
                                    "institutions/DECISION_REGISTER.md") if decisions else reg

    # 4. Machine-readable decisions
    data["decisions"].extend(decisions)
    data["recorded_as_of"] = published_on
    files[data_path] = json.dumps(data, indent=2, ensure_ascii=False) + "\n"

    # 5. HTML rows on decisions and administration pages
    html_rows = "".join(
        f'<tr data-decision-id="{d["id"]}"><th scope="row">{d["id"]}</th><td>{html.escape(d["title"])}</td>'
        f'<td>{html.escape(d["result"])}</td><td><a href="notices/{number}.html">Gazette {number}</a></td></tr>\n'
        for d in decisions)
    for page in ("docs/decisions.html", "docs/administration.html"):
        p = root / page
        text = p.read_text(encoding="utf-8")
        if decisions:
            last_row = re.findall(r'<tr data-decision-id="FA-\d{4}-\d{3}">.*?</tr>\n', text, flags=re.S)[-1]
            text = _replace_once(text, last_row, last_row + html_rows, page)
        files[p] = text

    # 6. Notice web page, built from the most recent notice's page shell
    shell_src = sorted((root / "docs/notices").glob("*.html"))[-1].read_text(encoding="utf-8")
    a, b = shell_src.index('<main id="main">'), shell_src.index("</main>")
    body = _minutes_html(root, m, number, pub_date)
    page = shell_src[:a] + body + shell_src[b:]
    page = re.sub(r"<title>[^<]*</title>", f"<title>Notice {number} · Republic of Parristan Gazette</title>", page)
    page = re.sub(r'<meta name="description" content="[^"]*">',
                  f'<meta name="description" content="Gazette {number}: confirmed minutes of the '
                  f'{html.escape(m["title"])}, {fmt_date(m["starts_at"])}.">', page)
    files[root / f"docs/notices/{number}.html"] = page

    # 7. Homepage card and count
    home_path = root / "docs/index.html"
    home = home_path.read_text(encoding="utf-8")
    cards = re.findall(r'<a class="notice" href="notices/\d{4}-\d{3}\.html" data-notice.*?</a>', home, flags=re.S)
    card = (f'<a class="notice" href="notices/{number}.html" data-notice data-category="assembly">'
            f'<div class="meta"><span>No. {number}</span><span>{fmt_date(published_on)}</span>'
            f'<span class="tag">Minutes</span></div><h3>{html.escape(m["title"])}, {fmt_date(m["starts_at"])}</h3>'
            f'<p>Confirmed minutes: {carried} of {len(m["motions"])} motions carried, '
            f'{len(m["actions"])} actions assigned.</p></a>')
    home = _replace_once(home, cards[-1], cards[-1] + card, "docs/index.html")
    count = len(list((root / "gazette").glob("20??/*.md"))) + 1
    home = re.sub(r"<strong>\d+</strong><span>Published notices</span>",
                  f"<strong>{count}</strong><span>Published notices</span>", home)
    files[home_path] = home

    # 8. Meeting record
    m["publication"] = {"gazette": number, "published_on": published_on,
                        "decision_ids": [d["id"] for d in decisions]}
    m["stage"] = "published"
    files[meeting_path(root, m["id"])] = json.dumps(m, indent=2, ensure_ascii=False) + "\n"

    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    write_actions_page(root)
    return number, [d["id"] for d in decisions]


def _minutes_html(root, m, number, pub_date):
    e = html.escape
    att = m["attendance"]
    parts = [
        '<main id="main"><section class="page-hero"><div class="container"><div class="breadcrumbs">'
        f'<a href="../index.html">Gazette</a> / Notice {number}</div>'
        f'<div class="eyebrow" style="color:#e9c58a">Gazette notice {number} · {pub_date}</div>'
        f'<h1>{e(m["title"])}, {fmt_date(m["starts_at"])}</h1><p>Confirmed minutes of the Assembly.</p>'
        '</div></section><section class="section"><div class="container page-layout"><article class="prose">',
        f'<p class="kicker">Published {pub_date} · Australia/Sydney</p>',
        f'<div class="highlight"><strong>Status:</strong> Minutes confirmed '
        f'{fmt_date(m["minutes_approval"]["approved_on"])} by {e(m["minutes_approval"]["method"])}. '
        '<strong>Legal effect:</strong> Internal voluntary association record only.</div>',
        '<div class="table-wrap"><table><tbody>',
        f'<tr><th scope="row">Opened</th><td>{fmt_dt(m["starts_at"])}</td></tr>',
        f'<tr><th scope="row">Closed</th><td>{fmt_dt(m["closed_at"])}</td></tr>',
        f'<tr><th scope="row">Place</th><td>{e(m["place"])}</td></tr>',
        f'<tr><th scope="row">Chair / minutes</th><td>{e(m["chair"])} / {e(m["secretary"])}</td></tr>',
        f'<tr><th scope="row">Present</th><td>{e(", ".join(att["present"]))}</td></tr>',
        f'<tr><th scope="row">Apologies</th><td>{e(", ".join(att["apologies"]) or "none")}</td></tr>',
        f'<tr><th scope="row">Quorum</th><td>{"Met" if att["quorum"] else "Not met"} (at least 3)</td></tr>',
        '</tbody></table></div>']
    for a in m["agenda"]:
        motions = [x for x in m["motions"] if x["agenda_item"] == a["n"]]
        if not a["notes"] and not motions:
            continue
        parts.append(f'<h2>{a["n"]}. {e(a["title"])}</h2>')
        if a["notes"]:
            parts += [f"<p>{e(p)}</p>" for p in a["notes"].split("\n") if p.strip()]
        for mo in motions:
            parts.append(f'<p><strong>Motion {mo["n"]}:</strong> {e(mo["text"])}<br>'
                         f'YES {mo["yes"]} · NO {mo["no"]} · ABSTAIN {mo["abstain"]} — '
                         f'<strong>{e(mo["result"])}</strong></p>')
    parts.append('<h2>Actions</h2><div class="table-wrap"><table class="stack"><thead><tr><th scope="col">ID</th>'
                 '<th scope="col">Owner</th><th scope="col">Action</th><th scope="col">Due</th></tr></thead><tbody>')
    parts += [f'<tr><td data-label="ID" class="nowrap">{x["id"]}</td><td data-label="Owner">{e(x["owner"])}</td>'
              f'<td data-label="Action">{e(x["task"])}</td><td data-label="Due" class="nowrap">{x["due"]}</td></tr>'
              for x in m["actions"]] or ['<tr><td colspan="4">No new actions.</td></tr>']
    parts.append('</tbody></table></div><p>Progress on actions: <a href="../actions.html">Assembly actions</a>.</p>'
                 '</article></div></section>')
    return "".join(parts)


def write_actions_page(root):
    """Regenerate docs/actions.html listing actions from published meetings only."""
    root = Path(root)
    published = [m for m in all_meetings(root) if m["stage"] == "published"]
    rows = []
    for m in published:
        for a in m["actions"]:
            state = f'Done {a["done_on"]}' if a["status"] == "done" else "Open"
            rows.append(f'<tr><td data-label="ID" class="nowrap">{a["id"]}</td>'
                        f'<td data-label="Owner">{html.escape(a["owner"])}</td>'
                        f'<td data-label="Action">{html.escape(a["task"])}</td>'
                        f'<td data-label="Due" class="nowrap">{a["due"]}</td><td data-label="Status">{state}</td>'
                        f'<td data-label="Source"><a href="notices/{m["publication"]["gazette"]}.html">'
                        f'Gazette {m["publication"]["gazette"]}</a></td></tr>')
    shell = (root / "docs/status.html").read_text(encoding="utf-8")
    a, b = shell.index('<main id="main">'), shell.index("</main>")
    body = ('<main id="main"><section class="section"><div class="container"><article class="prose">'
            '<h1>Assembly actions</h1><p>Actions assigned at Assembly meetings, from confirmed minutes. '
            'Updated whenever minutes are published or an action is completed.</p>'
            '<div class="table-wrap"><table class="stack"><thead><tr><th scope="col">ID</th><th scope="col">Owner</th>'
            '<th scope="col">Action</th><th scope="col">Due</th><th scope="col">Status</th>'
            '<th scope="col">Source</th></tr></thead><tbody>'
            + ("".join(rows) or '<tr><td colspan="6">No actions from published minutes yet.</td></tr>')
            + '</tbody></table></div></article></div></section>')
    page = shell[:a] + body + shell[b:]
    page = re.sub(r"<title>[^<]*</title>", "<title>Assembly actions · Republic of Parristan Gazette</title>", page)
    page = re.sub(r'<meta name="description" content="[^"]*">',
                  '<meta name="description" content="Actions assigned at Republic of Parristan Assembly meetings and their status.">', page)
    (root / "docs/actions.html").write_text(page, encoding="utf-8")


def status_report(root):
    lines = []
    for m in all_meetings(root):
        nxt = {"scheduled": "record-notice", "noticed": "attendance", "held": "motion / action / note, then close",
               "minutes_drafted": "approve-minutes", "minutes_approved": "publish", "published": "—"}[m["stage"]]
        open_actions = sum(1 for a in m["actions"] if a["status"] == "open")
        lines.append(f"{m['id']}  {m['stage']:<17} next: {nxt:<36} open actions: {open_actions}")
    return "\n".join(lines) or "No meetings scheduled."


# ---------------------------------------------------------------- CLI

def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    s = p.add_subparsers(dest="cmd", required=True)
    c = s.add_parser("schedule", help="create a meeting"); c.add_argument("--at", required=True, help="'YYYY-MM-DD HH:MM' Sydney time")
    c.add_argument("--place", required=True); c.add_argument("--title")
    c = s.add_parser("agenda-add", help="add an agenda item before Other business"); c.add_argument("meeting")
    c.add_argument("--title", required=True); c.add_argument("--lead", required=True)
    c = s.add_parser("notice", help="print the notice text to send"); c.add_argument("meeting")
    c = s.add_parser("record-notice", help="record when notice was sent"); c.add_argument("meeting")
    c.add_argument("--sent-at", required=True); c.add_argument("--channel", action="append", required=True)
    c = s.add_parser("attendance"); c.add_argument("meeting"); c.add_argument("--present", action="append", required=True)
    c.add_argument("--apology", action="append", default=[])
    c.add_argument("--acting-chair"); c.add_argument("--acting-secretary")
    c = s.add_parser("note"); c.add_argument("meeting"); c.add_argument("--item", type=int, required=True); c.add_argument("--text", required=True)
    c = s.add_parser("motion"); c.add_argument("meeting"); c.add_argument("--item", type=int, required=True)
    c.add_argument("--text", required=True); c.add_argument("--short", required=True, help="short public title")
    c.add_argument("--yes", type=int, required=True); c.add_argument("--no", type=int, required=True)
    c.add_argument("--abstain", type=int, default=0); c.add_argument("--mover"); c.add_argument("--seconder")
    c = s.add_parser("action"); c.add_argument("meeting"); c.add_argument("--owner", required=True)
    c.add_argument("--task", required=True); c.add_argument("--due", required=True)
    c = s.add_parser("action-done"); c.add_argument("action_id"); c.add_argument("--on", required=True)
    c = s.add_parser("close"); c.add_argument("meeting"); c.add_argument("--at", required=True)
    c = s.add_parser("minutes", help="print minutes (draft or confirmed)"); c.add_argument("meeting")
    c = s.add_parser("approve-minutes"); c.add_argument("meeting"); c.add_argument("--on", required=True)
    c.add_argument("--method", required=True, help="e.g. 'the Assembly meeting of 12 January 2027'")
    c.add_argument("--yes", type=int, required=True); c.add_argument("--no", type=int, required=True)
    c.add_argument("--abstain", type=int, default=0)
    c = s.add_parser("publish"); c.add_argument("meeting"); c.add_argument("--on")
    s.add_parser("status")
    a = p.parse_args(argv)
    r = a.root
    try:
        if a.cmd == "schedule":
            m = schedule(r, a.at, a.place, a.title)
            print(f"Scheduled {m['id']} ({fmt_dt(m['starts_at'])}). Carried actions: {len(m['carried_actions'])}.")
        elif a.cmd == "agenda-add":
            add_agenda_item(r, a.meeting, a.title, a.lead); print("Agenda updated.")
        elif a.cmd == "notice":
            print(render_notice(r, a.meeting), end="")
        elif a.cmd == "record-notice":
            record_notice(r, a.meeting, a.sent_at, a.channel); print("Notice recorded; 24-hour rule met.")
        elif a.cmd == "attendance":
            m = record_attendance(r, a.meeting, a.present, a.apology, a.acting_chair, a.acting_secretary)
            print(f"{len(m['attendance']['present'])} present — quorum {'met' if m['attendance']['quorum'] else 'NOT met'}.")
        elif a.cmd == "note":
            add_note(r, a.meeting, a.item, a.text); print("Note added.")
        elif a.cmd == "motion":
            mo = record_motion(r, a.meeting, a.item, a.text, a.short, a.yes, a.no, a.abstain, a.mover, a.seconder)
            print(f"Motion {mo['n']}: {mo['result']}.")
        elif a.cmd == "action":
            print("Action", add_action(r, a.meeting, a.owner, a.task, a.due)["id"])
        elif a.cmd == "action-done":
            complete_action(r, a.action_id, a.on); write_actions_page(r); print("Action marked done.")
        elif a.cmd == "close":
            close_meeting(r, a.meeting, a.at); print("Meeting closed; minutes drafted. Run 'minutes' to review.")
        elif a.cmd == "minutes":
            print(render_minutes(r, a.meeting), end="")
        elif a.cmd == "approve-minutes":
            approve_minutes(r, a.meeting, a.on, a.method, a.yes, a.no, a.abstain); print("Minutes confirmed.")
        elif a.cmd == "publish":
            number, ids = publish(r, a.meeting, a.on)
            print(f"Published Gazette {number}; decisions {', '.join(ids) or 'none'}. "
                  "Run the validators, commit and push; the site deploys from main.")
        elif a.cmd == "status":
            print(status_report(r))
    except (CycleError, ValueError) as exc:
        p.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
