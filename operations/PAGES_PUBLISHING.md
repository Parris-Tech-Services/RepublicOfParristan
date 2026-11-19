# Publishing the Gazette website

**Status checked 19 November 2026:** An alternative production deployment is available at [https://republic-of-parristan.vercel.app/](https://republic-of-parristan.vercel.app/) from GitHub `main/docs` through Vercel. The Vercel production deployment reached **READY**, and connected checks returned HTTP 200 for the homepage, the administration dashboard and the public decisions JSON export. Production aliases are not Vercel sign-in protected. Independent anonymous-client HTTP verification was not available in this run.

## Current deployment: Vercel

- **Project:** `republic-of-parristan`, team `joshualparris-projects`, Hobby plan.
- **Repository:** `Parris-Tech-Services/RepublicOfParristan`; **production branch:** `main`; **root directory:** `docs`.
- **Initial verified production source:** `41f12ea9da645d790dbff27777c620e5aebf974c` on 19 November 2026, [deployment record](https://vercel.com/joshualparris-projects/republic-of-parristan/EEG78tvTcraJLohBHJzyVgmVvANx).
- **Evidence:** Vercel READY and connected HTTP 200 responses for `/`, `/administration.html` and `/data/decisions.json`.
- **Access:** production alias intentionally public-facing; Vercel Authentication retained for preview deployments. No private roster or ballot data was deployed.
- **Release:** normal pushes to `main` trigger Vercel's Git integration; check the resulting commit SHA and route responses before claiming a later update is live.
- **Rollback:** promote a previous known-good production deployment in Vercel after verifying its source and content; do not overwrite historic Gazette notices.

## Optional GitHub Pages (not configured)

The proposed Pages address `https://parris-tech-services.github.io/RepublicOfParristan/` was returning HTTP 404. A [GitHub Pages Action](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470637527) failed in `actions/configure-pages` with `Get Pages site failed: Not Found`. The default `GITHUB_TOKEN` cannot create a Pages site using the action's `enablement` option.

An authorised repository administrator can enable **Settings → Pages → Build and deployment → Source: GitHub Actions**, then manually run `Deploy Gazette to GitHub Pages`. The workflow is manual-only while Pages is not configured, to avoid unsuccessful runs on each documentation commit.

Alternative: configure GitHub Pages to deploy from `main` and `/docs` directly. Choose *one* Pages publishing method rather than enabling both.

**Do not mark national operations item 34 complete until the actual GitHub Pages URL is independently reachable.** The Vercel deployment is a separately verified technical publishing milestone, not evidence that GitHub Pages is operational.

## Public verification checklist

- [x] Vercel production deployment READY, linked to the intended `main` commit.
- [x] Connected deployment returned HTTP 200 for home, admin and JSON routes.
- [x] Vercel production sign-in protection disabled; preview sign-in protection retained.
- [ ] Independently verify public browser access without account cookies or share links.
- [ ] Enable and verify GitHub Pages only if that second hosting route is wanted.
- [ ] Check cross-device readability, keyboard accessibility and responsive layout in a real browser.

Never publish personal contact details, confidential membership registers or individual ballots.
