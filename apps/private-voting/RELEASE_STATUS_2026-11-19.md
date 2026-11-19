# Private voting service — production verification register

**Status (19 November 2026):** code implemented, private database provisioned, founder account slots seeded, and rules tests passed in PR #33. These facts are **not** proof of live service or certified voting. The five accounts are not yet activated, and no ballots have been cast through this application.

## Release gates

- [x] Five named founder records, without passwords or private contact details in Git
- [x] One-use 48-hour invitations; password hashing; private sessions and CSRF checks in source
- [x] Written motions: three-voter quorum, 48-hour interval / early closure with all founders, majority of valid cast votes
- [x] Constitution amendments: 14-day full-text notice and two-thirds valid votes
- [x] Independent tally/check/certify workflow implemented for recorded motions
- [x] Historical first presidential election in Gazette 2026-012/013 is preserved and not re-created as a new app ballot
- [x] New secret election ballots locked pending independent security assessment, officer approval and adopted method
- [x] Private-voting tests and Gazette validation passed on PR #33
- [x] Production deployment READY at Git SHA `85c4f2978c80ac0c1c7a7f6821ff09e3998a94c4`; [private login page](https://republic-of-parristan.vercel.app/voting/) returned HTTP 200 through connected Vercel. This **does not** mean voting is functional.
- [ ] Production API health check and unauthenticated private-data rejection: **BLOCKED** — [status endpoint](https://republic-of-parristan.vercel.app/api/voting?action=status) returned HTTP **503** with `Voting database not connected` because `DATABASE_URL` has not been configured on the deployed project. The API cannot authenticate, enforce ballots, or be verified until connected.
- [ ] First organiser activation and five founders' account ownership verified
- [ ] Officers verify official use of this portal is adopted and compatible with Matrix/email channel
- [ ] One real end-to-end written-motion vote with quorum, double-vote rejection and certified result independently observed
- [ ] Independent election security review before any new secret electoral ballot

The deployed site can show a sign-in page to everyone while the service is private behind its **own** founder authentication. An accessible login URL does not give non-members access to ballots.

**Deployment context:** Git-linked Vercel project `parristan-private-assembly`, root `apps/private-voting`, sensitive `DATABASE_URL` and `BOOTSTRAP_KEY` stored in hosting environment. Direct deployment API returned a free-tier daily rate limit (402) on 19 November, so a source push will test the standard Git integration as an alternative. Do not claim this alternative succeeded unless a production deployment is observed as READY.

**Governance:** [Gazette 2026-013](../../gazette/2026/2026-013-first-president-confirmed.md) records Joshua Parris as President; [Gazette 2026-014](../../gazette/2026/2026-014-presidents-first-programme.md) retains Matrix debate/votes and official email for notices. The private portal must not silently replace either channel.

## Actual hosting verification — 19 November 2026

- [PR #36](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/36) merged, both voting and Gazette CI passed. It hosts the authenticated voting app as a supplementary subpath to the already-live public Gazette. The main Gazette homepage still returned HTTP 200 after production deploy.
- Vercel production SHA `85c4f2978c80ac0c1c7a7f6821ff09e3998a94c4` reported **READY**.
- `https://republic-of-parristan.vercel.app/voting/` returned HTTP 200 and HTML login page.
- `https://republic-of-parristan.vercel.app/api/voting?action=status` returned HTTP **503**: `{"error":"Voting database not connected"}`.
- The connected-service security check blocked moving sensitive Neon credentials directly into a different Vercel project. The Vercel API also returned a 402 daily API deployment quota error when trying the separate private voting project. The existing Gazette Git-linked production build worked instead.

### Manual secure hosting configuration still required

Through the Vercel project `republic-of-parristan` → Settings → Environment Variables, an authorised owner must set `DATABASE_URL` to the scoped Postgres connection string for the **existing, separate** Neon database `parristan_ballots`, and set `BOOTSTRAP_KEY` to a unique random private setup code, targeting **Production only**. Keep `SECRET_ELECTIONS_ENABLED=false`. Do not place these values in GitHub, the public Gazette, chat rooms or URLs.

**After saving the variables, trigger a production redeployment**, then verify the API status is 200 and `setupRequired:true`, that `?action=polls` rejects unauthenticated users with 401, and only then complete the first founder account activation on the private login page. Login and one-vote-per-person behaviour must be tested with authorised officers before the portal is used for real business.

The [published Lovable alternative](https://parristan-assembly-voting.lovable.app/) remains an independent, **unusable-for-official-voting** prototype with zero authenticated members and exhausted Lovable credits. Do not confuse its login page with this GitHub/Vercel backend.
