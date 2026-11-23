# Parristan Living Nation — implementation checklist

> **Fictional, independent simulation.** Computer-generated residents, towns, journeys, relationships and events are not real citizenship, government decisions, elections or people.

## Numbered checklist (23 November 2026)

1. [x] Inspect the existing Republic of Parristan Gazette repository and hosting.
2. [x] Model 12 illustrative settlements with home/work sites and routes.
3. [x] Seed 500 unique fictional residents with occupations, goals, traits and finances.
4. [x] Implement autonomous time-based work, sleep, leisure, travel, friendships, career changes, memory and community stories.
5. [x] Provision a separate Cloudflare D1 database and deploy a 15-minute Cloudflare Worker cron.
6. [x] Create a mobile-responsive map, citizen search/profile and recent-event diary.
7. [x] Persist state with version-checked D1 updates and limit events to the latest 800 and memories to five per citizen.
8. [x] Separate simulated data from the real civic Gazette and membership register; expose read-only API.
9. [x] Verify CI unit tests, shared D1 state, the first 15-minute scheduled D1 update (revision 0 → 1, tick 0 → 1 on 23 Nov 2026 at 06:30 UTC), and the rendered production Vercel website.
10. [x] Merge the feature into main and verify the public Vercel-hosted page is HTTP 200 and renders 500 residents. Custom parristan.org URL was not independently reachable from the test browser.

## What's built

- **Simulation engine:** [worker.js](worker.js). Every 15 minutes a scheduled Cloudflare Worker advances one shared world. It reconstructs elapsed time in 15-minute ticks, capped at 96 per invocation; state is saved to D1. On a concurrency conflict it declines the duplicate write and retries next schedule.
- **Data:** exactly 500 fictional agent profiles, 12 named settlements, distinct homes/workplaces, current activity/location, preferences, goals, energy, mood, virtual currency, reciprocal friendships, personal memories and event history. No real personal data.
- **User interface:** [Living Nation dashboard](../docs/living-nation.html), canvas map, search, filters, profiles, latest stories, explicit update status. A previously saved snapshot can be shown as cached when the backend is inaccessible.
- **Cost:** No model/API usage is required. This is rule-based autonomous simulation, **not language-model-powered conversation**. On the applicable Cloudflare free tier, this should not incur charges within published quotas, but check actual account limits and billing.
- **Reading:** GET /api/health shows revision, population, tick count and age. GET /api/world returns the full shared state. No public write routes.
- **Cloudflare worker:** parristan-living-nation. This is simulation infrastructure, not an official government instrument.

### Live endpoints

- UI: https://parristan.org/living-nation.html (after site deployment)
- Alternative UI: https://republic-of-parristan.vercel.app/living-nation.html
- Read-only API: https://parristan-living-nation.parris-neathaustralia.workers.dev/api/world
- Health: https://parristan-living-nation.parris-neathaustralia.workers.dev/api/health

### Tests

- node --test simulation/test.mjs
- node --check simulation/worker.js
- node --check docs/living-nation.js
- python3 scripts/validate_gazette.py

The GitHub Actions workflow living-nation-tests.yml runs these checks on feature changes.

### Backend setup and redeploy

1. Create a D1 database named parristan-living-nation with a table:

    CREATE TABLE IF NOT EXISTS worlds (
      id INTEGER PRIMARY KEY CHECK (id = 1),
      revision INTEGER NOT NULL DEFAULT 0,
      state TEXT NOT NULL,
      updated_at INTEGER NOT NULL
    );

2. Deploy simulation/worker.js as a Cloudflare ES module Worker, with a D1 binding named DB.
3. Enable a cron trigger at */15 * * * * and a workers.dev subdomain.
4. Verify GET /api/health reports 500 residents and GET /api/world has fictional:true.
5. Confirm that ticks and revisions advance after the next scheduled quarter-hour. **Verified 23 Nov 2026 06:31 UTC:** D1 revision advanced 0 to 1 and simulation ticks advanced 0 to 1; the stored world updated at 06:30 UTC.

**Rollback:** Stop background execution by disabling the cron trigger. Revert the website feature commit if required. Preserve/export the D1 database before a reset; never delete the Gazette or membership records.

### Deliberate limitations / next improvements

- Travel is map-coordinate interpolation, not road-accurate routing.
- Citizens follow deterministic rules, **not independent LLM inference**. Optional Ollama storytelling or restricted language-model decisions can be added later within a budget.
- One shared fictional world, 500 agents, latest 800 story events; no account login, direct editing, real votes or external actions.
- Geography is imaginary and does not assert any territorial claim.
