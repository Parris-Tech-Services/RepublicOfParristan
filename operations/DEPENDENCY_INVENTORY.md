# Third-party dependency inventory

Everything Parristan relies on that someone else runs. Review every six months. Last reviewed: 19 November 2026.

| Service | Used for | Owner of account | Lock-in risk | Exit plan |
|---|---|---|---|---|
| GitHub (organisation `Parris-Tech-Services`) | Public repo, Gazette source, CI | Josh + Glenn (owners) | Medium | Git bundles ([backup procedure](BACKUP_AND_HANDOVER.md)); any git host works |
| GitHub Enterprise trial | Private drafting repository | [ ] | **High — trial expires** | Final bundle before expiry; move to free private repo or Nextcloud |
| GitHub Pages | Website hosting (not yet live) | Repo admins | Low | `docs/` is plain static HTML; any static host |
| GitHub Actions | Validation and deploy | Repo admins | Low | Scripts run locally with Python |
| Matrix homeserver (which one: [ ]) | Interim official channel | [ ] | Medium | Export room history; Secretary minutes are the record |
| Python 3 standard library | Validator, registry | — | None | — |
| Cloudflare Registrar + DNS | `parristan.org` domain (expires 19 Nov 2027, auto-renew) | Josh + Glenn (both admins) | Low | Domain can be transferred to any registrar |
| Purelymail | Official email (Gazette 2026-011) | Joint admins | Low | Standard IMAP export; change MX records to move |

Paid services: domain (~US$11/yr) and Purelymail (~US$10/yr).
