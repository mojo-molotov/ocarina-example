# Ocarina example

An end-to-end test suite that demonstrates the [Ocarina](https://github.com/mojo-molotov/ocarina) browser test automation framework against a live demo site.

## What this runs against

The suite targets **Igoristan**, a public demo application hosted on GitHub Pages at <https://mojo-molotov.github.io/igoristan>.  
No local server is required: tests drive the real site over the network.  
The demo exposes:
- a homepage,
- a dashboard with OTP-based login,
- a file upload page,
- a Pokédex ("Corsicamon"),
- and several intentionally chaotic pages used to exercise Ocarina's retry and match-page features, such as:
  - random errors, 
  - random loaders, 
  - flaky forms

## Prerequisites

- Python **3.14+**.
- A WebDriver binary on disk. The CI pipeline uses **geckodriver 0.35.0** with Firefox.
- A running **Redis 6+** instance, used to coordinate OTP fetches across parallel workers. `docker run -p 6379:6379 redis:8` is enough locally.
- An `IGOR_API_KEY` value, required by tests that retrieve one-time passwords from the Igoristan OTP API. Host your own [tests workers](https://github.com/mojo-molotov/tests-workers) on Vercel.

## Setup

```bash
git clone https://github.com/mojo-molotov/ocarina-example
cd ocarina-example

make create-venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
make install

pip install --index-url https://test.pypi.org/simple/ ocarina

cp .env.example .env
# then edit .env with your values
```

The `ocarina` package is published on TestPyPI (not PyPI) during active development, so it must be installed separately after `make install`.

## Environment variables

Read from `.env` via `python-dotenv`. Values below come from [`.env.example`](.env.example).

| Variable | Purpose |
| --- | --- |
| `DASH_USERNAME` | Dashboard username (sample value: `SacredFigatellu`). |
| `DASH_PASSWORD` | Dashboard password (sample value: `figatellu`). |
| `IGOR_API_KEY` | Secret key used to retrieve OTP codes from the Igoristan API. |
| `REDIS_URL` | Redis connection string, e.g. `redis://localhost:6379`. |

## Running the suite

1. Start Redis.
2. Download the matching WebDriver binary (e.g. `geckodriver`) and place it at the repo root, or pass an absolute path via `--driver-path`.
3. Run the entry point:

```bash
python -u ./src/main.py \
  --driver-path ./geckodriver \
  --browser firefox \
  --workers 3
```

Headless mode is the default; pass `--not-headless` to see the browsers. All other flags (`--wait-timeout`, `--profile-path`, `--logger`, etc.) come straight from Ocarina's opinionated Selenium CLI: see the framework README for the complete list.

The exit code is `0` on success and `1` if any test fails, so the command is CI-friendly as-is.

## Artifacts

A run writes all the following under the repo root:

- `.reports/tests_docx_output/` — DOCX proof documents.
- `.reports/tests_json_output/` — JSON results.
- `.ocarina_logs/` — structured log files.
- `.screenshots/` — screenshots captured on failure and at explicit checkpoints.

## Project layout

```
src/
├── main.py                         # entry point: CLI → driver pool → bootstrap(cycle)
├── pages/                          # Page Object Models (POMBase subclasses)
├── api/                            # API clients (e.g. OTP retrieval)
├── caches/                         # L1 in-memory cache + cache-key reservation
├── constants/                      # URLs, Redis keys, transient error sets
├── lib/
│   ├── connectors/test_steps/      # pure action functions operating on POMs
│   ├── custom_errors/              # HttpErrorPageReachedError, TransientError, …
│   └── ext/                        # adapters for Ocarina, Redis, Selenium extras
└── tests/
    ├── cycles/                     # TestCycle definitions (e2e)
    ├── campaigns/                  # TestCampaign definitions
    ├── suites/                     # TestSuite definitions
    └── scenarios/                  # Scenario factories and test datasets
```

## Continuous integration

Two GitHub Actions workflows live in [`.github/workflows/`](.github/workflows):

- [`main_ci.yml`](.github/workflows/main_ci.yml) — runs on every push and PR to `main`, across Ubuntu and Windows with Python 3.14. Executes `make check-coding-style` (mypy + ruff) only; no browser tests.
- [`e2e.yml`](.github/workflows/e2e.yml) — manual-dispatch workflow that spins up a Redis service, installs Firefox + geckodriver, runs the full suite, and uploads `.screenshots/`, `.ocarina_logs/`, and `.reports/`. `IGOR_API_KEY` is read from the `OC` GitHub environment.

## Development

```bash
make check-coding-style   # mypy + ruff
make ruff-check           # lint only
make ruff-format          # apply formatting
make clean                # remove .venv, caches, egg-info
```

Pre-commit hooks (ruff, mypy) are installed by `make install`.

## License

MIT — Igor Casanova.

---

Built by [@mojo-molotov](https://github.com/mojo-molotov)  
Fueled by figatellu and Квас.
