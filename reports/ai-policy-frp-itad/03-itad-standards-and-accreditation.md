# 03 — ITAD Standards, Accreditation and Manufacturer Access

*Deliverable 5. Covers research workstreams 4 and 5.*

---

## 1. The central question for standards

Your research brief asks whether certification regimes **prohibit particular recovery practices** or merely **require documented, verified outcomes**.

The answer, consistently across all four frameworks examined, is the second: **they regulate evidence, not method.** No ITAD standard surveyed prohibits account-lock removal. They require that you can demonstrate, on audit, that data was sanitised to a defined standard and that the device's chain of custody is unbroken.

This is a materially favourable finding, and it is the strongest technical-legitimacy argument available to you. It also means the standards do not *authorise* unlocking — they are silent, and silence here is neutrality rather than permission.

---

## 2. R2v3

Source: <https://sustainableelectronics.org/r2/>; overview deck: <https://www.pjr.com/downloads/webinar_slides/2.8.2021_R2-V3-Overview.pdf>

- Successor to R2:2013, maintained by SERI (Sustainable Electronics Recycling International).
- Requires documented data sanitisation consistent with **NIST SP 800-88**, per-device records, and a documented downstream vendor programme.
- Introduces equipment categorisation (functioning product categories, e.g. F5 "refurbished") and focus material requirements.
- **Outcome-based**: the standard asks what you did and what evidence you hold; it does not prescribe or prohibit particular technical procedures. **[V]**

**Assessment.** R2v3 does not stand between you and account-locked devices. It stands between you and *undocumented* processing of them. **[I]**

---

## 3. e-Stewards

Source: <https://e-stewards.org/>

- Requires chain of custody, on-site destruction records with witness logs or video, and prohibits export of e-waste to developing countries.
- Data sanitisation requirements are again evidence-and-outcome oriented.
- Strong on downstream accountability, weak on method prescription. **[V/R]**

---

## 4. ADISA

Sources: <https://adisacertification.com/adisa-itad-essentials-standard/>; <https://adisa.global/wp-content/uploads/2020/06/ADISA-Welcome-Brochure_2020.pdf>

- ADISA runs an **ITAD Essentials Standard** and a separate asset-recovery standard, focused on risk management and process validation for ITAD providers.
- Explicitly covers the Asia-Pacific and Australian markets.
- Certifications validate the quality of an ITAD service or a sanitisation tool. **[V]**

**Assessment.** ADISA is the most relevant certification for a small Australian ITAD operator, being process- and risk-based rather than tied to a large corporate supply chain. **[I]**

---

## 5. NIST SP 800-88 Rev 1

Source: <https://www.nist.gov/publications/guidelines-media-sanitization-1>

Defines **Clear**, **Purge** and **Destroy** as sanitisation categories, with decision guidance tied to data confidentiality and media type. It is the reference standard that R2v3, e-Stewards and auditors invoke. **[V]**

**Relevance to FRP.** A device that cannot be unlocked generally cannot be sanitised to *Purge* with verification, because you cannot run a verified wipe or confirm the state. This is precisely why account-locked devices default to the **Destroy** path in professional practice — not because unlocking is forbidden, but because the evidence trail for reuse cannot be completed without it. **[I]**

**This is the strongest technical statement in the report**, and it is the one to bring to a provider: *unlocking is the precondition for a verified sanitisation, which is a legal obligation under APP 11, not a security violation.*

---

## 6. What professional refurbishers actually require

Across the standards and published practice, the recurring evidence set is:

| Control | Purpose | Typical proof |
|---|---|---|
| Business identity | Who is accountable | ABN, registration, insurance |
| Chain of custody | Unbroken control | Transfer records, courier logs |
| Title / ownership transfer | Lawful authority to process | Signed donor declaration, invoice |
| Stolen-device check | Exclude criminal property | IMEI check against national/industry databases |
| Sanitisation authorisation | Explicit mandate | Client instruction, disposal authorisation |
| Sanitisation evidence | Outcome proof | NIST 800-88 certificate, per-device record |
| Technician accountability | Deterrence | Named operators, access logs |
| Audit logging | Retrospective verification | Immutable logs, witness records |

**Observation.** This list is exactly the design of a credible professional access framework. Nothing on it requires a manufacturer. Everything on it is something a small operator can implement. That is the substance of section 7 (framework) and it should be your advocacy position. **[I]**

---

## 7. Manufacturer accreditation programmes

### 7.1 Huawei and the Australian market — an evidence conflict

This is the area where I was previously wrong, so the evidence is set out in full.

**Claim A — Roadhound is Huawei's Australian authorised repairer.**
Multiple independent Whirlpool forum posts describe Roadhound as "Huawei's only authorised repairer in Australia" and Huawei as having "a single approved repairer, Roadhound." These posts date from roughly the Mate 10 / Mate 20 era (2017–2018) and are **enthusiast forum evidence [R]**, not official.
Sources: <https://forums.whirlpool.net.au/thread/38k1vqm9?p=84#r1669>; <https://forums.whirlpool.net.au/thread/9lk6jxj3?p=11#r55039173>

**Claim B — Happytel is Huawei's authorised service centre network.**
iTWire reported in 2019 that Huawei had partnered with Happytel as an authorised Huawei service centre network, with 56 collection points and two service centres. **This is trade-press reporting [R]**, closer to primary than a forum but still secondary.
Source: <https://itwire.com/android/phones/launch-video-and-exec-interviews-happytel-and-huawei-s-customer-service-partnership>

**Assessment of the conflict [I].** These are not necessarily contradictory: a "service centre network with collection points" and a "repairer" describe different tiers, and the claims are from different years. What cannot be established from public sources is Huawei's *current* Australian arrangement, its eligibility criteria, or its fees. Your direct conversation with Roadhound's technical manager is therefore **the best available evidence**, and it is **[R] — a reported statement by an interested party**, not independently verified.

**What this means practically.** Treat "Roadhound is the only authorised Huawei option in Australia" as **your working assumption pending written confirmation**, not as an established fact. Ask them for it in writing — accreditation status, scope, and whether a Huawei partner ID exists. A genuine authorised centre can produce that; it is also the evidence you would need for any provider access request.

### 7.2 Samsung

Reported requirements for authorised repair centre status include a commercial lease with 12+ months remaining, business registration and tax ID, professional liability insurance around the $1M mark, and secure storage for high-value inventory. **[R]** Source: <https://www.simplysolved.blog/become-samsung-authorized-repair-center>
Samsung's own Australian support directs customers to authorised service centres with proof of purchase for lock-related matters. **[V]** Source: <https://www.samsung.com/au/support/how-to-book-a-repair/>

**Barrier assessment.** Lease term, insurance floor and premises security are plausibly achievable for an established Dubbo business, but the insurance and premises requirements are the binding constraints for a home-based or shared-premises operator. **[I]**

### 7.3 Apple

Two distinct programmes matter, and conflating them is a common error:

- **Apple Authorised Service Provider (AASP)** — the full programme. The Australian application documentation requires a credit application, three years of financial statements, a business plan, and a cash deposit or bank guarantee. Also requires certified technicians and audited financial records. This is a **high barrier**, effectively excluding small and start-up operators. **[V]** Sources: <https://support.apple.com/en-au/aasp-program>; <https://www.apple.com/support/assets/docs/products/programs/aasp/aasp_application_au_2013.pdf>
- **Independent Repair Provider (IRP)** — a deliberately lower-barrier programme for independent repair businesses, with different (lighter) requirements. Availability and terms vary by country.

**Assessment [I].** Apple's IRP existence is important evidence for your advocacy: it demonstrates that a major manufacturer has already designed a tiered access model for small independents. It undercuts the claim that gated access is unavoidable. It also shows the model is *technically and commercially possible* — which is the whole argument in section 7.

### 7.4 Google and Motorola

Google operates authorised repair arrangements for Pixel hardware through partner networks; Motorola lists authorised repairers including, in Australia, **Roadhound Electronics (Cardiff NSW)** as a carry-in repair centre. **[R]** Source: Motorola Australia support repair-centre listing.

**Assessment.** Motorola's published listing of Roadhound is independently checkable and is the strongest single data point that Roadhound is a multi-brand authorised centre — which is consistent with, but does not prove, Huawei accreditation. **[I]**

### 7.5 Cross-brand summary

| Brand | Programme | Published barrier | Small/regional accessible? |
|---|---|---|---|
| Huawei | Authorised service network (opaque) | Unknown; reported as high | Reported no |
| Samsung | Authorised Service Centre | Lease, $1M insurance, premises | Marginal |
| Apple | AASP / IRP | AASP high; IRP lower | AASP no; IRP maybe |
| Motorola | Authorised repairer | Opaque | Via Roadhound |
| Google | Authorised partners | Opaque | Unclear |

**General finding.** Manufacturer programmes are **not designed for reuse-first ITAD**. They are designed for warranty repair. Their eligibility criteria (premises, insurance, volume, audited accounts, certified technicians) are proxies for warranty-service capability and have little to do with whether an operator can sanitise and refurbish responsibly. This is a genuine structural mismatch, and it is the strongest form of your advocacy argument — stronger than any claim about AI policy. **[I]**

---

## 8. Affordability comparison for Dubbo E-waste

Indicative, from published and reported requirements:

| Path | Direct cost | Indirect cost | Realistic for a small NSW operator |
|---|---|---|---|
| Roadhound per-device | $65/device, no volume break | Nil | Yes, but uneconomic at scale |
| Samsung ASC | Insurance ~$1M, lease, premises | Staff certification | Marginal |
| Apple AASP | Deposit/guarantee, 3 yrs financials, business plan | Audited accounts | No |
| Apple IRP | Lower | Technician certification | Possibly |
| R2v3 | Certification and audit fees | Process documentation | Yes, if volume justifies |
| ADISA Essentials | Certification fees | Process documentation | Yes — best fit |
| Do nothing / recycle | $0 | Lost reuse value | Yes |

**Conclusion.** For your scale, the **only affordable accredited path is standards certification (ADISA Essentials, then R2v3) plus MobileMuster for the non-reuseable stream.** Manufacturer accreditation is not a realistic near-term option for any brand, and the $65 per-device route is a per-unit commercial decision, not a strategic one.

---

## 9. What this section establishes

1. ITAD standards are **outcome-based** and do not prohibit unlocking. **[V]**
2. NIST 800-88 makes unlocking a **precondition** for verified sanitisation, which is a legal obligation. **[I]**
3. No manufacturer programme is designed for reuse-first ITAD; all are warranty-service proxies. **[I]**
4. Apple's IRP proves tiered access for small independents is possible. **[V]**
5. Public evidence on Huawei's Australian network is **contradictory and dated**; your manager conversation is the best available but remains a reported statement. **[R]**
6. The affordable route is **certification, not manufacturer accreditation.** **[I]**
