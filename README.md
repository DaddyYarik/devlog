# devlog

> Stop wondering what you did yesterday.

`devlog` is a dead-simple CLI that logs what you work on throughout the day and generates a clean standup report in seconds — no accounts, no cloud, no nonsense.

```
$ devlog standup

╭──────────────── Standup Report ─────────────────╮
│ ✅  Done (yesterday)                             │
│    • fixed login redirect bug                    │
│    • deployed new /users endpoint                │
│                                                  │
│ 🔨  Doing (today)                                │
│    • reviewing PR from @alice                    │
│    • writing unit tests for auth module          │
│                                                  │
│ 🚧  Blockers                                     │
│    • waiting on design mockups                   │
╰──────────────────────────────────────────────────╯
```

---

## Install

```bash
pip install devlog-cli
```

## Quick start

```bash
# Log what you're doing as you work
devlog add fixed the login redirect bug
devlog add -t backend deployed new /users endpoint
devlog add -t blocked waiting on design mockups from Alice

# Check today's work
devlog today

# Next morning — generate standup in one command
devlog standup
```

## All commands

| Command | Description |
|---|---|
| `devlog add <message>` | Add a log entry |
| `devlog add -t TAG <message>` | Add entry with tag (use `blocked` for blockers) |
| `devlog today` | Show today's entries |
| `devlog yesterday` | Show yesterday's entries |
| `devlog standup` | Print standup report |
| `devlog week` | Show this week's overview |
| `devlog ls` | List recent entries (last 7 days) |
| `devlog ls -d 30` | List entries from last 30 days |
| `devlog delete <id>` | Delete an entry by ID |

## How it works

Entries tagged with `-t blocked` automatically appear in the **Blockers** section of the standup report. Everything else goes into Done (yesterday) and Doing (today).

```bash
devlog add -t blocked waiting on API keys from DevOps
#                   ↑ this entry appears under Blockers in standup
```

## Why devlog?

- **Zero config** — works out of the box, no setup required
- **Local-first** — logs stored in `~/.devlog/logs.json`, your data stays yours
- **No internet required** — 100% offline
- **Tiny** — two dependencies: `click` + `rich`
- **Standup-ready** — copy-paste the standup output directly into Slack or Teams

## Data

All entries are stored locally in `~/.devlog/logs.json` as plain JSON. You own your data.

```json
[
  {
    "id": "a1b2c3d4",
    "timestamp": "2026-06-13T10:23:45",
    "date": "2026-06-13",
    "message": "fixed login redirect bug",
    "tags": []
  }
]
```

## License

MIT
