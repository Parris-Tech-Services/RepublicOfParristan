# Open-Source Digital Government Strategy — Adopted Strategic Direction v0.1

**Republic of Parristan · 19 November 2026 · Status: open-source strategic direction unanimously adopted by the founding assembly. Individual system rollouts remain proposed or unverified.**

## Purpose

Build a small, useful, secure and independently maintainable digital administration. Parristan will **learn from the French National Gendarmerie's long-running Linux/GendBuntu deployment** and **Schleswig-Holstein's integrated programme to replace proprietary office, email, cloud, identity and desktop systems**. These are models to adapt, not products or policies endorsed by those governments.

Here, **digital sovereignty** means practical control over data, configuration, formats, backups, infrastructure and vendor exit. It does **not** imply legal sovereignty, governmental recognition or exemption from Australian law. The Assembly unanimously adopted the strategic direction on 19 November 2026, per the [founding minutes](FOUNDING_ASSEMBLY_2026-11-19.md); this does not mean all equipment, services or bills are approved, funded or deployed.

## Design principles

1. **Open source and open standards by default.** Prefer software with auditable source, sustainable licensing and standard data exports; record any necessary proprietary exceptions.
2. **Start small, migrate in stages.** A five-person initiative does not need a custom Linux distribution or an enterprise data centre. Pilot, document, train, then expand.
3. **User-first services.** Accessibility, ease of use, support and reliable everyday workflows matter more than symbolic technology choices.
4. **Security and privacy by design.** Least privilege, multi-factor authentication, encrypted backups, patch management, data minimisation, incident response and consent-based membership records.
5. **Exit without lock-in.** Test export and restoration to independently operated systems. Use ODF, PDF/A where appropriate, interoperable mail/calendar protocols and documented APIs.
6. **Transparency without exposing people.** Open-source code and public decisions where suitable; private membership, identity, contact, election and financial records remain access-controlled.
7. **Cost and maintainability.** Record total operating cost, volunteer workload, support needs, uptime, accessibility and migration risk before making commitments.
8. **Evidence over claims.** A selected product is not a deployed service; a demonstration is not a secure production system.

For the exact **publicly evidenced products**, with completed/ongoing distinctions, use the [reference software stack matrix](REFERENCE_STACK_MATRIX.md). For the Windows developer workstation see the [Qwen + Pi quickstart](WINDOWS_QWEN_DEVELOPMENT.md).

## Reference models

| Reference | Transferable lesson | How Parristan will apply it |
| --- | --- | --- |
| French National Gendarmerie (GendBuntu) | Standardised Linux workstations, open office tools, staged adoption and internal operational know-how | Start with one reproducible Linux workstation/VM image, common applications and an onboarding/support guide |
| Schleswig-Holstein (Germany) | Plan the **whole** workplace: documents, mail, groupware, cloud, conferencing, identity, specialist applications and operating system | Maintain a service inventory and migrate interoperable workflows as a coordinated programme, not one app at a time |

Further reading: [European Commission Open Source Observatory on GendBuntu](https://interoperable-europe.ec.europa.eu/collection/open-source-observatory-osor/document/towards-freedom-operating-system-french-gendarmerie-goes-ubuntu); [French National Assembly 2026 report](https://www.assemblee-nationale.fr/dyn/opendata/RAPPANR5L17B3054-t1.html); [Schleswig-Holstein's official digital workplace programme](https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/I/Presse/PI/2024/CdS/240403_cds_it-arbeitsplatz.html).

## Proposed technology blueprint — none of these pilots is claimed as operational

| Capability | Preferred evaluation path | First practical deliverable |
| --- | --- | --- |
| Desktop operating system | Ubuntu LTS or Debian; choose on hardware compatibility, security updates and support | Test one pilot device/VM, document installation, rollback and accessibility |
| Documents | LibreOffice, ODF by default; PDF for public releases | Publish a shareable template and confirm export/import compatibility |
| Email and calendars | Thunderbird with standards-based hosted IMAP/SMTP and calendar initially; assess Open-Xchange if scale justifies it | Set up role-based mail and test mailbox/calendar export and restore |
| Files and collaboration | Nextcloud with scoped folders and access controls | Small non-sensitive pilot, sync, sharing, backup and restore tests |
| Meetings | Jitsi Meet or OpenTalk after accessibility and operational review | Hold a trial founding-committee meeting with an alternative dial-in or simple fallback |
| Identity | MFA from day one; assess authentik/Keycloak or Univention Nubus only if central identity management becomes necessary | Document admin access and recovery ownership without placing secrets in Git |
| Website and Gazette | Keep the existing static public GitHub Pages-compatible site; evaluate portable static hosting later | Publish accurate policy proposals and link to the public decision register |
| Source and issue tracking | Existing GitHub repositories for now; assess Forgejo/Gitea for later independent hosting | Make export/mirroring possible; retain dated, reviewable changes |
| Infrastructure and backups | Reproducible configuration (e.g. Ansible), encrypted backups (e.g. restic), documented restores | Back up a pilot service, restore to a different environment, record results |
| Public records and data | Markdown/open formats; PostgreSQL only if a real application needs it | Public minutes/decisions, private member records stored separately |

**Not a procurement order:** individual choices require pilot results, budget, licence review, privacy/security checks and appropriate approval. Public websites must not imply that any service exists before a verified live deployment.

## Implementation sequence and acceptance gates

### Pilot A — everyday office (first 30 days)

- [ ] Inventory existing documents, domains, applications and data flows privately.
- [ ] Test a Linux desktop or VM with LibreOffice, browser, Thunderbird and video calls.
- [ ] Produce a workstation setup guide and train a second person to reproduce it.
- [ ] Exchange ODF/PDF documents with another system without losing essential content.
- [ ] Record known blockers, operating costs and rollback plan.

**Pass:** two people can perform routine document and meeting tasks, with tested recovery and no sensitive data in public repositories.

### Pilot B — collaboration (30–60 days, only if needed)

- [ ] Evaluate a small Nextcloud workspace and privacy-respecting conferencing.
- [ ] Define roles, MFA, offboarding, maintenance ownership and service-level expectations.
- [ ] Restore an encrypted backup to a clean environment and document the procedure.
- [ ] Assess whether a hosted service is more sustainable than self-hosting for current membership.

**Pass:** approved members can collaborate, revoke access and recover data without relying on one administrator.

### Pilot C — mature administration (60–90+ days)

- [ ] Decide whether Open-Xchange, central SSO, a managed Linux image or independent code hosting is justified.
- [ ] Create a tested software and configuration inventory, patch cadence and incident-response runbook.
- [ ] Audit accessibility, open-format interoperability, privacy, recurring costs and exit capability.
- [ ] Propose detailed implementation regulations and any separate Open Source Act bill for proper Assembly consideration; the open-source strategic direction is already adopted.

**Pass:** every critical service has a named operator, alternate administrator, export path, backup/restore evidence and a documented proprietary exception if applicable.

## Governance boundaries

- Work on personally controlled or expressly authorised infrastructure only. Do not enrol employer, client or school systems.
- Do not collect passports, government identity documents, home addresses or sensitive member data in GitHub repositories, public forms or screenshots.
- No binding procurement, office appointment or policy enactment arises from a GitHub commit.
- Publish updates as **proposal**, **pilot**, **approved** or **operational (verified)** with evidence and dates.
- Maintain a succession plan; the Republic's records and services must survive one person's departure.

## Phase 0 — governance draft

The [Open Source Act bill](OPEN_SOURCE_ACT_DRAFT.md) remains a draft, but the founding Assembly activated the [OSPO charter](OSPO_CHARTER_2026-11-19.md) and appointed Glenn as CDO by unanimous consent. Hosting options still require a real technical and governance decision.

## Tracking

See [Founding Execution Checklist](FOUNDING_EXECUTION_CHECKLIST.md) for the civic priorities, first assembly, service pilots and measurable milestones. The strategic direction was adopted 19 November 2026; this document does **not** claim that the systems described above are already deployed.
