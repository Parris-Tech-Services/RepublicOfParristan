# Verified Reference Software Stacks — France and Schleswig-Holstein

Research date: 19 November 2026. This is a matrix of **publicly documented products**, not an assertion that their full internal stacks, images, versions or configurations are public. Parristan has **not deployed or adopted** these systems as government policy. Any choices below are proposals subject to actual approval and testing.

## French National Gendarmerie

| Function | Publicly reported software | Parristan candidate |
| --- | --- | --- |
| Workstation OS | GendBuntu, tailored Ubuntu GNU/Linux | Supported Ubuntu LTS pilot, not a copy of undisclosed GendBuntu configuration |
| Server OS | Debian GNU/Linux | Debian for future small services |
| Office | OpenOffice.org originally; later LibreOffice | LibreOffice, ODF and PDF exports |
| Browser | Mozilla Firefox | Firefox |
| Email client | Mozilla Thunderbird | Thunderbird |
| Graphics | GIMP | GIMP where needed |
| Video/audio | VLC | VLC where needed |
| Data store | PostgreSQL | PostgreSQL only for a genuine application need |
| Other line-of-business software | Mixed internal and specialist systems | Do not invent an exhaustive or identical deployment |

Sources: [European Commission OSOR: Ubuntu migration](https://interoperable-europe.ec.europa.eu/collection/open-source-observatory-osor/document/towards-freedom-operating-system-french-gendarmerie-goes-ubuntu), [OSOR: server OS and PostgreSQL](https://interoperable-europe.ec.europa.eu/collection/open-source-observatory-osor/news/technological-sovereignty), [OSOR: desktop applications](https://interoperable-europe.ec.europa.eu/collection/open-source-observatory-osor/news/french-gendarmerie-open-sou).

## Schleswig-Holstein state administration, Germany

| Function | Product | Public position by November 2026 |
| --- | --- | --- |
| Office | LibreOffice | Largely migrated in 2025; specialist compatibility exceptions remain |
| Mail/groupware | Open-Xchange | Completed statewide government mailbox migration announced October 2025 |
| Email client | Thunderbird | Part of the completed email migration |
| Collaboration/files | Nextcloud | Deployment expanding; not verified as completely rolled out |
| Video conferencing | OpenTalk | State reported migration completed in 2025 |
| Workstation OS | GNU/Linux | State Chancellery transitioned in September 2026; other agencies following gradually |
| Directory/identity | Univention Nubus | Further introduction planned/under way, not verified complete |
| Interoperability | Univention AD Connector | Mentioned in official 2024 transition design |
| Telephony | OSKAR | Further migration planned, not verified complete |
| Hosting/support | Dataport and external Linux specialists | Operational/service relationships, not a claim of an exact software product |

Primary sources: [Government announcement 2024](https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/I/Presse/PI/2024/CdS/240403_cds_it-arbeitsplatz.html), [Government email migration announcement 2025](https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/I/Presse/PI/2025/cds/251006_cds_ox.html), [Government Linux rollout status 19 September 2026](https://www.schleswig-holstein.de/DE/landesregierung/ministerien-behoerden/I/Presse/PI/2026/cds/260919_cds_linux_stk), [European Commission review](https://interoperable-europe.ec.europa.eu/collection/open-source-observatory-osor/news/schleswig-holsteins-open-source-strategy-year).

## Proposed Parristan implementation order

1. **Developer PC (now):** Windows PowerShell, Git, Python, Pi coding agent + OpenRouter/Qwen, repo validation and GitHub PRs. This does not imply a Windows-to-Linux rollout.
2. **One office pilot:** Ubuntu LTS or Debian, Firefox, LibreOffice, Thunderbird, ODF/PDF, accessibility testing, backup and restore.
3. **Small-team collaboration pilot:** Nextcloud, OpenTalk if justified, standards-based email/calendar and export tests.
4. **Only when supported by actual demand:** Open-Xchange, Univention Nubus, central identity, PostgreSQL applications, managed Linux images and dedicated support.

Use explicit labels: **reference**, **proposed**, **pilot**, **approved**, or **operational (with date and proof)**. Verify open licensing, privacy, accessibility, support, interoperability, backup recovery and realistic costs. No software stack creates sovereignty or public authority.
