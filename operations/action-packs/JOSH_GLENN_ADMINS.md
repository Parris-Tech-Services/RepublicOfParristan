# Josh Parris and Glenn Peterson — joint admin pack

Gazette 2026-009: Josh and Glenn are joint admins of the channel, the GitHub organisation and the domain, so no single person can lock members out. Full guide: [../ADMIN_ACCESS_SETUP.md](../ADMIN_ACCESS_SETUP.md).

## Already done (19 Nov)
- [x] Cloudflare (domain): both admins, two-step sign-in on.
- [x] Purelymail (email): admin moved to admin@parristan.org; both have access.

## GitHub — do together, ~10 minutes
- [ ] Both have personal GitHub accounts with two-step sign-in on.
- [ ] github.com/orgs/Parris-Tech-Services/people → both shown as **Owner**. If Glenn isn't, Josh: *Invite member → Role: Owner*.
- [ ] Organisation **Settings → Authentication security → Require two-factor authentication**.
- [ ] Repository **Settings → Branches → Add rule** for `main`: require a pull request before merging.
- [ ] Repository **Settings → Pages → Source: GitHub Actions** (after merging the `claude/parristan-work-plan` branch), then run *Deploy Gazette to GitHub Pages*. See [../PAGES_PUBLISHING.md](../PAGES_PUBLISHING.md).
- [ ] Glenn opens Organisation Settings to prove access works.

## Matrix room — ~5 minutes
- [ ] In Element: room **Settings → Roles & Permissions** → both Josh and Glenn at **Admin (100)**.
- [ ] Both have saved their **Security Key / recovery key** (Settings → Security & Privacy), otherwise encrypted history can be lost.
- [ ] Optional: export room history monthly (room menu → *Export chat*) into the records backup.

## Optional but recommended
- [ ] Point the website at parristan.org once Pages is live (add `docs/CNAME` containing `parristan.org` and a Cloudflare CNAME record `@` → `parris-tech-services.github.io`, DNS only).

## Tell the records
Reply "GitHub and Matrix admin verified <date>" and the founding checklist item will be ticked.
