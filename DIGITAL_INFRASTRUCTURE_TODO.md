# Parristan digital government to-do list

Track delivery here. Mark a capability complete only when its operator, acceptance checks and supporting evidence are recorded. Record access details and private information in the intranet or another approved private store.

## Staff intranet

- [ ] Staff home: announcements, upcoming meetings, assigned actions, deadlines and service shortcuts.
- [ ] Directory: people, offices, delegates, deputies, contact routes and responsibilities.
- [ ] Meetings: calendar, notices, agendas, papers, attendance, quorum, minutes approval and action tracking.
- [ ] Decisions: current constitution and standing orders, searchable motions and resolutions, delegations, approval authority, effective dates and version history.
- [ ] Elections: Returning Officer-controlled nominations, one-person electoral roll, ballot windows, confidential ballot handling, counting, certification and authorised results. Keep ballots outside the work register.
- [ ] Files: approved document store, access by office or committee, search, co-editing, version history and safe sharing.
- [ ] Forms: private requests for spending, access and publication, with reviewer assignment, approval history and status.
- [ ] Office workspaces: procedures, templates, registers, handovers and server-enforced access for restricted records.
- [ ] Policies and help: onboarding, accessibility support, service desk and incident reporting.

## Infrastructure and operations

- [ ] Identity: verify office email sign-in and how mailboxes map to people; implement role permissions, administrator separation, access reviews, onboarding, offboarding, and MFA or stronger identity where required.
- [ ] Communications: verify mail delivery, aliases and ownership; establish shared calendars and chat, with agreed retention and handover.
- [ ] Records and archives: identify authoritative copies, record approvals and versions, adopt retention and disposal rules, support open exports and restore archived records.
- [ ] Domains and networks: record ownership, renewal dates, DNS and certificates; establish protected remote access and segment physical networks if operated.
- [ ] Hosting and data: inventory services and owners; maintain production and test environments, databases, file storage and secure configuration.
- [ ] Delivery: version releases, review and test changes, record deployed revisions and verify rollback.
- [ ] Security operations: asset inventory, patching, endpoint protection, logs, alerts, incident response and a responsible operator.
- [ ] Continuity: export records and configuration, test restore, agree recovery targets and verify recovery by a second authorised person.
- [ ] Privacy: document collection purpose, access, retention, sharing and incident handling.
- [ ] Accountability: document owners, deputies, support requests, suppliers, renewal dates, spending approvals, monitoring and handover.
- [ ] Accessibility: test mobile, keyboard, forms and documents; provide plain language, accessible alternatives and a feedback route.

## Public and future services

- [ ] Public services: maintain the official website and Gazette; add approved consultation, service directory, applications, case tracking, complaints and accessible support.
- [ ] Core administration: implement approved finance, budgeting, procurement, contracts, assets, workforce and payroll workflows with approval records.
- [ ] Shared services: assess identity, notifications, payments, signatures, data exchange, APIs and open data against actual service needs.
- [ ] Service-specific systems: evaluate licensing, planning and land, taxation, benefits, health, education, justice, elections and emergency management when there is an approved remit, owner and continuity plan.

## First milestone

Complete one Assembly cycle using the private intranet and approved communication channel: issue notice, prepare agenda, record attendance and quorum, approve minutes, track actions, publish the authorised record and restore a backup. Existing service links: [official public website](https://parristan.org/) and [private intranet](https://intranet.parristan.org/).

References: [Digital Service Standard](https://architecture.digital.gov.au/standard/digital-service-standard) and [Essential Eight / ISM mapping](https://www.cyber.gov.au/sites/default/files/2025-03/Essential%20Eight%20maturity%20model%20and%20ISM%20mapping%20%28October%202024%29.pdf).

## Delivery record — 19 November 2026

- Deployed the [private intranet](https://intranet.parristan.org/) with an office directory, links to adopted rules and published decisions, office-specific action summaries, a dated work list, searchable shared work items and digital support links. Assign an action to the exact office email to show it in that office’s summary.
- Added an account-administration-only JSON export at `/backup.json`. A local test restored the exported work items and activity history into a fresh database and compared the rows. A second-person restore, approved backup destination, backup schedule and recovery targets remain open.
- Verified search, account restrictions and export/restore with synthetic office identities and data. Browser sign-in and officer acceptance still need a real mailbox session.
- The first presidential election is already recorded in [Gazette 2026-013](gazette/2026/2026-013-first-president-confirmed.md). Future electronic voting requires the Returning Officer to confirm the electoral roll, approve the ballot method and verify one-person eligibility independently of office email addresses.
- The existing shared register supports agenda items and actions. Meeting notice delivery, minutes approval, delegated permissions, restricted document sharing and service workflows remain open.

### Work-register recovery

The account administrator can download the export from the signed-in intranet. Store it in the approved private backup destination. In a separate recovery database, apply the work-register schema, import items before activity entries, and compare row counts and representative records with the export. Keep the export out of the public repository. Record the restore date, operator and outcome without copying private contents into the Gazette.
