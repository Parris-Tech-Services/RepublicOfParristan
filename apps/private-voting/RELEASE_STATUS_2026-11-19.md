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
- [ ] Production deployment READY and public login page returning HTTP 200 without provider sign-in
- [ ] Production API health check and unauthenticated private-data rejection checked
- [ ] First organiser activation and five founders' account ownership verified
- [ ] Officers verify official use of this portal is adopted and compatible with Matrix/email channel
- [ ] One real end-to-end written-motion vote with quorum, double-vote rejection and certified result independently observed
- [ ] Independent election security review before any new secret electoral ballot

The deployed site can show a sign-in page to everyone while the service is private behind its **own** founder authentication. An accessible login URL does not give non-members access to ballots.

**Deployment context:** Git-linked Vercel project `parristan-private-assembly`, root `apps/private-voting`, sensitive `DATABASE_URL` and `BOOTSTRAP_KEY` stored in hosting environment. Direct deployment API returned a free-tier daily rate limit (402) on 19 November, so a source push will test the standard Git integration as an alternative. Do not claim this alternative succeeded unless a production deployment is observed as READY.

**Governance:** [Gazette 2026-013](../../gazette/2026/2026-013-first-president-confirmed.md) records Joshua Parris as President; [Gazette 2026-014](../../gazette/2026/2026-014-presidents-first-programme.md) retains Matrix debate/votes and official email for notices. The private portal must not silently replace either channel.
