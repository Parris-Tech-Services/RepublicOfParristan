# Parristan Private Assembly — Voting service v1

**Privacy:** the public GitHub repository contains program code and documented rules, not member passwords, ballot data or private enrolment credentials. The application itself requires private authenticated access.

**Current implementation:** five pre-provisioned founder slots and a database; server-side authenticated motions, atomic one-vote-per-founder enforcement, officer workflow and independently checked aggregate tally. **No founders are yet activated and no ballots have been cast in this app.** New secret elections remain **locked** until the Returning Officer confirms the authorised method and a security/privacy review is completed. A deployed site or an existing user slot is not proof of an authenticated successful vote.

## Governing rules

- Constitution v0.1 Article IV: eligible adult member, one vote each; ordinary motions by a simple majority of valid votes.
- Founding Motion 4, Gazette 2026-009: written votes run for 48 hours, or may close once every member votes; quorum minimum **three voters**; majority of valid votes cast.
- Constitution Article XI: full text of an amendment available at least **14 days** before voting and a two-thirds majority of valid votes.
- Motion 2, Gazette 2026-007: Matthew Walker is independent Returning Officer. The initial timetable was superseded by [Motion 6](../../gazette/2026/2026-012-election-timetable-brought-forward.md).
- First-election rules remain a **draft**, rather than falsely being described as enacted law. A sole candidate faces a YES/NO confirmation. Multiple candidates need a majority or a separately approved runoff. Joshua Parris was confirmed as the first President, as recorded in [Gazette 2026-013](../../gazette/2026/2026-013-first-president-confirmed.md).
- Motion 3, Gazette 2026-008: Jane Carbunkle Secretary, Fred Carbunkle Treasurer and Glenn Peterson Registrar; Glenn is CDO and joint technical administrator with Joshua Parris.
- Motion 1, Gazette 2026-006: the encrypted Matrix room remains the official notice and voting channel until a replacement is adopted. The voting portal supplements rather than silently changes this procedure.

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
- The office roles, election timetable and constitutional amendment rules were taken from the actual published founding documents, but rules for future elections remain for the Returning Officer and Assembly to agree.
- Existing Gazette decisions are not replayed as ballots and no Presidency is automatically created.
- Do not enable real voting until the secure live service and all five founders' access have been verified with the responsible officers.

## Tests and operational controls

Node built-in test suite checks quorum, ordinary majority, amendment thresholds, amendment notice, early closure, first-election majority/runoff, vote windows and count consistency. GitHub Actions runs this on every change in this application. Deployment requires separate runtime verification (login, session, same-origin, admin controls, atomically rejected duplicate vote) before reporting operational success.

## Updated 19 November 2026 governance position

[Gazette 2026-012](../../gazette/2026/2026-012-election-timetable-brought-forward.md) replaced the original date ranges. The first presidential confirmation used an emailed YES/NO ballot under Motion 6, **not this application**. [Gazette 2026-013](../../gazette/2026/2026-013-first-president-confirmed.md) records Joshua Parris as first President for **19 November 2026 – 19 November 2028**, with a 5–0 confirmation (organiser-supplied record). No historical ballots or account actions have been inserted here.

[Gazette 2026-014](../../gazette/2026/2026-014-presidents-first-programme.md) established the President's first programme, Matrix debate/votes, official-email notices/correspondence, and future January 2027 symbol ballots. An Assembly resolution adopting use of this portal for official voting has not yet been evidenced; until then this portal is supplementary to the adopted Matrix/email process. Its platform can support written motion submissions once the five founders have activated accounts and the officers have confirmed its deployment, roll and operating method. Existing presidential terms are never silently reset.
