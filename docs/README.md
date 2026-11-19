# Public Gazette Website — GitHub Pages

This static website has no backend, account system, tracking, data collection or external dependencies.

## Publishing

Repository: [Parris-Tech-Services/RepublicOfParristan](https://github.com/Parris-Tech-Services/RepublicOfParristan).

Once the main branch contains these files, enable Pages in [repository Settings → Pages](https://github.com/Parris-Tech-Services/RepublicOfParristan/settings/pages):
- **Source:** Deploy from a branch
- **Branch:** `main`
- **Folder:** `/docs`
- **Save**

Expected URL after successful deployment: https://parris-tech-services.github.io/RepublicOfParristan/

This URL must not be described as live until verified. The `docs/.nojekyll` file makes the static HTML straightforward to deploy.

## Editorial workflow

- Issue a unique, sequential notice ID as a dated Markdown file under `gazette/YYYY/`.
- Add the notice to `gazette/INDEX.md`.
- Add a matching public HTML page in `docs/notices/`.
- Link the notice from `docs/index.html`.
- Clearly state *proposal*, *consultation*, *adopted* or *correction*.
- Never backdate a decision or imply a legal effect without evidence.
- Use a dated erratum for substantive historical corrections.

This site does not accept membership applications. Keep private contact and eligibility data outside the repository.
