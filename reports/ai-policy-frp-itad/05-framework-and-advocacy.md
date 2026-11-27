# 05 — Proposed Verified ITAD Access Framework and Advocacy Plan

*Deliverables 7, 8 and 9. Covers research workstreams 7 and 8.*

---

## 1. Why a framework, and why it will be hard

The blocker identified throughout this report is **verifiable provenance at the point of request**. Everything else — law, standards, manufacturer contracts — is either settled in your favour or irrelevant to the AI question.

A provider cannot currently distinguish three requests that look identical:

1. A certified ITAD with a signed donor declaration and an IMEI log.
2. A small repairer with a plausible story and no paperwork.
3. Someone with a stolen phone.

Any framework must separate (1) from (2) and (3) **without** requiring the provider to adjudicate property law. That is achievable in principle by making the credential external and auditable.

**The honest caveat up front:** the barrier to this framework existing is not technical and not principled. It is **commercial**. There is no meaningful market incentive for a provider to build an ITAD access tier, because the addressable population is small and the reputational risk is asymmetric. Recognition of that should temper expectations: this is a multi-year advocacy proposition, not a support ticket. **[I]**

---

## 2. Proposed framework

### 2.1 Design principle

Borrow the architecture that already works: **OpenAI's Trusted Access for Cyber**. Identity-verify the organisation once, attest purpose, restrict usage to approved workflows, log everything, and reserve the right to revoke. The same machinery serves ITAD if you substitute the credential.

**Do not** ask the provider to assess whether unlocking is lawful in your jurisdiction. Instead, have a recognised certification body attest to the controls, and let the provider accept that attestation as a trust anchor. This mirrors how financial institutions use auditors rather than adjudicating their own counterparties' solvency.

### 2.2 Tiers

| Tier | Credential | What is unlocked | Revocation trigger |
|---|---|---|---|
| **T0** Public | None | Existing behaviour: general advice, standards references, policy information | N/A |
| **T1** Verified operator | ABN + ASIC extract + public liability insurance + NSW second-hand dealer registration | Procedural guidance on sanitisation workflow, standards interpretation, triage economics | Lapse of registration; complaint |
| **T2** Attested provenance | T1 + ADISA Essentials or R2v3 certification + per-batch provenance pack (Tier 3 evidence below) | Device-specific recovery reasoning for named IMEIs, with the batch declared | Failed audit; provenance irregularity |
| **T3** Regulated partner | T2 + statutory instrument such as a police second-hand dealer audit history, or government contract | Bulk/automated processing assistance | Any adverse finding |

### 2.3 The provenance pack (the actual control)

This is the part that does the work, and it is entirely within your control to build now, before any provider agrees to anything:

1. **Donor declaration** — signed, identifying the donor, their ABN or ID, the devices, and a statement of title: that the donor owns the devices and has authority to transfer them.
2. **Transfer record** — date, quantity, models, IMEI/Serial list.
3. **Stolen-device check** — IMEI status check against available databases, with the result recorded.
4. **Sanitisation authorisation** — explicit instruction that data is to be erased, with the standard specified (NIST SP 800-88).
5. **Named technician** — the individual accountable for the batch.
6. **Audit log** — immutable record of devices touched, when, by whom, outcome.
7. **Sanitisation certificate** — per-device outcome record.

**Note what this is:** it is the standard ITAD evidence set from `03` §6, formalised. You would need most of it for R2v3 or ADISA anyway. Building it now is not speculative work — it is the accreditation groundwork you need regardless.

### 2.4 What each side must give up

- **Provider** gives up a small amount of discretion and takes on a modest verification cost. It retains revocation authority and defines the usage envelope.
- **Operator** gives up anonymity and accepts audit. In exchange it gets deterministic, non-arbitrary treatment instead of per-session refusal roulette.

### 2.5 What this framework deliberately does not do

It does not tell anyone *how* to defeat an account lock. Its entire function is to decide **whether** a request is eligible. That separation is what makes it a governance proposal rather than an operational one, and it is the reason it can be put to a provider without asking them to compromise a control.

---

## 3. Would it actually work? Honest assessment

**In favour [I]:**

- It reuses a proven pattern (GTAC, Apple IRP).
- The credential is external and auditable, so the provider avoids becoming a property-law tribunal.
- The evidence set is already required by R2v3/ADISA — no new burden in substance.
- It distinguishes the three request types in §1.
- It gives providers a defensible position: *"we serve verified ITAD operators under policy X"* is easier to defend than *"we decide case by case."*

**Against [I]:**

- **Attestation is forgeable.** A determined bad actor can produce plausible paperwork. This is true of GTAC too, and providers accept identity-based risk; but it is a real limitation, not a solved problem.
- **Volume is tiny.** A handful of Australian ITADs is not a market. Without a consortium (industry body + several providers + a certification body), no provider will build it.
- **Liability transfer.** A provider that approves a process and a device turns out to be stolen has taken on reputational exposure it currently avoids by refusing. The framework must therefore place the liability on the operator, contractually and explicitly.
- **Precedent risk.** An "ITAD tier" invites adjacent claims (repair shops, resellers, hobbyists). Providers will worry about scope creep.

**Verdict.** The framework is *coherent and buildable*, and it would *plausibly* distinguish legitimate from illegitimate requests. Whether it is *commercially* achievable in the next few years is doubtful for a single small operator. It becomes realistic only as a consortium proposition.

---

## 4. Draft professional access request to OpenAI

> *Adapt the bracketed fields. Send to OpenAI's policy/trust contact channel; note that a response is not guaranteed.*

---

**Subject:** Policy review request — IT asset disposition and device data-sanitisation use case

To the Policy and Trust teams,

I write regarding a use case that I believe falls outside your published Usage Policies but is currently treated as though it falls inside them, and I am requesting a policy review.

**Who we are.** Dubbo E-waste is a reuse-first IT asset disposition (ITAD) operator based in Dubbo, NSW, Australia. We receive donated and end-of-life devices, sanitise them, and either refurbish for reuse or route them to certified recycling.

**The use case.** Devices received with a residual Factory Reset Protection (FRP) lock cannot complete a verified data sanitisation to NIST SP 800-88, because the device state cannot be reached. Under the Australian Privacy Act 1988 (APP 11) we have an obligation to destroy or de-identify personal information we hold. Unlocking the device is therefore upstream of a privacy obligation, not downstream of a security violation.

**What we are not asking for.** We are not asking for, and would not use, instructions for obtaining access to another person's account or data. We are not asking you to determine title. We are asking whether a documented, auditable operator can be treated differently from an anonymous requester.

**The published policy position, as we read it.** We have reviewed your Usage Policies and Model Spec. Neither names device refurbishment, FRP, or ITAD. The security clauses turn on "unauthorised" access, which is a question of the operator's entitlement — a matter we can evidence but you cannot verify per-request. We note that Anthropic's guidance refers to access "without authorization," and that your Trusted Access for Cyber programme already differentiates access on verified identity and approved workflows. That is the model we would like to see extended.

**What we can provide.** We are prepared to submit, for verification: ABN and ASIC registration; public liability insurance; NSW second-hand dealer registration; ADISA or R2v3 certification (in progress); per-batch donor declarations and title attestations; IMEI lists with stolen-device check results; named technician accountability; and immutable audit logs. We are willing to accept contractual liability for provenance and to submit to audit.

**What we are asking for.** A written view on whether (a) ITAD sanitisation is within scope of permitted use when accompanied by documented provenance, and (b) whether a verified-operator tier is under consideration, or could be piloted with a small number of certified Australian operators.

If the answer is that this is out of scope, a clear written statement to that effect would also be valuable, because it would let us stop pursuing an unavailable path and document the constraint for our own governance and for industry advocacy.

Yours faithfully,
[Name], Dubbo E-waste
[ABN] · [Contact]

---

## 5. Prioritised action plan for Dubbo E-waste

Ordered by cost-effectiveness, not by ambition. Everything in Phase 1 is free and delivers value even if no provider ever responds.

### Phase 1 — This week, zero cost, immediate risk reduction

1. **Build the provenance pack** (§2.3). Donor declaration template, transfer record, IMEI log, stolen-check result, named technician, sanitisation record. This is your legal protection *and* your future access credential. Highest-value action in the entire plan.
2. **Get Roadhound's position in writing.** Accreditation status, scope, brand coverage, whether the fee is refundable on failure, and whether they will accept a batch with a donated provenance declaration instead of individual receipts.
3. **Confirm your NSW second-hand dealer obligations** with Service NSW / NSW Police. Administrative question with a definite answer.
4. **Adopt the triage discipline.** Unlock only units that clear margin; recycle the rest via MobileMuster at zero cost. Stop treating a donated box as homogeneous inventory.

### Phase 2 — Next quarter, low cost

5. **Apply for ADISA ITAD Essentials.** Best-fit certification for your scale and the credential a provider framework would actually accept.
6. **Send the access request** (§4) to OpenAI, and an adapted version to Anthropic. Expect no substantive reply; the value is the documented record and the possibility of a policy-adjacent response.
7. **Join the industry conversation.** AMTA (which operates MobileMuster) and the Australian repair/right-to-repair advocacy community are the natural venues. Verify current names and membership costs before committing.
8. **Lodge a submission** to any active Australian circular-economy or product-stewardship consultation arguing for a phone stewardship scheme and an ownership-transfer mechanism. This is the only lever that changes the $65.

### Phase 3 — 12 months plus, strategic

9. **Pursue R2v3** once volume justifies the audit cost.
10. **Consortium approach.** With ADISA certified and two or three peer operators, approach a provider jointly. A single small operator has no leverage; a certified cohort with a shared evidence standard is a different proposition.
11. **Do not pursue manufacturer accreditation** unless a specific brand becomes commercially necessary. On the evidence in `03`, the eligibility barriers are not proportionate to your scale.

### The one thing to stop doing

Do not spend further time on AI-assisted recovery attempts as a *workflow*. On the evidence, the expected value is low, the per-request variance is high, and the time is better spent on the provenance pack that fixes the root cause.
