# 02 — Australian Legal and Regulatory Assessment

*Deliverable 4. Covers research workstream 3.*

> **Not legal advice.** This is an analysis of statute and published guidance. The criminal-provenance questions in §6 carry real exposure and warrant a solicitor's opinion before you scale the donation intake.

---

## 1. The separation that matters

Three frameworks are routinely confused. They are independent:

| Framework | Source | Governs | Consequence of breach |
|---|---|---|---|
| **Law** | Commonwealth and NSW statutes | What you may do | Criminal/civil liability |
| **Manufacturer agreement** | Contract, accreditation terms | What tools and credentials you may use | Loss of accreditation, warranty, access |
| **AI provider policy** | Private terms | What an AI will help with | Refusal, account action |

Something can be **lawful but not manufacturer-authorised** (independent repair). It can be **manufacturer-authorised but unlawful** (an authorised agent handling stolen goods). And it can be **lawful and authorised but still refused by an AI** — which is precisely the situation you are in.

The remainder of this section addresses law only.

---

## 2. Ownership and title in donated devices

### 2.1 When title passes [V]

A gift is a transfer of property made without consideration. For a donation to transfer good title, the donor must have had title to give. The common-law principle *nemo dat quod non habet* — no one can give what they do not have — means a stolen device remains the property of its true owner regardless of how many hands it passes through.

**Implication for you.** Donation paperwork does not create title; it evidences the donor's representation that they had it. Your protection is documentary, and it is the only protection available.

### 2.2 Why this is the actual legal risk [I]

The criminal exposure in your case study is **not** in unlocking a phone. It is in receiving and processing goods whose provenance you cannot evidence. The unlock is the visible act; provenance is the liability. This distinction is routinely lost in these debates and it is the one that should drive your operating model.

---

## 3. Computer access offences

### 3.1 Commonwealth — Criminal Code Act 1995, Part 10.7 [V]

Source: <https://www.legislation.gov.au/C2004A04868/latest>

Relevant provisions include:

- **s 476.1** — definitions. Access to data is *unauthorised* where the person is not entitled to cause that access. This is the hinge on which everything turns.
- **s 477.1** — unauthorised access to, or modification of, data with intent to commit a serious offence.
- **s 478.1** — unauthorised access to, or modification of, restricted data; penalty 2 years. "Restricted data" means data held in a computer to which access is restricted by an access control system associated with a function of the computer.

**Analysis.** An FRP lock is an access control system, and the data behind it is restricted data. The offence element is that access be **unauthorised**, which s 476.1 defines by entitlement. If you lawfully own the handset and are entitled to control its configuration, you are entitled to cause the access — the element fails. This is the straightforward owner's case, and it is why unlocking your own device is not a computer offence. **[I — legal analysis, not a judicial holding]**

The same analysis is why the position is weak for a device you cannot show title to: without entitlement, you are in the offence's target zone.

### 3.2 NSW — Crimes Act 1900 [V]

Source: <https://legislation.nsw.gov.au/view/html/inforce/current/act-1900-040>

- **s 308C** — unauthorised access, modification or impairment with intent to commit a serious indictable offence; maximum 10 years.
- **s 308H** — unauthorised access to, or modification of, restricted data; summary offence; 2 years.

Same structure: the offence turns on "unauthorised," and "unauthorised" turns on entitlement. The NSW provisions are the ones that would apply to a Dubbo operation, since the conduct occurs in NSW and the devices are physically there.

**Note on seriousness.** s 308C's 10-year maximum is reserved for access with intent to commit a serious indictable offence. There is no plausible version of legitimate refurbishment that engages it. The realistic exposure, if any, is the summary provision under s 308H — and only on a no-title scenario.

---

## 4. Copyright and technological protection measures — the genuine uncertainty

### 4.1 The provisions [V]

Source: <https://www.austlii.edu.au/cgi-bin/viewdoc/au/legis/cth/consol_act/ca1968133/s116an.html>

- **s 116AN** — circumventing an **access control technological protection measure** (TPM) is actionable at the suit of the copyright owner.
- **s 116AO / s 116AP** — exceptions for permitted purposes, and a separate prohibition on providing circumvention *services*.
- Criminal offences attach to commercial-scale circumvention services, not to a person acting on their own device.

### 4.2 Does FRP engage this? [I]

The chain of reasoning required for s 116AN to bite is: (a) there is a copyright work; (b) a TPM protects access to that work; (c) you circumvent it.

FRP protects access to a **Google account and device configuration**, not to a copyright work. The lock's function is anti-theft and account security. It is a device access control, not a copyright access control. On the natural reading, s 116AN does not reach it.

**But** the provision is broadly drafted, and there is no Australian authority on FRP specifically. A manufacturer could argue that the device's bundled software constitutes copyright material and the lock controls access to it. That argument is weak but not frivolous.

**Practical consequence.** Low risk, non-zero, and higher for a *service provider* than for an owner: s 116AP targets providing circumvention services, which is the shape of a commercial refurbishment offering. This is the one legal vector that gets worse, not better, as you professionalise. Worth a solicitor's five-minute view before you offer unlocking as a service to third parties.

---

## 5. Right to repair

### 5.1 The Productivity Commission's finding [V]

Source: <https://www.pc.gov.au/inquiries-and-research/repair/report/>

The Commission's 2021 Right to Repair inquiry found that Australia's consumer guarantees already provide meaningful repair rights, that the principal barriers are practical (parts, information, software locks) rather than legal, and recommended targeted interventions including repairability labelling and product stewardship reform.

**Analysis.** Australian law does not create a general statutory "right to repair" for commercial refurbishers, but it equally does **not** require manufacturer authorisation to service owned goods. Independent repair is lawful. The Commission's work is the authoritative Australian statement that manufacturer control of repair is a competition and consumer problem, not a settled entitlement.

### 5.2 The ACL and "authorised repairer" claims [V]

The Australian Consumer Law prohibits misleading conduct about consumer rights (s 18) and provides consumer guarantees that cannot be excluded. The ACCC has taken enforcement action against manufacturers for representing that repairs must be done by authorised agents or that third-party repair voids rights. Those representations are frequently unlawful.

**Consequence for your advocacy.** "Only an authorised service centre may lawfully unlock this device" is a claim that should be tested. It is often a commercial statement wearing a legal costume. Whether it is *accurate* for Huawei specifically depends on the contract and the technical access, not on law.

---

## 6. Second-hand goods, provenance and stolen property — the live exposure

### 6.1 NSW licensing and records [V]

Sources: <https://apps.police.nsw.gov.au/weblink/pdfdocs/Self_Audit_Leaflet_V1.pdf>; <https://legislation.nsw.gov.au/file/Pawnbrokers%20and%20Second-hand%20Dealers%20Regulation%202020.pdf>

Mobile phones are prescribed second-hand goods in NSW. A business dealing in them falls within the Pawnbrokers and Second-hand Dealers Act 1996 and its regulations, which require identity evidence for acquisitions and retention of transaction records.

**Corroborating detail.** The Regulation contains **company-specific exemptions** from those identity and record-keeping duties for named ITAD firms (e.g. Verser Technology Lifecycles, IBM Australia). Two readings are available: (a) the obligations are onerous enough that major operators seek relief; (b) they are standard and the relief is a red-tape concession. Either way, the existence of named exemptions proves the obligations are real and that the compliance path for a serious operator is **comply or seek exemption**.

**Action for you.** Establish your position with NSW Police or Service NSW before scaling donation intake. This is a licensing question with a clear administrative answer, unlike everything else in this report.

### 6.2 Receiving stolen goods [V]

NSW Crimes Act 1900 s 188 makes it an offence to receive property where the person knows or **suspects** it was stolen. The "suspicion" standard matters: a locked, undocumented handset in a donated box is a fact pattern that can support suspicion. The defence is documented enquiry and provenance.

**This is the paragraph to act on.** Your legal exposure is concentrated here, not in the unlock. A donor declaration, an ABN, a signed statement of title, and an IMEI log are the mitigating controls. Without them, the number of phones unlocked is irrelevant to the risk.

---

## 7. Data protection and sanitisation

- **Privacy Act 1988** — APP 11 requires reasonable steps to secure personal information and to destroy or de-identify it when no longer needed. A refurbisher holding devices with residual personal data from previous owners is holding personal information. [V]
- **Notifiable Data Breaches scheme** — applies to eligible data breaches; relevant if a device with residual data is resold. [V]
- **NIST SP 800-88 Rev 1** — the accepted technical standard for sanitisation (Clear / Purge / Destroy). Not law, but the benchmark regulators and auditors apply. <https://www.nist.gov/publications/guidelines-media-sanitization-1> [V]

**Implication.** There is a positive legal duty to sanitise, and FRP removal is sometimes the *enabling step* for sanitisation — you cannot factory-reset and verify a device you cannot unlock. That is a genuinely important point: in the ITAD frame, unlocking is upstream of a **privacy obligation**, not downstream of a security violation. It is the strongest normative argument in this entire report.

---

## 8. Waste and stewardship

- **Product Stewardship Act 2011** — enables co-regulatory and voluntary schemes. [V]
- **National Television and Computer Recycling Scheme (NTCRS)** — covers televisions and computers; **mobile phones are not a covered product**. [V]
- **MobileMuster** — the voluntary industry scheme for mobile phones, free to consumers and businesses at volume, and it recycles rather than resells. <https://www.mobilemuster.com.au/frequently-asked-questions/> [V]

**Implication.** There is no legislated producer obligation for phones in Australia. MobileMuster is the compliant disposal channel and it costs nothing, which means the $65 recovery fee is a **reuse** cost, never a **disposal** cost. That distinction should govern how you price the two streams.

---

## 9. Conclusion on lawfulness

| Question | Answer | Confidence |
|---|---|---|
| Is removing an account lock from a device you lawfully own a criminal offence in NSW? | **No** — the computer offences require "unauthorised" access, and an owner is entitled. | High [I] |
| Does Australian law require manufacturer authorisation to refurbish? | **No.** | High [V] |
| Is there a copyright TPM risk? | **Low but not zero**, higher for a service provider than an owner. Unresolved by authority. | Medium [I] |
| What is the real legal risk? | **Provenance.** Receiving goods you cannot show title to, and failing to sanitise. | High [V] |
| Is manufacturer policy law? | **No.** | Certain [V] |

**The legal answer is more permissive than the AI refusals assume, and the operational answer is more demanding than the legal one.** Both are true simultaneously. That asymmetry is the central practical finding of this report.
