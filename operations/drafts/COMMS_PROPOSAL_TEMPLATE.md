# Permanent email and chat proposal — template (DRAFT)

**For:** Glenn Peterson, Chief Digital Officer. **Due:** 3 December 2026 (Gazette 2026-006, Motion 1). **Status:** template; Glenn fills in and presents it to the Assembly.

## 1. Recommendation (pre-filled at the organiser's request — Glenn to confirm or change)
Use **Purelymail** (about **US$10 a year**, flat price for the whole account, no per-user charge on our own domain) for email on a Parristan domain, read in **Thunderbird**. Keep the existing **Matrix/Element** room for chat and votes.

**Each role gets its own mailbox** (president@, secretary@, treasurer@, registrar@, cdo@, returning-officer@), so mail stays with the office and is handed over by resetting the password, not by forwarding into personal inboxes. Members can also have personal mailboxes. Routing rules can send one address to several people (e.g. assembly@ to all members). Standard IMAP/SMTP means we can move providers later without losing mail.

Total first-year cost: about US$10 plus the domain (roughly A$15–30 a year).

### What it covers for a small government
| Need | Purelymail |
|---|---|
| Official addresses on our own domain | Yes |
| Role mailboxes that pass to the next officeholder | Yes (separate users, no extra cost) |
| Group addresses (assembly@) | Yes, via routing rules |
| Two-factor sign-in | Yes — app codes or security key |
| Works in Thunderbird and phones | Yes (IMAP/SMTP) |
| Shared calendar | Basic CalDAV only (no webmail calendar). Use Thunderbird's calendar, or keep the National Calendar in Nextcloud later |
| Export / leave later | Yes, standard IMAP |
| Records retention | Not built in — Secretary exports official mail into the records backup monthly (`operations/BACKUP_AND_HANDOVER.md`) |
| Guaranteed uptime / support contract | **No.** Small operator; acceptable for five members, revisit if Parristan grows |

Prices and features checked 19 Nov 2026 at purelymail.com — recheck before paying.

## 2. Options considered
| Option | Email | Chat | Cost / year | Open source? | Who runs it | Effort |
|---|---|---|---|---|---|---|
| **Purelymail + Matrix (recommended)** | Purelymail, own domain | Existing Matrix room | ~US$10 + domain | Client-side yes | Provider | Low |
| Migadu Micro + Matrix | Migadu, own domain | Existing Matrix room | ~US$19 + domain | Client-side yes | Provider | Low |
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
3. Sign up for Purelymail; add the domain; copy the DNS records Purelymail shows (MX, SPF, DKIM, DMARC) into the domain's DNS.
4. Create role mailboxes and member mailboxes; turn on 2FA for every account; give role passwords to officeholders and record who holds each (not the password) in the handover list.
5. Two members test sending/receiving in Thunderbird and on phone; check mail does not land in spam (send to a Gmail address).
6. Everyone set up; keep the Matrix room as the official channel until the Assembly confirms email works.

## 5. Motion for the Assembly
> That the Assembly adopts Purelymail email on the domain [name] together with the existing Matrix room as the permanent official email and chat system, with [names] as administrators, replacing the interim Matrix arrangement from [date].
