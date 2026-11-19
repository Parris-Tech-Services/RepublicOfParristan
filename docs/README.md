# Public Gazette website — Git-linked Vercel deployment and optional GitHub Pages

This static website has no backend, account system, tracking, data collection or external dependencies.

## Publishing

Repository: [Parris-Tech-Services/RepublicOfParristan](https://github.com/Parris-Tech-Services/RepublicOfParristan).

**Production:** [https://republic-of-parristan.vercel.app/](https://republic-of-parristan.vercel.app/), served from the Vercel project `republic-of-parristan`, with GitHub `main` as its production branch and `docs` as the static root. The initial Vercel production build reached READY on 19 November 2026, and connected checks returned HTTP 200 for the homepage, administration dashboard and JSON export. Production aliases are configured without Vercel Authentication; independent unauthenticated reachability was not checked.

**Optional GitHub Pages:** GitHub Pages has **not been enabled**. The existing workflow failed while looking up the Pages site. To use GitHub Pages, an authorised repo administrator can configure [Settings → Pages](https://github.com/Parris-Tech-Services/RepublicOfParristan/settings/pages) → Build and deployment → GitHub Actions, then manually run the workflow. It is deliberately not triggered on every push while it cannot deploy. The proposed Pages URL is https://parris-tech-services.github.io/RepublicOfParristan/ and remains unverified.

The site is plain static HTML/CSS/JS and can also be exported from `docs/` without Vercel or GitHub Pages.

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
