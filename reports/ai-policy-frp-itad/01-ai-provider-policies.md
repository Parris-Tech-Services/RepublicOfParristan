# 01 — AI Provider Policies and Cross-Provider Comparison

*Deliverable 3. Covers research workstreams 1 and 2.*

---

## 1. Headline finding

**No surveyed provider publishes a policy that names Factory Reset Protection, account-lock removal, refurbishment, or ITAD.** Not one. Every refusal in this space is therefore an application of a general clause about security, unauthorised access, or illegal activity — an inference by the model or by a classifier, not the execution of a written rule.

This is the single most important finding in the report, and it cuts in your favour on the narrow question: the policies do not say what the refusals imply they say.

It does **not** follow that assistance is owed. Policy silence is not permission; providers reserve broad discretion, and clauses about "unauthorised" access are deliberately open-textured.

---

## 2. OpenAI

### 2.1 Usage Policies [V]

Source: <https://openai.com/policies/usage-policies/>

The Usage Policies set out prohibited categories. The relevant ones to this case are the security-related clauses concerning compromising the security or integrity of systems and obtaining unauthorised access. The policy does **not** define "unauthorised" by reference to device ownership, nor does it address device servicing, refurbishment, or data sanitisation as a use case.

**Assessment.** FRP recovery on a device you own is not named. Whether it falls inside "unauthorised access" depends entirely on whether the operator's access is authorised — which is a *title* question, not a technical one. The policy does not answer it.

### 2.2 Model Spec [V]

Source: <https://model-spec.openai.com/>

The Model Spec is a behaviour specification, not a use policy. Its relevant architecture is the hierarchy of authority — chain of command, then user, then model defaults — plus rules on facilitating wrongdoing and on not taking actions that are unsafe or irreversible. It is explicitly not a list of permitted topics.

**Assessment.** The Spec gives a model discretion to decline where it cannot establish that an action is legitimate. That discretion is the mechanism by which a policy-silent case becomes a refusal. It is also the mechanism by which a documented, authorised case *should* be assistable. The Spec does not resolve which applies; it delegates the judgement.

### 2.3 Trusted Access for Cyber / Daybreak [V/R]

Sources: <https://openai.com/form/enterprise-trusted-access-for-cyber/> (locale variants exist); OpenAI Help Center article "OpenAI Daybreak — Trusted Access for Cyber overview".

This is the closest thing OpenAI has to a professional access pathway for security work. Per the published material **[R]**:

- Access is restricted to **approved** users and **approved internal workflows**.
- Individual access requires an eligible paid plan, advanced account security, and at least one compatible FIDO2 hardware security key.
- The higher tier ("Daybreak Red") is limited to approved Business and Enterprise organisations.
- Use remains bound by the Usage Policies; the access form's own text ties permitted use to the Usage Policies and expressly excludes aggressive operations, obtaining unauthorised access, and malware deployment.

**Assessment.** This is an *authorisation* programme for cyber defence. It is **not** an ITAD programme and does not cover device refurbishment. It is, however, proof of concept that OpenAI will extend differential access on the basis of verified identity and purpose. That matters for section 7 of the framework paper: the architecture you would be asking for already exists in another domain.

### 2.4 System cards [V]

Published system cards describe evaluations and mitigations, including cyber capability and refusal behaviour. They do not publish per-request classification logic. Any claim about *why* a specific refusal occurred is therefore inference.

---

## 3. Anthropic

Sources: <https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet>; <https://support.claude.com/en/articles/12005017-using-agents-according-to-our-usage-policy>

Anthropic publishes the most explicit cyber taxonomy of any provider surveyed. It separates:

- **Prohibited use** — "Cybersecurity activities that are almost always used maliciously and have little to no legitimate defensive application such as mass data exfiltration or ransomware code development."
- **High Risk Dual use** — activities with both legitimate and malicious applications.

The agents usage-policy guidance includes an explicit heading, **"Do Not Use Agents for Unauthorized System Access or Manipulation,"** and a sub-item prohibiting installing "malware, backdoors, or monitoring software **without authorization**."

**Assessment.** This is the clearest evidence in the entire survey that **authorisation is a live variable in provider policy**, not a fixed prohibition. The phrase "without authorization" is doing real work: with authorisation, the same conduct falls outside the prohibition. FRP recovery sits in the dual-use band — it is not mass exfiltration or ransomware, and it is not obviously "almost always malicious."

---

## 4. Google

Source: <https://policies.google.com/terms/generative-ai/use-policy>

The Generative AI Prohibited Use Policy includes, among others:

- "Do not engage in dangerous or illegal activities, or otherwise violate applicable law or regulations."
- "Do not compromise the security of others' or Google's services."

**Assessment.** Note the object: "others' or Google's services." A device you own is not "others' services" in any natural reading. The clause is aimed at service compromise, not at hardware servicing. This is the clearest instance of a policy whose text does *not* reach the conduct, even though a cautious model might apply it anyway.

The "illegal activities" clause is a genuine hook, but it is circular until you know the law — which is section 02's job. If the conduct is lawful in NSW, this clause has nothing to bite on.

---

## 5. Microsoft

Source: <https://www.securityweek.com/microsoft-ai-code-of-conduct-sets-cyberattack-boundaries-chain-of-command-safety-constraints/> **[R]**

Reported coverage of Microsoft's draft AI code of conduct states that it bars models from producing "exploit code, attack tooling or step-by-step operational guidance," while **allowing** "vulnerability discovery, malware analysis, proof-of-concept exploit development for testing," and names defensive cybersecurity as a domain where restricted capabilities may be legitimately required.

**Assessment.** Microsoft's distinction is capability-based: offensive tooling barred, defensive and analytical work permitted. Device refurbishment is neither, which illustrates the taxonomy gap rather than resolving it. Because this is draft and reported rather than published policy **[R]**, treat with caution.

---

## 6. DeepSeek

Source: <https://cdn.deepseek.com/policies/en-US/deepseek-terms-of-use.html>

The Terms of Use are law-referencing and service-integrity oriented: users may not use the service for illegal or non-compliant activities, may not attack or disrupt the service, and must comply with applicable law including export control.

**Assessment.** There is no published cyber-specific use policy comparable to Anthropic's or OpenAI's. The operative standard is **compliance with applicable law**, which makes the Australian legal analysis in section 02 directly determinative for this provider in a way it is not for others. This is analytically important: for DeepSeek, "is it lawful?" is closer to the whole question.

---

## 7. xAI

Source: acceptable use policy (xAI publishes an AUP prohibiting intrusion, system compromise, fraud and similar conduct) **[V]**

**Assessment.** General intrusion prohibition, no device-servicing carve-out, no explicit cyber dual-use taxonomy published. Same inference gap as the rest.

---

## 8. Open-source and self-hosted providers

Open-weight models (Llama family, Mistral, Qwen and similar) carry acceptable-use policies but the operator controls the deployment, so **provider policy does not govern the request** — the deployer's obligations do. For a small ITAD operator this is a materially different governance path: it moves the question from provider policy to your own acceptable-use framework and insurance. It is outside scope here but should not be overlooked as a legitimate option.

---

## 9. Cross-provider comparison

| Provider | Explicit FRP/refurb policy | Cyber taxonomy published | Authorisation materially relevant | Professional access pathway | Reaches owned-device servicing? |
|---|---|---|---|---|---|
| OpenAI | No | Model Spec + Usage Policies | Yes (Spec discretion; GTAC) | Yes — GTAC/Daybreak, cyber only | Not on the text |
| Anthropic | No | Yes — prohibited vs dual-use | Yes — "without authorization" | Cyber safeguards only | Not clearly; dual-use band |
| Google | No | Minimal | Implied | No | No — clause is about "services" |
| Microsoft | No | Draft code of conduct **[R]** | Yes — defensive carve-out | None published for ITAD | Not addressed |
| DeepSeek | No | No | Law-dependent | None | Only via legality |
| xAI | No | No | Implied | None | Not on the text |
| Open-weight | N/A (deployer) | N/A | Deployer determines | Self-hosted | Fully deployer-governed |

**Consistency:** zero of seven name the conduct.
**Divergence:** they differ sharply on whether authorisation changes the answer, and in what counts as "defensive."
**Consequence:** identical requests produce different outcomes across providers for reasons unrelated to the request's merits. You have experienced this directly: one session assisted an HTC recovery; subsequent sessions declined Huawei work.

---

## 10. Findings on false positives and review mechanisms

1. **Over-broad classification is structurally likely.** Security classifiers are trained on harm patterns; device-unlock language pattern-matches to account-takeover language. A dual-use activity with no published taxonomy is the textbook false-positive case. **[I]**

2. **No provider publishes an appeal route specific to dual-use device servicing.** GTAC is an access programme for cyber defence, not a review mechanism for a refused refurbishment request. **[V]**

3. **The practical review mechanism available to you is a written support/policy enquiry**, not a technical escalation. Whether it produces a substantive answer is unknown and untested at scale. **[I]**

4. **Nothing in the published text obliges a provider to grant an ITAD exception**, and no provider has published one. That is a gap in the ecosystem, not a breach by any individual provider. **[V]**

---

## 11. Direct answer to workstream 1's questions

| Question | Answer |
|---|---|
| Is FRP recovery explicitly prohibited? | **No.** Not by any surveyed provider. |
| Are restrictions inferred from broader security policies? | **Yes** — this is the entire mechanism. |
| Does authorisation materially change what is permitted? | **Yes, in principle** — Anthropic's "without authorization" and OpenAI/Microsoft defensive carve-outs show it. Unverifiable in practice, which is why it does not help at the point of request. |
| Does ITAD qualify as legitimate defensive security? | **No.** It is not defensive security and not device administration in the enterprise sense. It is asset disposition. Forcing it into the defensive-security category is a weak argument; it should be argued as its own category. |
| Could an assistant be unnecessarily refusing a legitimate request? | **Yes, plausibly, on the policy text** — particularly where the clause invoked is about "others' services." Whether any given refusal was unnecessary cannot be established without the provider's classification reasoning, which is unpublished. |
| Is there an ITAD-specific exception or pathway? | **No.** Not at any surveyed provider. |
