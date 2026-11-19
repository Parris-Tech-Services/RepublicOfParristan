# Membership policy, privacy notice and appeals (DRAFT)

**For:** Glenn Peterson, Registrar (Gazette 2026-008), then a vote of the Assembly. **Status:** draft. Builds on [citizenship operations](../CITIZENSHIP_OPERATIONS.md).

## 1. Policy
1. **Membership is voluntary** and does not create any legal nationality, passport or rights under Australian law.
2. **Who may apply:** any person who agrees with the Constitution. Applicants under 18 need written consent from a parent or guardian and become *junior members* without a vote.
3. **How:** application form (section 3) sent privately to the Registrar — never by public GitHub issue.
4. **Decision:** the Registrar decides within [14] days. Refusal must be in writing with a reason.
5. **Member number:** issued in order (P-0001, P-0002…) once accepted. Numbers are never reused.
6. **One person, one vote.** The Registrar produces the electoral roll on request of the Returning Officer.
7. **Leaving:** a member may resign at any time by telling the Registrar. Effective that day.
8. **Removal:** only by Assembly vote under the Constitution, with a chance to respond first.
9. **Founders:** the five founders are recorded as members P-0001 to P-0005 once each confirms consent and the date in writing.

## 2. Privacy notice (give to every applicant)
- **What we keep:** your public name, the date you consented, your member number and status (active/resigned). Optional: a contact method you choose.
- **What we do not collect:** addresses, date of birth, ID documents, photographs.
- **Where:** a private register on the Registrar's device, encrypted backup with one other officer. Never in GitHub.
- **Who sees it:** the Registrar and, for the electoral roll only, the Returning Officer. Published reports contain counts only.
- **How long:** while you are a member, plus [12 months] after you leave; then deleted on request or automatically.
- **Your rights:** ask to see, correct or delete your record at any time by contacting the Registrar.

## 3. Application form
> **Republic of Parristan — Membership application**
> Name to be shown on the register: ______________
> Contact method you want us to use (optional): ______________
> I am 18 or over ☐ / I am under 18 and my parent or guardian consents ☐ (guardian name: ______)
> I have read the Constitution and privacy notice and wish to become a member ☐
> Date: __________

## 4. Appeals
1. An applicant refused, or a member removed, may appeal within [28] days by writing to the Secretary.
2. The appeal goes to the next Assembly meeting. The Registrar may explain but does not vote on it.
3. The Assembly's decision is final and recorded (without private details) in the decision register.

## 5. Registry tool commands (for the Registrar)
```bash
python3 tools/parristan_registry.py --db /secure/path/members.sqlite3 init
python3 tools/parristan_registry.py --db /secure/path/members.sqlite3 add --name "Name" --consent-date 2026-11-19
python3 tools/parristan_registry.py --db /secure/path/members.sqlite3 number --id <member-id>
python3 tools/parristan_registry.py --db /secure/path/members.sqlite3 roll --as-of 2026-11-20
python3 tools/parristan_registry.py --db /secure/path/members.sqlite3 report
```
