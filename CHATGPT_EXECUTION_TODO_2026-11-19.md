# ChatGPT execution backlog — 19 November 2026

**Scope:** Evidence-based engineering and publication work in the public `Parris-Tech-Services/RepublicOfParristan` repository. Prepared at the founding organiser's request. This is a **project task list, not an Assembly resolution**. It does not delegate civic powers, elect anyone, open services or create sovereignty.

**Working principle:** [x] only means the exact technical deliverable was verified, with a commit/PR/check or public URL. Preparing a page is not deploying it; a template is not an election notice; publishing records is not members approving a decision.

## A. Executable by ChatGPT from the connected repository — this work session

**Execution record:** 19 November 2026 — A01–A12 were implemented and checked; A13's live-publishing check was performed and identified an outstanding administrator-controlled Pages setting. **No live website deployment is claimed.** [Engineering PR #23](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/23) · [Gazette CI](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470637435) · [national operations CI](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470559516).


- [x] **A01 — Audit repo and open PRs.** Inventory the Gazette, election, operations, workflows and pending pull requests; preserve the original records.  
  **Outcome:** Audit completed: baseline had nine Gazette notices and eight FA decisions; open-PR query was empty before this work, and new changes were tracked in PRs #22 and #23.
- [x] **A02 — Publish this execution list.** Commit an actionable public scope and distinguish autonomous technical work from founder-controlled decisions.  
  **Outcome:** Published via [PR #22](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/22), merged as `150ffca`.
- [x] **A03 — Reconcile current officeholders and election dates.** Correct stale documents that still say the Returning Officer, Secretary, Treasurer or Registrar are unappointed, while keeping the Presidency vacant.  
  **Outcome:** Reconciled both governance docs and the election-operations roster in [PR #23](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/23), merged as `4927ad5`.
- [x] **A04 — Correct Gazette homepage counts.** Align displayed notices with the nine published, unique Gazette IDs and prevent discovery/index drift.  
  **Outcome:** Homepage now correctly lists nine notices; new Gazette index/list/count checks passed in [CI](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470559549).
- [x] **A05 — Add a read-only public administration dashboard.** Show accurate institutions, the presidential-election schedule, decisions, action owners and evidence links; no simulated actions represented as real.  
  **Outcome:** [Public administration dashboard](docs/administration.html) verified on `main` with all eight FA entries; a published source page is not proof of live hosting.
- [x] **A06 — Publish open-format public decision data.** A machine-readable JSON export of eight existing FA-2026-001…008 decisions, without room IDs, account details or ballots.  
  **Outcome:** [JSON export](docs/data/decisions.json) verified on `main` with eight entries and no private roll or ballots.
- [x] **A07 — Prepare election notices and records, not run an election.** Offer an editable Returning Officer checklist and notice template with unknown times and voting method left blank.  
  **Outcome:** Reviewed and corrected the existing [draft election kit](operations/drafts/ELECTION_KIT.md), removing assumed clock times and aligning the contested-vote threshold; only Matthew may issue the real notice.
- [x] **A08 — Add automated integrity tests.** Verify decision IDs, vote count handling (including exact versus reported unanimity), paths, dates, Gazette numbering and dashboard source-data consistency.  
  **Outcome:** Public-data validator and standard-library tests passed [national operations CI](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470559516).
- [x] **A09 — Keep Actions focused.** Wire validation into existing GitHub checks with narrow path filters and no secrets, deployments or extra recurring runs.  
  **Outcome:** Path-filtered validation passed; GitHub Actions was not given any secrets, new deployment destination or recurring schedule.
- [x] **A10 — Update navigation and publishing notes.** Make the new dashboard, export and task register discoverable from the website and README.  
  **Outcome:** Verified links from homepage, public decisions page, status page, governance docs and README; Gazette link validation passed.
- [x] **A11 — Perform privacy and content-safety review.** Keep private member register, contact data, Matrix room identifiers and secret ballots out of the repository; no unsupported sovereignty or enactment claims.  
  **Outcome:** Reviewed changed public files and eight-record JSON for privacy and civic-status claims; no private membership data, email addresses or ballots were introduced.
- [x] **A12 — Run CI, review diff, merge and verify `main`.** Confirm the exact changed files, GitHub validation result, PR state and committed source.  
  **Outcome:** [PR #23](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/23) merged as `4927ad5`; [post-merge Gazette check](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470637435) passed.
- [x] **A13 — Check live GitHub Pages publication.** Verify actual public access if possible; otherwise report as unverified and leave hosting configuration to an authorised administrator.  
  **Outcome:** **CHECK COMPLETED; DEPLOYMENT BLOCKED.** [Pages workflow](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470637527) failed in `actions/configure-pages` with `Get Pages site failed: Not Found`; public URLs could not be verified. An authorised admin must enable **Settings → Pages → Source: GitHub Actions**. The token supplied to `configure-pages` cannot silently enable this via its `enablement` option.

## B. Other repository work ChatGPT can prepare in later changes

- Plain-language summaries of standing orders, Constitution v0.1 and adopted decisions
- Public evidence/provenance matrix with exact sourced dates, caveats and correction history
- Accessible, printable minutes, agendas, vote and election-return templates
- Public consultation forms using GitHub issues (not private applications or ballots)
- Open-source stack comparison, one-machine Linux/LibreOffice pilot guide, and test criteria
- Backup/restore runbooks, checksums, data-export format examples and handover pack
- Privacy notice drafts, threat model, retention policy proposal and role-based access design
- Open-format $0 ledger **template**, budget proposal and dual-approval procedure
- Citizenship software *demo* and tests without real personal information
- Static symbol consultation gallery and licence/attribution review
- Domain/email/communications options research and procurement-neutral recommendation
- Website accessibility, mobile layout, broken-link and release verification improvements
- PR review, deduplication and safe merge/close workflows with evidence
- Future public status summaries once accurate records and permission are supplied

These preparations remain proposals or software until the authorised people perform real actions.

## C. Requires founder, officer, administrator or external action — NOT autonomous completion

- **Matthew (Returning Officer):** publish the actual nomination notice/method and precise times; check the confidential roll, administer fair secret ballots and certify the 28 November–1 December poll
- **All eligible voters:** nominate and vote; a candidate statement or GitHub commit is not a ballot
- **Jane (Secretary):** arrange the first monthly meeting and obtain any full-Assembly minutes approval still required
- **Fred (Treasurer):** maintain a real ledger, seek an adopted budget and apply authorised financial controls; a public $0 template proves no accounts
- **Glenn (CDO/Registrar):** establish a protected private membership register with consent; propose permanent email/chat by 3 December; operate only systems he has agreed to administer
- **Josh and Glenn:** configure and verify joint administrative permissions on Matrix, the GitHub organisation and any actual domain; the vote alone does not change permissions
- **Repository administrator:** enable GitHub Pages if not already configured and approve any settings or billing changes
- **Founders/Assembly:** decide the final Open Source Act, mission and first-year goals, legal form, budget, symbols, membership policy, land use and public representation
- **External parties:** give venue/land permission, assess registration applications, recognise or decline relationships, and supply real infrastructure or contracts

**Status convention:** `verified complete`, `partially complete`, `blocked / external authority`, or `not attempted`. Retain old history; correct errors visibly, without rewriting enacted motions or leaking private evidence.
