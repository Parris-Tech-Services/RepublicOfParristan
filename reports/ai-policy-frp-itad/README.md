# AI Safety Policy, FRP Recovery, Right to Repair and Legitimate ITAD Operations

**Prepared for:** Dubbo E-waste (reuse-first ITAD, NSW, Australia)
**Date:** 27 November 2026
**Scope:** Policy, governance, legal and industry-practice analysis. This report deliberately contains **no operational bypass instructions** and should not be read as one.

---

## Executive summary

**Bottom line.** No AI provider surveyed publishes a policy that explicitly addresses Factory Reset Protection (FRP) recovery or electronic device refurbishment. The refusals you encountered are **inferences** drawn from broad cyber-misuse clauses, not the application of a written rule. Australian law does **not** require manufacturer authorisation to service or refurbish a device you lawfully own, and the two leading ITAD certification regimes (R2v3, e-Stewards) regulate *outcomes and evidence*, not *methods*. There is, however, **no professional access programme anywhere in the AI industry that covers ITAD work**, and no manufacturer programme structured for small regional refurbishers.

Those four findings pull in different directions, and the most useful thing this report can do is stop them being collapsed into one another.

**The four independent questions.**

| Question | Authority | Answer |
|---|---|---|
| Is it technically possible? | Engineering evidence | Model- and generation-specific. Old Android (pre-2019) has documented setup-wizard routes; modern Huawei (EMUI 12+/HarmonyOS) largely does not. Independent of everything else. |
| Is it lawful in Australia? | Commonwealth and NSW legislation | Removing an account lock from a device you own is **not per se** an offence. Computer offences turn on *unauthorised* access, and an owner is entitled. The genuine legal uncertainties are the copyright TPM provisions and provenance/stolen-goods law — neither of which is about the unlock itself. |
| Is it manufacturer-authorised? | Manufacturer agreements | Generally **no**. Manufacturer authority is contractual and gated. Australian law does not require it; manufacturer policy is not law. |
| Can an AI assist? | Provider policies | **Undetermined by any published policy.** No explicit prohibition exists. Providers infer restriction from wider cyber clauses and cannot verify provenance, so they default to caution. No ITAD pathway exists. |

**What the evidence supports.** A legitimate ITAD with documented title can lawfully refurbish FRP-locked hardware in Australia. AI refusals in this space are, on the published policy text, **broader than the policies require**. That is a real and defensible criticism of the current provider ecosystem, including of this assistant's behaviour.

**What the evidence does not support.** It does not establish an entitlement to assistance, an ITAD exemption, or that any provider must serve you. Absence of prohibition is not the same as permission. Nor does it support the view that manufacturer authorisation is the only legitimate route to recovery — that is a right-to-repair proposition, and Australian law already rejects it in principle.

**The unresolved core.** The blocker is not law, not standards, and not policy text. It is **verifiable provenance at the point of request**. An AI system cannot tell a documented ITAD from someone with a stolen phone, and the harm asymmetry is severe. Section 7 proposes a framework that could resolve this; section 10 states plainly what remains unsettled.

---

## Deliverable map

| # | Deliverable | File |
|---|---|---|
| 1 | Executive summary | this file, above |
| 2 | Detailed research report with citations | all files |
| 3 | Cross-provider AI policy comparison | `01-ai-provider-policies.md` |
| 4 | Australian legal and regulatory assessment | `02-australian-legal.md` |
| 5 | ITAD accreditation and affordability comparison | `03-itad-standards-and-accreditation.md` |
| 6 | Environmental and economic impact assessment | `04-environment-economics.md` |
| 7 | Proposed verified ITAD access framework | `05-framework-and-advocacy.md` §2 |
| 8 | Draft professional access request to OpenAI | `05-framework-and-advocacy.md` §4 |
| 9 | Practical, prioritised action plan | `05-framework-and-advocacy.md` §5 |
| 10 | Definitive evidence-based conclusion | `06-conclusion-and-open-questions.md` |

---

## Evidence classification convention

Every substantive claim in this report is tagged:

- **[V]** — verified against a primary or authoritative source (legislation, standards body, provider policy page, official statistics).
- **[R]** — reported: sourced to secondary reporting, vendor marketing, forums, or a party's own account. Directionally useful, not established.
- **[I]** — inference drawn by this analysis from [V] material. Explicitly not a finding of fact.

Where the record is contradictory, both positions are stated rather than resolved by preference.

---

## Case study as recorded

The following is the operator's account **[R]**, recorded here because several findings depend on it:

- Donated mobile phones received for refurbishment rather than disposal.
- Manufacturer-authorised pathways investigated; significant financial and organisational barriers reported.
- Direct contact with the technical department manager at Roadhound Electronics.
- Fixed quotation of **AU$65 per device**, no volume discount, charged **per device** rather than per successful recovery.
- One FRP-locked HTC Desire 530 restored to working condition with AI assistance in a prior session.
- Two Huawei handsets subsequently encountered AI refusals.

**Analytical note.** The $65-per-device-without-volume-tertier structure is the single most consequential commercial fact in this case study, and it is the one least amenable to policy remedy. No AI policy change makes that fee smaller. Section 6 of `04-environment-economics.md` treats it as an economic question, not a policy one.

---

## Method and limitations

Research conducted 27 November 2026 using public sources: provider policy pages, Commonwealth and NSW legislation, standards bodies, official statistics, and secondary reporting. Limitations that materially affect confidence:

1. **No access to manufacturer contracts.** Huawei, Samsung and Apple service agreements are not public. Claims about their terms are necessarily [R], not [V].
2. **No access to AI provider enforcement internals.** Classification thresholds are not published. Statements about *why* a refusal occurred are [I].
3. **Forum-sourced claims about Roadhound.** The strongest public statement that Roadhound is Huawei's sole Australian authorised repairer comes from enthusiast forums **[R]**. It is consistent with your direct conversation but not independently verified.
4. **The public record is internally contradictory** on Huawei's Australian service network (see `03`, §4). This is reported as a finding, not smoothed over.
5. **No legal advice.** Section 02 is analysis of statute and published guidance, not a legal opinion. Matters with criminal exposure warrant qualified advice.
