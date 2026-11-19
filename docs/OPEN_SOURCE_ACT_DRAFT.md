# Open Source Act — Draft Bill, Sovereign Systems Office and Hosting Decision (Phase 0)

**Republic of Parristan · 19 November 2026 · Status: the full Open Source Act remains a DRAFT bill. The founding Assembly unanimously adopted the open-source direction, activated the separately proposed OSPO charter, and appointed Glenn CDO by consent. No hosting site is confirmed.**

This is the Phase 0 (governance, week 1) package of the [Open-Source Digital Government Strategy](OPEN_SOURCE_DIGITAL_GOVERNMENT.md). It uses the status vocabulary in [Official Records](../operations/OFFICIAL_RECORDS.md): nothing here is **ADOPTED** or **IN FORCE** until a real decision exists with dated evidence. A GitHub merge of this file is a document edit, not a vote.

## Phase 0 checklist

- [ ] Assembly expressly adopts the **full text** of the Open Source Act (draft below). *The founding motion adopted an open-source strategy but did not expressly pass every section of this bill.*
- [x] Founding Assembly appointed **Glenn** as Chief Digital Officer by unanimous consent; Glenn accepted. See [minutes](FOUNDING_ASSEMBLY_2026-11-19.md) and [activated OSPO charter](OSPO_CHARTER_2026-11-19.md).
- [ ] Confirm the hosting site (The Shed, with ForgeGrid as build/test coordinator). *Needs a hardware and connectivity check; see the decision record below.*

## Part 1 — Open Source Act (draft)

**Short title.** Open Source Act 2026.

**1. Purpose.** To keep the Republic's administration under its own control: auditable software, portable data and no forced dependence on a single vendor.

**2. Definitions.**
- *National system* means software, services or infrastructure used to run the Republic's official business, records or public communications.
- *Open source software* means software released under a licence approved by the Open Source Initiative.
- *Open format* means a publicly documented, royalty-free file format, such as ODF for documents and spreadsheets, PDF/A for archives, and plain text, Markdown, CSV or JSON for data.
- *Office* means the Office of Sovereign Systems established under section 6.

**3. Open source by default.** National systems must use open source software. A system that is not open source may be used only under a recorded exemption (section 5).

**4. Open formats.** Official records must be created, stored and published in open formats. Every national system must be able to export its data in an open format, and the Office must test that export at least once a year.

**5. Exemptions.** The Office may grant a written exemption where no suitable open source option exists. Each exemption must state the reason, the alternatives considered, a migration or exit plan and an expiry date no later than 12 months after it is granted. Exemptions are listed in a public register. Private personal data is never published as part of that register.

**6. Contractors and suppliers.** A person who builds or operates a national system for the Republic must meet sections 3 and 4. Software written for the Republic under contract is released under an OSI-approved licence unless the Office records an exemption. No contract may prevent the Republic from exporting its own data.

**7. Security and privacy.** This Act does not authorise publishing membership, identity, election or financial records. Those stay access-controlled. Open source is not a substitute for security: national systems must have multi-factor authentication, patching, encrypted backups and a tested restore.

**8. Existing systems.** Within 90 days of commencement, the Office publishes an inventory of national systems and a migration plan for any that do not comply.

**9. Review.** The Assembly reviews this Act within 12 months of commencement.

**10. No legal effect beyond the association.** This Act governs the Republic's own administration as a developing micronation. It does not create legal sovereignty, override Australian law or bind third parties.

**11. Commencement.** This Act commences on the date the Assembly records its adoption, or a later date the Assembly specifies.

## Part 2 — Office of Sovereign Systems (charter draft)

**Role.** The Office runs the Republic's open source strategy, keeps the service inventory, grants and tracks exemptions, and reports on digital operations.

**Head.** Chief Digital Officer (CDO). **Founding holder: Glenn Peterson**, appointed by the unanimous founding Assembly on 19 November 2026; he accepted. This is an association administrative office, **not an elected presidency**. The activated charter is [recorded here](OSPO_CHARTER_2026-11-19.md).

**Alternate administrator.** A second named person holds recovery access and can run every critical service, so no service depends on one administrator.

**Duties.**
1. Maintain the service inventory: what each system is, its operator, licence, data location, backup and exit path.
2. Run the pilots described in the strategy (A: everyday office, B: collaboration, C: mature administration) and record the results.
3. Grant, publish and expire exemptions under section 5 of the Act.
4. Test export and restore at least once a year and publish a pass/fail summary.
5. Report to the Assembly at least annually: services in use, costs, incidents, exemptions and migration progress.

**Limits.** The Office does not collect member data in public repositories and does not enrol employer, client or school systems. It cannot spend money or sign contracts beyond limits the Assembly sets.

## Part 3 — Hosting site decision record

**Status:** options only. No site is confirmed.

| Option | What it provides | Open questions |
| --- | --- | --- |
| The Shed (physical site) | Power, network and a place for hardware under the founders' control | Hardware available, connectivity and uptime, power backup, physical security, whether the site is suitable for a continuous service |
| ForgeGrid coordinator | Distributes build and test jobs across LAN machines | It is a build/test coordinator, not a host for email, files or meetings, so it complements a hosting stack rather than replacing one |
| Hosted open source services (for example a managed Nextcloud or mail provider) | Less maintenance for a five-person group | Cost, data location, vendor exit and whether it meets the Act's export requirement |

**Proposed approach (not decided):** use The Shed for hardware and ForgeGrid for builds and automated tests, run a small pilot of the services in the strategy's blueprint, and compare self-hosting against a managed service on cost, workload and recovery before committing. The decision should record the hardware list, backup location off-site, who holds admin and recovery access, and the restore test result.

**Decision evidence needed before this is marked complete:** a named site, a service inventory, a tested backup restore and an alternate administrator.

## Next steps

1. The open-source strategic direction and OSPO charter are approved. Founders can still review this **full bill** as a separate legislative proposal.
2. Bring the **full Act** to a properly noticed Assembly session if the founders want to enact its remaining provisions; record its own vote, and reconcile any presidential-appointment clause with the Assembly's founding CDO appointment.
3. Glenn's acceptance is recorded. Separately evaluate The Shed or any other authorised hosting site before declaring it in use.
