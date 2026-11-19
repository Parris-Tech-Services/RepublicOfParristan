# Claude work plan — 19 November 2026

Tasks a coding assistant can complete in this repository without casting votes, holding office or touching private records. Everything marked **draft** needs the responsible official or the founders to adopt it before it has any effect. Ticks here mean "file written and checked", not "adopted".

## Technical
1. [ ] Check whether GitHub Pages is live → **not live (HTTP 404 on 19 Nov)**; add a Pages deploy workflow and setup guide: [operations/PAGES_PUBLISHING.md](operations/PAGES_PUBLISHING.md). Checklist item 34 stays open until the URL actually loads.
2. [ ] Backup and handover procedure plus backup script: [operations/BACKUP_AND_HANDOVER.md](operations/BACKUP_AND_HANDOVER.md), `scripts/backup_records.sh`.
3. [ ] Low-cost link checking: relative links are already checked on every push by `scripts/validate_gazette.py`; added a manual-only external link checker (`scripts/check_external_links.py`, workflow `check-external-links.yml`).
4. [ ] Joint admin access guide (Gazette 2026-009): [operations/ADMIN_ACCESS_SETUP.md](operations/ADMIN_ACCESS_SETUP.md).
5. [ ] Website: decisions register, status and corrections/contact pages (`docs/decisions.html`, `docs/status.html`, `docs/corrections.html`).
6. [ ] Registry tool: electoral roll export, aggregate report, member numbers, with tests.
7. [ ] Digital pilot guide, open document template and dependency inventory: [operations/DIGITAL_PILOT_GUIDE.md](operations/DIGITAL_PILOT_GUIDE.md), [templates/OFFICIAL_DOCUMENT.md](templates/OFFICIAL_DOCUMENT.md), [operations/DEPENDENCY_INVENTORY.md](operations/DEPENDENCY_INVENTORY.md).

## Drafts for approval (in `operations/drafts/`)
8. [ ] [Election kit](operations/drafts/ELECTION_KIT.md) for the Returning Officer.
9. [ ] [Membership policy, privacy notice, application and appeals](operations/drafts/MEMBERSHIP_POLICY.md) for the Registrar.
10. [ ] [Financial controls](operations/drafts/FINANCIAL_CONTROLS.md) for the Treasurer.
11. [ ] [Legal form comparison](operations/drafts/LEGAL_FORM_COMPARISON.md) — not legal advice.
12. [ ] [Symbol ballot, specifications and register](operations/drafts/SYMBOLS_SPEC_AND_REGISTER.md).
13. [ ] [Correspondence protocol and first-contact letter](operations/drafts/CORRESPONDENCE_PROTOCOL.md).
14. [ ] [Permanent email/chat proposal template](operations/drafts/COMMS_PROPOSAL_TEMPLATE.md) — due 3 December 2026.
15. [ ] [Founding-meeting audit forms](operations/drafts/FOUNDING_AUDIT_FORMS.md).

## Out of scope for an assistant
Voting, certifying results, holding office, incorporation lodgement, land permissions, anything in the Matrix room or private records.
