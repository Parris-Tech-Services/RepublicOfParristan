# Publishing the Gazette website

**Status — 19 November 2026:** Parristan has two alternative published hosts:
- **Public snapshot:** [https://republic-of-parristan-gazette.joshualparris.chatgpt.site/](https://republic-of-parristan-gazette.joshualparris.chatgpt.site/) — reported published by a separate process and recorded in the repository; it is **not** documented as a continuously Git-linked deployment.
- **Vercel Git-linked mirror:** [https://republic-of-parristan.vercel.app/](https://republic-of-parristan.vercel.app/) — directly linked to `Parris-Tech-Services/RepublicOfParristan` `main` with project root `docs`, on a Hobby team plan. Initial production deployment at commit `41f12ea9da645d790dbff27777c620e5aebf974c` is **READY**. The connected Vercel deployment returned HTTP 200 for `/`, `/administration.html` and `/data/decisions.json`. The production alias is not sign-in protected; previews remain SSO protected. An independent, anonymous external client check was not available for this mirror.

## Automatic publishing and verification

Vercel Git integration deploys updates to `main/docs` to the Vercel production alias. After changes merge, check Vercel's latest production SHA and the site routes before claiming the new version is live. [Initial verified deployment](https://vercel.com/joshualparris-projects/republic-of-parristan/EEG78tvTcraJLohBHJzyVgmVvANx). A snapshot on the other host does not necessarily receive subsequent GitHub commits.

## Optional GitHub Pages — not enabled

The address `https://parris-tech-services.github.io/RepublicOfParristan/` returned HTTP 404; a [failed Pages run](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44470637527) stopped at `actions/configure-pages`: **Get Pages site failed: Not Found**. The default `GITHUB_TOKEN` cannot provision the initial Pages site using `enablement: true`.

An authorised repository admin may enable **Settings → Pages → Build and deployment → Source: GitHub Actions**. The existing `Deploy Gazette to GitHub Pages` workflow is now manual-only until the site has been enabled, preventing recurring failed push runs. The admin may then dispatch the workflow and independently check its homepage, notice and fallback page. An alternative is Pages `main`/`docs` branch publishing; use one Pages method, not both.

**Keep National Operations item 34 unchecked until GitHub Pages itself is actually reachable.** Existing alternative hosts do not make a different host operational.

## Verification checklist

- [x] Vercel production deployment status READY and intended source commit identified
- [x] Three connected Vercel deployment routes returned HTTP 200
- [x] Production Vercel Authentication disabled; previews remain protected
- [x] Earlier separately published public snapshot recorded as its own source
- [ ] Independent unauthenticated HTTP/browser check of Vercel alias
- [ ] GitHub Pages configured and verified, only if the second hosting method is desired
- [ ] Real-device accessibility and responsive layout checks

## Rollback

The Git-linked Vercel mirror can be restored by promoting a previously verified deployment. The separate public snapshot should be rolled back with its own publishing mechanism; publishing to Vercel does not control that host. Do not silently overwrite historic Gazette decisions or introduce private data.
