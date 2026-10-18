# Run Family Line locally

This is the completed presentation prototype. The app is local and single-household. Existing project data stays in `data/`; do not replace that folder to reproduce a fresh case.

## Dashboard from a clean checkout

Use Python 3.11+ and `uv`. The original local demo used Python 3.12. From the repository root:

```sh
uv sync --locked
uv run python scripts/prepare_demo.py --data-dir ./data
uv run python main.py
```

Open http://127.0.0.1:8778/. The preparation script loads the fictional June/Emma household’s TV context, licensed photo and notes. It makes no model requests or calls, creates no pretend real call history and refuses a nonempty directory. Complete the sample-family onboarding in the browser.

For the original project, which already has data, skip preparation and start the app directly. For a separate replay dataset:

```sh
uv run python scripts/prepare_demo.py --data-dir ./data/replay
FAMILY_DATA_DIR=./data/replay uv run python main.py --port 8779
```

Always use the same `FAMILY_DATA_DIR` for the dashboard and phone process. Run one instance per data directory while demonstrating, so background jobs and listener ownership are clear.

## OpenAI intake

Use **Connections** in the dashboard to enter a provider key and available model. This powers family-side chat, image/scanned-PDF understanding and microphone transcription. The default model name is `gpt-4.1-mini`; the saved selection is preserved. Transcription uses `gpt-4o-mini-transcribe`.

The key is stored in `<data-directory>/.provider.json` with file permissions 0600. It is not returned by `/api/state` or stored in browser storage. `OPENAI_API_KEY` is a fallback when no local provider file exists. Do not put a key in the repository or a presentation screenshot.

No key is required merely to browse the prepared household. An unconfigured provider produces a visible error for AI intake.

## Guava phone access

Install the Guava CLI, authenticate with your own account and configure an inbound project with an assigned phone number. The local original project already has its binding in the ignored `guava.toml`.

For a new checkout, Guava can scaffold a separate setup directory so it does not replace this application:

```sh
guava login
guava create ../family-line-guava
```

In the prompts, choose the inbound Python project and your account’s phone number. Copy **only** the generated `guava.toml` into the Family Line repository. [`guava.toml.example`](guava.toml.example) shows the expected fields; placeholder IDs will not work. `guava numbers list` lists numbers available to your account.

Then, from the Family Line repository:

```sh
guava run . -- --phone
```

Keep the process running and call the configured number. The same process starts the dashboard, phone listener and reminder worker. Use `Ctrl+C` to stop it.

Optional modes:

```sh
guava run . -- --chat
guava run . -- --voice
```

The first is Guava text chat; the second uses the local microphone. Neither is the main dashboard/phone presentation mode.

Guava’s conversation service and the dashboard’s OpenAI intake are separate integrations. Configuring the OpenAI key does not configure a Guava phone number.

## Demonstrating the case

The main interface has two tabs:

- **Overview:** requests needing attention and the latest call. Older calls, reminders and activity are secondary.
- **Family assistant:** continuous chat, attachment/URL intake, reviewed handovers and saved source material.

Follow the [TV walkthrough](DEMO_WALKTHROUGH.md), [solo presentation](PRESENTATION_SCRIPT.md) or [video/caller script](VIDEO_SCRIPT_4MIN.md). Use the local configuration’s phone number; numbers appearing in archived presentation material refer to the original account.

A clean fixture has household knowledge but no actual calls. To show a real transcript/request, make a new call and show its actual saved result. The existing sample-call API creates labeled simulation data, not telephone evidence.

## Reminder and parcel boundaries

The worker checks for due jobs every two seconds. Dashboard reminders are persistent. Phone reminders require phone mode, an explicitly configured test recipient and an explicitly scheduled job. An attempted call is not proof that anyone answered. Interrupted calls do not automatically redial.

The parcel routes simulate shipment transitions; they do not fetch live carrier status. Automatic smart-home, Apple Watch and family-escalation workflows are future ideas.

## Local verification

```sh
uv run python -m pytest -q
```

Tests use temporary data, placeholder credentials and mocked provider behavior. The source also retains `--verify-live` helpers; those are optional real-provider checks, may use account quota and are not run by the ordinary test command. Do not run them solely to read the project.

See [verification evidence](docs/VERIFICATION.md) for exactly what was checked at wrap-up.

## Data and backup

`data/family.db` is the persistent SQLite database; `data/uploads/` holds originals. `FAMILY_DATA_DIR` overrides both and the provider config location. These are local-only and ignored by Git, along with logs, caches, account bindings and the earlier `todos.jsonl`.

For a backup, stop the app before copying the entire data directory, or use SQLite’s backup API while running. Do not copy just a live `.db` file and assume the WAL has been included. Repository clones reconstruct the fictional case instead of receiving your live data.
