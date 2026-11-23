# Bill 2026-01 — Local Civic Governance and Simulated Public Order

**Status:** TABLED by the President. Notice running. Not adopted. Not law.
**Introduced by:** President Joshua Parris (Art V.2: "implements Assembly resolutions")
**Procedure:** Ordinary bill under Art IV.2 and Art IV.3 — simple majority of valid votes cast, quorum per standing orders.
**Depends on:** [Constitutional Amendment 2026-01](AMENDMENT_2026_01_LOCAL_SERVICES_AUTHORITY.md), which must be adopted first for clauses 5 and 6 to operate (Art III.3, Art XI).
**Versions:** v0.1, 2026-11-23.

> Nothing in this bill creates real police, court, taxing or planning authority. Australian and NSW law take precedence (Art X.1). The bill exists so that Parristan's internal civic rules can match the fictional institutions of the Repository Town game without ever altering real law or real local government.

## 1 — Purpose

To give Parristan's settlements a lawful internal civic form, and to define how Parristan may depict public-order services inside the Repository Town simulation. The problem it solves: Repository Town and real Narromine both have civic institutions (a council, a constabulary, a courthouse, a fire service), and Parristan's settlements currently have none at all. Parristan adapts to the wider world. The wider world does not adapt to Parristan.

## 2 — Interpretation

- **Settlement** means one of the twelve settlements in `simulation/worker.js` `SETTLEMENTS`.
- **Civic Association** means the volunteer body of members resident in, or associated with, a settlement.
- **Civic Service (Simulation)** means a fictional service that exists only as content in the Repository Town 3D game. It has no real-world existence.
- **Simulation output** means anything rendered, downloaded or displayed by the Repository Town game.

## 3 — Direction of adaptation (standing rule)

1. Parristan's internal rules adapt to Australian, NSW and local government law and to the host institutions of the places where members live.
2. No Parristan instrument may amend, override, replace or purport to amend Australian law, NSW law, a real local government area, or any real council.
3. Where Parristan's fiction depicts a settlement inside a real local government area, the real area is authoritative over real land, and Parristan's depiction is a game stage only (Art IX.1).

## 4 — Settlement Civic Associations

1. Members resident in or associated with a settlement may constitute a **Civic Association** by publishing a short charter: name, settlement, officers, meeting times, and the services it volunteers to run.
2. A Civic Association may hold a hall, run a market, a hall committee, a Country Women's-style branch, a bushfire brigade in the volunteer style of the NSW Rural Fire Service, and a postal agency acting for the Treasury.
3. A Civic Association is not a council, a shire, or a local government area. It has no power to make by-laws binding on anyone who is not a consenting member.
4. A Civic Association must publish its own ledger. The Treasurer rules in force apply to its money (see `gazette/2026/2026-014`).
5. Volunteer service in a Civic Association is not employment, and confers no accreditation recognised outside Parristan (Art X.2).

## 5 — Local service charges (requires Amendment 2026-01)

*This clause operates only if Constitutional Amendment 2026-01 is adopted (Art XI).*

1. A Civic Association may propose a **local service charge** for disclosed services: hall upkeep, lighting, water points, road grading within the settlement.
2. The charge is authorised only by (a) a decision of the Assembly recording the rate, purpose and duration, and (b) consent of the members affected, recorded individually. Art III.3 is satisfied only when both exist.
3. A charge is never a rate on land. No instrument may attach a charge to a parcel, a title, a dwelling or a person who has not consented (Art IX.1, Art X.2).
4. Every charge and every dollar spent is published, with totals, in the settlement ledger.

## 6 — Civic Service (Simulation)

*This clause operates only if Constitutional Amendment 2026-01 is adopted (Art XI).*

1. The Assembly may constitute a **Civic Service (Simulation)** for the Repository Town game, performing fictional public-order functions that mirror the fictional institutions already present in that game.
2. The Civic Service (Simulation) is defined by these limits, which no Assembly decision may relax:
   - it exists only as simulation output;
   - it has no power of arrest, detention, search, seizure, entry or identification over any real person or real place;
   - it may not fine, imprison or seize property in the real world, and its fictional outcomes bind nobody (Art VII.3);
   - any real incident is referred to NSW Police and other real authorities, whose authority is unaffected (Art X.1);
   - it must never be described as police, or as an accredited service, outside the game.
3. Disputes within the simulation are heard by a fictional settlement panel whose fictional decisions have no real effect, are appealable to the Ethics and Appeals Panel, and which may not impose fines, imprisonment or seizure in the real world (Art VII.3, Art VII.4).

## 7 — Settlement classification

1. For civic purposes the existing `kind` values acquire meaning, which they did not previously have:
   - **capital** — Founders Square: Civic Association plus the Assembly chamber.
   - **town** — Starhaven, Tealford, Goldmere, Westhaven, Rivermark: full Civic Association of at least five officers.
   - **village** — Dawnridge, Birchfield, Hearthbrook, Southridge, Lantern Point: Civic Association of at least three officers.
   - **port** — Bluewater: Civic Association with a wharf and river-landing remit. Waterborne freight is fictional; no real port, ramp or navigation status is claimed.
2. Classification changes nothing physical. It changes the minimum civic form each settlement publishes.

## 8 — First application: Tealford

1. Tealford (settlement id 2) is the first settlement to be given a governed 3D form in Repository Town.
2. Its Civic Association is chartered with: a Progress Association, a hall committee, a volunteer brigade, and a Treasury postal agency.
3. Tealford has no constabulary of its own under this bill. If the Assembly later adopts clause 6, Tealford becomes eligible for a Civic Service (Simulation) detachment on the same fictional footing as Lantern Point.

## 9 — Records, privacy and reporting

1. The Assembly must publish each adopted charter, each charge decision, and each Civic Association ledger.
2. No personal information beyond a member's chosen display name may appear in a published ledger (Art II.4, Art III.4).
3. Simulation output is never evidence of real activity, real membership or real office (Art VIII.2).

## 10 — Commencement

1. Clauses 1–4 and 7–9 commence on adoption.
2. Clauses 5 and 6 commence only on the effective date of Constitutional Amendment 2026-01.

## Voting record

| Field | Value |
|---|---|
| Tabled | 2026-11-23 |
| Notice | Running — 14 days minimum if the companion amendment proceeds (Art XI.2) |
| Quorum | Per standing orders (`gazette/2026/2026-009`) |
| Votes for / against / abstain | **Not yet taken** |
| Effective date | None — not adopted |

## Related

- [Constitutional Amendment 2026-01](AMENDMENT_2026_01_LOCAL_SERVICES_AUTHORITY.md) — the amendment this bill depends on
- [Gazette 2026-016](../gazette/2026/2026-016-local-civic-governance-tabled.md) — notice of tabling
- Repository Town game canon: `repository-town/docs/PARRISTAN_STAGE_AND_CIVIC_CANON.md` (JoshMemory)
- [LEGAL_STATUS.md](LEGAL_STATUS.md) — territory and sovereignty position, unchanged by this bill
