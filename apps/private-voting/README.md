# Parristan Private Assembly — Voting service v1

**Privacy:** the public GitHub repository contains program code and documented rules, not member passwords, ballot data or private enrolment credentials. The application itself requires private authenticated access.

**Implementation status:** invite-only founder records and a database, server-side authenticated motions, atomic one-vote-per-founder enforcement, role-based officer workflow, dual checking and private aggregate tally exist in source. **Live production deployment, initial organiser activation and founder logins must be verified separately.** This project is not proof a real vote has occurred. **New secret election ballots (for other offices or a future vacancy) are deliberately locked** until the Returning Officer confirms the actual method and times and an independent security/privacy review is completed.

## Governing rules

- Constitution v0.1 Article IV: eligible adult member, one vote each; ordinary motions by a simple majority of valid votes.
- Founding Motion 4, Gazette 2026-009: written votes run for 48 hours, or may close once every member votes; quorum minimum **three voters**; majority of valid votes cast.
- Constitution Article XI: full text of an amendment available at least **14 days** before voting and a two-thirds majority of valid votes.
- Motion 2, Gazette 2026-007 appointed Matthew Walker independent Returning Officer. The **original 20–27 November nominations and 28 November–1 December poll were superseded** by unanimous Motion 6, [Gazette 2026-012](../../gazette/2026/2026-012-election-timetable-brought-forward.md): same-day nominations and a confirmation ballot on **19 November 2026**, by confidential email to returningofficer@parristan.org. The published [result in Gazette 2026-013](../../gazette/2026/2026-013-first-president-confirmed.md) records **Joshua Parris confirmed as first President, YES 5, NO 0**, with a term from 19 November 2026 to 19 November 2028. The original ballots are NOT in this service, and the app makes no independent claim to have verified them.
- First-election rules were a draft; Motion 6 specifically authorised the 19 November email method. Future elections must follow whichever rules the Assembly and Returning Officer actually approve. A sole-candidate YES/NO confirmation and contested majority/runoff are draft procedures for other elections, not an excuse to rerun the concluded presidential poll.
- Motion 3, Gazette 2026-008: Jane Carbunkle Secretary, Fred Carbunkle Treasurer and Glenn Peterson Registrar; Glenn is CDO and joint technical administrator with Joshua Parris. [Gazette 2026-014](../../gazette/2026/2026-014-presidents-first-programme.md) additionally records the President's programme, including Matrix debate and votes, official email notices/correspondence, financial controls, and later symbol ballots. The [official website](https://parristan.org/) was adopted in Gazette 2026-015.
- Motions 1, 5 and 7 (Gazette 2026-006, 010 and 014): the encrypted Matrix room remains the **official channel for debate and votes**; official email handles notices/correspondence. The voting portal supplements this channel and **cannot replace it without a properly adopted further resolution**. Using a portal ballot is not, by itself, an official Matrix vote.

## Deployment

Vercel project rooted at this directory, with Node 22+, plain static pages and serverless API. Dedicated Postgres database **parristan_ballots** on the connected Neon resource; app-only scoped role. These are required project environment variables (set privately, not committed):

- DATABASE_URL — Postgres connection string for a least-privilege application role.
- BOOTSTRAP_KEY — random high-entropy single-use organiser setup code.
- SECRET_ELECTIONS_ENABLED — leave **false** until an independent election security review, approval by eligible members and a formal Returning Officer method.

One organiser activation creates a password for Josh; two technical admins can then generate 48-hour single-use account activation invitations, shared privately with each founder. There is no guessed founder email, public registration or password sent through the public Gazette.

## Security boundaries and limitations

- Server-side roles, HttpOnly Secure SameSite Strict sessions, CSRF token/Origin checks, scrypt password hashing, failed sign-in throttling and parameterised SQL.
- A unique participation row plus a separately stored ballot choice are committed atomically, preventing duplicate ballots and inconsistent counts.
- Choices have **no voter ID or timestamp** in the application table; audit logs record who performed officer actions, not a member's choice.
- However, a five-member election can reveal voting preferences through inference, timing or privileged database logs. **This is not cryptographic end-to-end verifiable secret voting.** Avoid official secret elections until independently assessed; use separately authorised paper/envelope voting if necessary.
- The site does not independently verify a published Matrix notice, voter identity, nomination eligibility, real-world consent, appeal hearing or external certification. Officer attestation is required.
- The office roles, election timetable and constitutional amendment rules were taken from the actual published founding documents, but the first election's final regulations remain for the returning officer and Assembly to agree.
- Existing Gazette decisions are not replayed as ballots and no Presidency is automatically created.
- Do not enable real voting until the secure live service and all five founders' access have been verified with the responsible officers.

## Tests and operational controls

Node built-in test suite checks quorum, ordinary majority, amendment thresholds, amendment notice, early closure, first-election majority/runoff, vote windows and count consistency. GitHub Actions runs this on every change in this application. Deployment requires separate runtime verification (login, session, same-origin, admin controls, atomically rejected duplicate vote) before reporting operational success.

## Historical election status in the portal

Do not import, recreate or count the 19 November 2026 presidential confirmation as if it happened inside the portal. Gazette 2026-013 is the official published historical record as supplied by the organiser. Any new Presidential poll before expiry of the recorded term needs separate evidence of a lawful vacancy and fresh Returning Officer instructions. The portal blocks pre-term presidential polls rather than inventing a vacancy.
