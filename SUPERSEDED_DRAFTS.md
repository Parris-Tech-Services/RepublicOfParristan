# SUPERSEDED — never published, never adopted

**Status:** design record only. Nothing in this branch was published, voted on, or adopted, and nothing downstream should cite it.

On **23 November 2026** the Assembly adopted the ordinary resolution **PA-2026-001** — *Parristan Civic Governance and Repository Town Integration* — recorded as [Gazette 2026-016](gazette/2026/2026-016-civic-governance-repository-town-integration.md) and in the [Decision Register](institutions/DECISION_REGISTER.md), with the proposed Article XIII published for consultation as [Gazette 2026-017](gazette/2026/2026-017-article-xiii-amendment-notice.md) and [`PROPOSED_AMENDMENT_2026_01_ARTICLE_XIII.md`](institutions/PROPOSED_AMENDMENT_2026_01_ARTICLE_XIII.md).

The drafts on this branch were written before that and are **superseded** by it:

| Draft here | Superseded by | Why it must not be used |
|---|---|---|
| `gazette/2026/2026-016-local-civic-governance-tabled.md` | `gazette/2026/2026-016-civic-governance-repository-town-integration.md` | **Gazette number 2026-016 is taken.** Two files numbered 2026-016 make `scripts/validate_gazette.py` fail with "Duplicate Gazette IDs" |
| `institutions/BILL_2026_01_LOCAL_CIVIC_GOVERNANCE.md` | `institutions/CIVIC_AND_SIMULATION_POLICY_2026-11-23.md` (PA-2026-001 clauses 4-6) | The adopted policy covers Civic Associations, the Civic Service (Simulation) and virtual-only finances, without this bill's charging machinery |
| `institutions/AMENDMENT_2026_01_LOCAL_SERVICES_AUTHORITY.md` | `institutions/PROPOSED_AMENDMENT_2026_01_ARTICLE_XIII.md`, **still not adopted** | It would have replaced Art III.3 and authorised local service charges. The Assembly's motion expressly does **not** authorise compulsory real-world taxation, land rates or new public-law enforcement, and proposed XIII.4 bars compulsory land charges outright. Using this draft would contradict PA-2026-001 clause 6 |

The **"Amendment 2026-01" number is also taken** by the published Article XIII proposal, so the filename here cannot be reused for a different amendment.

## If any element of these drafts is still wanted

1. Renumber to the next free Gazette ID - the last published is **2026-017**, so **2026-018** onwards.
2. Do not reuse "Amendment 2026-01"; the Article XIII proposal holds it.
3. Put it through the ordinary-motion process (Art IV.2-3: simple majority, quorum 3, 48-hour window closing early once all eligible members vote), and cite it as a fresh instrument rather than editing this branch into the record.
4. If it would touch Art III.3 or Art VII.3, it is a constitutional amendment: Art XI.1-2 requires full-text notice, at least 14 days, quorum and two-thirds of valid votes cast. No urgency lane exists.

## Merge safety

Merging this branch into `main` **breaks the published record**: `python3 scripts/validate_gazette.py` fails with duplicate Gazette IDs, a stale Markdown index and a stale homepage notice count. This branch is kept unpushed as a design record only.
