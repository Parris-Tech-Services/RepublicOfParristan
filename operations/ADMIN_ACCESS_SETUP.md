# Joint administrator access — setup guide

Gazette 2026-009 decided that **Josh Parris and Glenn Peterson are joint admins**. This guide turns that decision into actual access. Tick each step in a private record and note the date; publish only "completed on <date>", never passwords or recovery codes.

## GitHub organisation `Parris-Tech-Services`
1. Both people have their own personal GitHub account (no shared login).
2. Both turn on two-factor authentication, preferably with a passkey or authenticator app, and store recovery codes offline.
3. Organisation → People: both set to **Owner**. Two owners means one can recover access if the other loses theirs.
4. Organisation → Settings → Authentication security: **require 2FA** for all members.
5. Repository → Settings → Branches: protect `main` (require a pull request; allow owners to bypass for emergencies).
6. Check who else has access (People, Outside collaborators, Apps). Remove anything not needed.

## Domain (once one is chosen)
1. Register in the name agreed by the founders (an individual on behalf of the association until there is a legal entity — record who in the decision register).
2. Turn on registrar 2FA and registrar lock. Add the other admin as a contact or delegate if the registrar allows.
3. Turn on auto-renew and record the renewal date in the calendar.

## Other accounts (Matrix room, future Nextcloud/mail)
- At least two admins on each. No account depends on one person's phone or email alone.

## Handover
If an admin steps down: add the replacement first, confirm they can log in, then remove the old admin. Record the change in the decision register.

## Verification (do this together, then record the date)
- [ ] Each admin can open Organisation → Settings.
- [ ] Each admin can change Pages settings.
- [ ] Domain registrar shows both contacts (when applicable).
