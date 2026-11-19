# Publishing the Gazette website

**Status checked 19 November 2026:** `https://parris-tech-services.github.io/RepublicOfParristan/` returned **HTTP 404**. The website is **not live**. Do not announce an address until it loads.

## One-time setup (needs a repository admin — Josh or Glenn)

1. Merge the branch that adds `.github/workflows/deploy-pages.yml`.
2. On GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. If the repository is private under an Enterprise trial, check that Pages is allowed for the organisation (**Organisation settings → Pages**). Public repositories work on all plans.
4. **Actions → Deploy Gazette to GitHub Pages → Run workflow.**
5. Open the URL shown in the workflow's summary. Check the home page, one notice and the 404 page.

Alternative without Actions: Settings → Pages → Source: *Deploy from a branch* → `main` / `/docs`. Use one method, not both.

## After it is live

- Record the date it was confirmed live, and by whom, in `NATIONAL_OPERATIONS_TODO.md` item 34, then tick it.
- Add the live link to `README.md`.
- A custom domain (for example a `.au` or other domain) needs a `docs/CNAME` file and DNS records; only do this after the founders decide who owns the domain (see [admin access](ADMIN_ACCESS_SETUP.md)).

## Rollback

Disable the workflow or set Pages source to *None*. Re-running the workflow on an earlier commit republishes that version.
