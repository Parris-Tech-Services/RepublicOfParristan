# Parristan implementation checklist — 19 November 2026

This batch supports the [national operations checklist](NATIONAL_OPERATIONS_TODO.md).

- [x] Audited open pull requests and ran the Gazette validator and eight registry tests. PR [#21](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/21) merged while this batch was underway. The open PR search returned zero.
- [x] Reconciled the [ratification return](docs/ASSEMBLY_RATIFICATION_RETURN_2026-11-19.md), [constitution](institutions/CONSTITUTION.md) and [election status](docs/FIRST_ELECTION_STATUS_2026-11-19.md) with [Motion 4](gazette/2026/2026-009-standing-procedures.md). The original founding notice time remains unrecorded.
- [x] Reviewed the merged [Returning Officer kit](operations/drafts/ELECTION_KIT.md) covering nominations, confidential voting, count and certification. The Returning Officer still needs to publish the notice and run the election.
- [x] Located the merged founder review drafts for [membership](operations/drafts/MEMBERSHIP_POLICY.md), [symbols](operations/drafts/SYMBOLS_SPEC_AND_REGISTER.md), [finance](operations/drafts/FINANCIAL_CONTROLS.md), [communications](operations/drafts/COMMS_PROPOSAL_TEMPLATE.md) and the [open-source pilot](operations/DIGITAL_PILOT_GUIDE.md). Adoption and provisioning remain with the founders.
- [x] Exercised the [public backup procedure](operations/BACKUP_AND_HANDOVER.md) in a temporary directory. The checksum passed, the bundle restored to commit `56e13bb`, and `git fsck --full` passed. Durable off-site storage and the private Enterprise backup are separate outstanding tasks.
- [ ] Publish and verify the public site. The Pages workflow is merged. The public URL still returned HTTP 404 on 19 November 2026. The [Pages publishing runbook](operations/PAGES_PUBLISHING.md) records the repository settings needed.

Founders and officers retain decisions, live membership and ballot custody, symbol adoption, spending and service approvals. External registrations, premises and recognition require the relevant parties.
