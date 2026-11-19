# Parristan Private Assembly — deployment verification

**Checked 19 November 2026, 18:10 AEDT (approximate).** This is an engineering record, **not a vote, published nomination notice, certified election or Assembly decision**.

## Verified source and tests

- [Private voting source](README.md) merged by [PR #28](https://github.com/Parris-Tech-Services/RepublicOfParristan/pull/28), commit `41415020d5d26095b2936c0793ab15b642c1e1ae`.
- Both "Validate Public Gazette" and "Validate Private Voting" passed on the final PR commit `b534be68` ([private-voting CI](https://github.com/Parris-Tech-Services/RepublicOfParristan/actions/runs/44478060630)).
- Eight pure rule tests cover ordinary majority, minimum 3 voters, abstention, 48h close, 14d amendments, two-thirds thresholds, single-candidate confirmation, runoff, voting windows and count consistency.
- Neon Postgres database `parristan_ballots` exists separately from the pre-existing application database `neondb`; least-privilege app role `parristan_voter_app` can read its five seeded founder records.
- **No ballots or polls have been recorded** in the new database at initial verification.
- Vercel project `parristan-private-assembly`, id `prj_FdE3qLGmIpjo94tAUlYXk1oLIfTB`, is linked to the GitHub repository with root `apps/private-voting`; production DATABASE_URL and BOOTSTRAP_KEY stored as sensitive environment variables; `SECRET_ELECTIONS_ENABLED=false`.

## Blocker

First production deployment was rejected by Vercel with HTTP **402 `api-deployments-free-per-day`**: this Hobby team exceeded its daily 100-deployment limit. Vercel recommended retrying after 24 hours or resolving plan limits. **No production URL, login test, independent security assessment or live ballot can be claimed until deployment and runtime checks pass.** Do not buy an upgrade automatically. Railway reported an expired trial; Replit reported too many apps; Lovable reported no remaining credits.

## Operational verification still required

- [ ] Vercel production deployment reaches READY, with exact commit SHA and a real deployment URL.
- [ ] Public app shell loads via HTTPS and unauthenticated ballot data remains inaccessible.
- [ ] Bootstrap is performed **once** by the actual organiser using the separately provided private code; code is never published or retained in this repo.
- [ ] Registrar and joint admins confirm actual founder membership, permissions and issue private one-use invitations.
- [ ] Test each founder's sign-in, sign-out, role restrictions, CSRF and session expiry on the live deployment.
- [ ] Use test-only or isolated verification data to confirm atomic duplicate-vote prevention, officer approval gates, quorum, 48h close, amendment 14d notice, confidential tally access and independent count verification; do not invent public governance actions.
- [ ] Secretary confirms a live voting portal is adopted as an authorised method in the official encrypted Matrix channel. The current Motion 4 authorises channel votes, not automatically this separate site.
- [ ] Matthew Walker specifies actual opening/closing times, secret-ballot method, eligibility, challenge procedure and certified candidacies; an independent security review confirms privacy acceptability for only five voters.
- [ ] Only then consider enabling official presidential/office elections. Default remains `SECRET_ELECTIONS_ENABLED=false`.

**Rollback:** keep official votes in the Matrix channel and, when approved, on paper until technical and procedural checks are complete. The new site must not override 19 November decisions or act as an election result simply because software exists.
