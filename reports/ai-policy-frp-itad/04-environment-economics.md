# 04 — Environmental and Economic Impact Assessment

*Deliverable 6. Covers research workstream 6.*

---

## 1. The macro picture

### 1.1 Global e-waste [V]

Source: Global E-waste Monitor 2024 (UNITAR/ITU), <https://rmis.jrc.ec.europa.eu/ewaste>

- **62 million tonnes** of e-waste generated in 2022.
- Projected **82 million tonnes by 2030**.
- Only **22.3%** is formally collected and recycled.
- An estimated **US$62 billion** of recoverable natural resources is lost to improper handling.

### 1.2 Mobile phones specifically [V]

Source: UNITAR / WEEE Forum, <https://unitar.org/about/news-stories/news/16-billion-mobile-phones-possessed-worldwide-53-billion-will-become-waste-2022>

- Approximately **16 billion mobile phones** in use worldwide.
- Roughly **5.3 billion** were expected to fall out of use in 2022 alone.

**Assessment.** Handsets are a high-turnover, high-embodied-value, low-recovery-rate product class. The macro case for reuse over recycling is not seriously contested.

---

## 2. The specific claim: do account locks cause avoidable e-waste?

### 2.1 What is established [V/I]

- Anti-theft locks are a **deliberate design choice** whose purpose is to reduce the resale value of stolen devices.
- A side effect is that devices with unresolvable account bindings cannot complete a verified sanitisation and therefore cannot enter the reuse stream.
- In professional ITAD practice they default to the **destruction/recycling** path, not because unlocking is prohibited but because the evidence trail for reuse cannot be completed.

### 2.2 What is *not* established [—]

**There is no reliable public dataset quantifying how many devices are discarded specifically because of account locks.** Not from the Global E-waste Monitor, not from MobileMuster, not from any manufacturer. The figure is frequently asserted in advocacy material and never sourced.

**This is an explicit unanswered question and should be treated as such in any submission you make.** Claiming a number you cannot support is the fastest way to lose credibility with a regulator or a provider. You can legitimately say: *"the mechanism is real and the direction of effect is certain; the magnitude is unmeasured."* That is defensible.

---

## 3. The economics of the $65

### 3.1 The arithmetic [I]

The per-unit decision is:

```
net = resale − (unlock fee + parts + labour + warranty reserve + freight)
```

With a flat AU$65 fee, **per device, charged regardless of success**, the fixed cost is high relative to the value of EMUI-era Huawei hardware. Huawei's Australian resale value fell sharply after the 2019 loss of Google Mobile Services, so the fee is a large fraction of most unit values — often exceeding the entire margin.

### 3.2 Why this is not a policy problem [I]

**The $65 is the single most consequential number in this case study, and no policy change anywhere — AI, legal, or standards — makes it smaller.** It is a pricing decision by a monopoly-adjacent authorised provider with no volume tier. That is a competition question, not a governance one.

Three honest implications:

1. The economic case for unlocking a donated box wholesale is **negative** at this price point. That is a business fact, not a moral one.
2. The correct response is **triage**: unlock the minority that clears margin, recycle the rest.
3. If the goal is systemically better reuse outcomes, the lever is **policy and market structure** (ownership-transfer mechanisms, right-to-repair reform, subsidised recovery), not bypass availability.

### 3.3 Per-device charging and risk [I]

Charging per device rather than per successful recovery transfers all technical risk to you. On a mixed donated box, expected cost is $65 × N regardless of outcome. Any business model built on this must assume a failure rate, and a failure rate on unknown donated hardware is high.

**Ask for it in writing:** what happens to the fee when recovery fails. If there is no refund or credit, price that in explicitly.

---

## 4. Environmental impact of premature disposal

### 4.1 Embodied impacts [R]

A smartphone's manufacturing footprint is dominated by:
- Semiconductor fabrication (energy- and water-intensive),
- Precious and critical metals (gold, copper, cobalt, rare earths, tantalum),
- Battery materials (lithium, cobalt, nickel),
- Assembly and logistics.

Published lifecycle assessments commonly place a handset's manufacturing carbon footprint in the **tens of kilograms of CO₂e**, i.e. the majority of its lifetime footprint is incurred before first use. Recycling recovers a fraction of the material value; **reuse avoids the entire manufacturing footprint.** That ordering — reuse ≫ recycling — is robust even though exact per-device figures vary widely by model and study. **[R/I]**

### 4.2 The honest limit of this argument [I]

**The environmental case does not justify bypass.** A locked phone can still be recycled properly at zero cost through MobileMuster, which destroys data and recovers materials. The environmental loss from recycling a locked handset is real but it is the loss of *reuse* value, not the loss of *disposal* compliance.

This matters because it is the argument opponents will make, and it is correct: **environmental harm does not create a security exemption.** The environmental case supports changing ownership-transfer policy and reducing recovery costs. It does not support weakening the anti-theft control itself.

Intellectual honesty requires conceding this, and then making the narrower, stronger claim: *the cost and inaccessibility of legitimate recovery is itself a driver of avoidable recycling, and that is a policy failure susceptible to policy remedy.*

---

## 5. Digital inclusion

- Reuse-first ITAD supplies low-cost devices to people who would otherwise be excluded. This is the social dividend of your model and it is a legitimate advocacy asset. **[I]**
- Australian digital inclusion research consistently finds a material minority of households without reliable device access; refurbished handsets are a recognised intervention. **[R]**
- **Unanswered:** no robust Australian dataset isolates the contribution of *locked-device attrition* to device affordability. Again: mechanism certain, magnitude unmeasured.

---

## 6. Barriers specific to small independent refurbishers

| Barrier | Effect on a Dubbo-scale operator |
|---|---|
| $65 flat per-device unlock, no volume tier | Kills the margin on all but premium units |
| No manufacturer accreditation pathway | No access to official tools or credentials |
| Certification costs (ADISA, R2) | Fixed overheads not matched by donated-volume revenue |
| Insurance and premises requirements (Samsung, Apple) | Effectively excludes home-based or shared-premises operators |
| No legislated phone stewardship scheme | No producer funding for collection or recovery |
| Provenance burden | Every undocumented donation is a legal risk, not an asset |

**Synthesis.** The small refurbisher is squeezed from three directions: **recovery cost** (fixed, high, per-device), **accreditation cost** (fixed, high, annual), and **provenance risk** (unbounded). None of these is addressed by AI policy. All three are addressable by industry or government policy.

---

## 7. Do anti-theft systems adequately accommodate legitimate secondary ownership?

**Short answer: no.** **[I]**

- FRP is designed to bind a device to an account, with recovery requiring the original credentials or a documented proof-of-purchase process through an authorised channel.
- There is **no standard, low-friction, machine-verifiable mechanism** for a secondary owner to demonstrate title and obtain a clean device state.
- The available paths are: (a) the original owner removes the binding; (b) an authorised service centre acts on proof of purchase; (c) professional destruction.
- For donated and orphaned devices, (a) is unavailable and (b) is often unavailable for lack of receipts, leaving only (c).

**This is a genuine design gap in the anti-theft ecosystem**, and it is a legitimate right-to-repair argument. It is also the strongest version of your case: not "let us bypass security," but "there is no workable ownership-transfer mechanism for the secondary market, and that gap destroys reusable hardware."

---

## 8. Summary table

| Claim | Status | Confidence |
|---|---|---|
| Global e-waste is 62 Mt and 22.3% recycled | Established | High [V] |
| 5.3 billion phones left use in 2022 | Established (modelled) | High [V] |
| Locks force devices out of the reuse stream | Established mechanism | High [I] |
| Volume of devices lost to locks | **Unmeasured** | None [—] |
| Reuse avoids more carbon than recycling | Established | High [R/I] |
| Environmental harm justifies bypass | **Rejected** | High [I] |
| Legitimate recovery cost drives avoidable recycling | Established mechanism | Medium [I] |
| Magnitude in Australia | **Unmeasured** | None [—] |
| Anti-theft systems accommodate secondary ownership | **No** | High [I] |
