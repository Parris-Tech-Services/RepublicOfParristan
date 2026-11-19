# Permanent email and chat proposal — template (DRAFT)

**For:** Glenn Peterson, Chief Digital Officer. **Due:** 3 December 2026 (Gazette 2026-006, Motion 1). **Status:** template; Glenn fills in and presents it to the Assembly.

## 1. Recommendation (pre-filled at the organiser's request — Glenn to confirm or change)
Use **Migadu Micro** (about **US$19 a year**, billed annually, flat price for the whole account, not per person) for email on a Parristan domain, read in **Thunderbird**. Keep the existing **Matrix/Element** room for chat. Unlimited mailboxes and role addresses (president@, registrar@, secretary@, treasurer@, returning-officer@) can be passed on when officers change. Standard IMAP/SMTP means we can move providers later without losing mail. Total first-year cost: about US$19 plus the domain (roughly A$15–30 a year).

**Limits to know:** 200 incoming and 20 outgoing emails per day across the account, 5 GB storage. That's plenty for five members; if an election notice to many people is ever needed, upgrade to the next plan. Prices checked 19 Nov 2026 at migadu.com/pricing — recheck before paying.

## 2. Options considered
| Option | Email | Chat | Cost / year | Open source? | Who runs it | Effort |
|---|---|---|---|---|---|---|
| **Migadu Micro + Matrix (recommended)** | Migadu, own domain | Existing Matrix room | ~US$19 + domain | Chat yes | Provider | Low |
| Self-hosted (UCS mail or Mailcow + Matrix/Element) | Self-hosted | Self-hosted Matrix | Hardware + domain | Yes | CDO | High |
| [Other] | | | | | | |

## 3. Requirements checklist
- [ ] Each member has their own login; at least two admins
- [ ] Role addresses (president@, registrar@, secretary@) can be passed on at handover
- [ ] Two-factor authentication available
- [ ] Encrypted chat for votes and private discussion
- [ ] Records can be exported (open formats) and backed up
- [ ] Works on members' phones and computers, including junior members with parental controls
- [ ] Total cost fits the draft budget

## 4. Migration plan
1. Assembly approves this proposal and who pays (Treasurer records it).
2. Register the domain (both joint admins on the registrar account, 2FA on — see `operations/ADMIN_ACCESS_SETUP.md`).
3. Sign up for Migadu Micro; add the domain; copy the DNS records Migadu shows (MX, SPF, DKIM, DMARC) into the domain's DNS.
4. Create one mailbox per member plus role aliases pointing to the current officeholder.
5. Two members test sending/receiving in Thunderbird and on phone; check mail does not land in spam (send to a Gmail address).
6. Everyone set up; keep the Matrix room as the official channel until the Assembly confirms email works.

## 5. Motion for the Assembly
> That the Assembly adopts Migadu Micro email on the domain [name] together with the existing Matrix room as the permanent official email and chat system, with [names] as administrators, replacing the interim Matrix arrangement from [date].
