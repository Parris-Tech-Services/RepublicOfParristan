# Public Gazette website — hosting and portability

This static website has no backend, account system, tracking, data collection or external dependencies.

## Publishing

Repository: [Parris-Tech-Services/RepublicOfParristan](https://github.com/Parris-Tech-Services/RepublicOfParristan).

**Primary public snapshot (published by a separate process):** [https://republic-of-parristan-gazette.joshualparris.chatgpt.site/](https://republic-of-parristan-gazette.joshualparris.chatgpt.site/). Its publication was recorded in the repository on 19 November 2026; it is a snapshot, not a verified automatic GitHub-to-site pipeline.

**Secondary Git-linked production mirror:** [https://republic-of-parristan.vercel.app/](https://republic-of-parristan.vercel.app/), Vercel project `republic-of-parristan`, production branch `main`, static root `docs`. Initial deployment was READY on 19 November 2026 and connected requests to the homepage, administration page and JSON export returned HTTP 200. Production Vercel Authentication is disabled; previews remain protected. Anonymous external reachability was not independently checked.

**Optional GitHub Pages:** Not enabled at https://parris-tech-services.github.io/RepublicOfParristan/. An administrator may activate [Settings → Pages → GitHub Actions](https://github.com/Parris-Tech-Services/RepublicOfParristan/settings/pages), then manually dispatch the existing workflow. That workflow is manual-only until configured, avoiding repeated failed push builds.

The `docs/.nojekyll` file and self-contained HTML/CSS/JS permit migration between supported static hosts. See [publishing and validation evidence](../operations/PAGES_PUBLISHING.md).

## Editorial workflow

- Issue a unique, sequential notice ID as a dated Markdown file under `gazette/YYYY/`.
- Add the notice to `gazette/INDEX.md`.
- Add a matching public HTML page in `docs/notices/`.
- Link the notice from `docs/index.html`.
- Clearly state *proposal*, *consultation*, *adopted* or *correction*.
- Never backdate a decision or imply a legal effect without evidence.
- Use a dated erratum for substantive historical corrections.

This site does not accept membership applications. Keep private contact and eligibility data outside the repository.

## Public administration and data

The read-only [administration dashboard](administration.html) shows the same eight documented founding decisions as the [public decisions page](decisions.html). A portable [JSON export](data/decisions.json) contains aggregate decisions and sources only, no member roll or ballots. The validator `python3 scripts/validate_public_records.py` checks machine-readable records against the decision register and both pages. It does not independently authenticate a vote.

## Authenticated Assembly voting (supplementary, separate application)

The `/voting/` entry point is a login-protected app and is **not part of the public Gazette's static information pages**. Its serverless endpoint `/api/voting` uses a separate private Postgres database, sensitive hosted environment variables and server-side founder access controls. No private passwords, ballots, individual participation or access tokens appear in the repository or public Gazette pages.

The Gazette and Matrix/email decisions remain authoritative. This portal must not create a second version of the 19 November presidential confirmation. A private portal ballot is not automatically an adopted official vote; officers must verify the approved method, electorate and certification. Secret officer elections remain disabled until reviewed.
