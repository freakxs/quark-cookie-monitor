---
name: quark-cookie-monitor
description: Validate and monitor the owner's Quark Drive web Cookie with a minimal read-only request. Use when the user asks whether their Quark Cookie is valid or wants a low-frequency expiry alert. Never automate login, extract browser credentials, refresh sessions, or perform file operations.
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [quark-drive, cookie, monitoring, blueprint]
    blueprint:
      schedule: "37 10 * * *"
      deliver: origin
      prompt: "Use the quark-cookie-monitor skill. Run `python3 ${HERMES_SKILL_DIR}/scripts/check_cookie.py --quiet-success`. If it succeeds, respond exactly [SILENT]. If it reports expired or missing credentials, send a concise Chinese alert asking the owner to replace QUARK_COOKIE in Dashboard > Keys > Custom Keys. If the network or API is inconclusive, report that without calling the Cookie expired. Never print the Cookie."
      no_agent: false
required_environment_variables:
  - name: QUARK_COOKIE
    prompt: "Paste your own Quark Drive Cookie"
    help: "Copy it manually from your own authenticated Quark Drive web session. Never send it through chat."
    required_for: "Read-only Cookie validity check"
---

# Quark Cookie Monitor

Run the bundled deterministic checker:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/check_cookie.py
```

For scheduled checks, use `--quiet-success`. Exit codes are:

- `0`: valid; quiet when requested.
- `1`: expired or rejected.
- `2`: `QUARK_COOKIE` is missing.
- `3`: network failure or unknown response; do not call it expired.

## Safety boundary

- Use only the owner's account and `QUARK_COOKIE` supplied through Hermes secret configuration.
- Never request or repeat the Cookie in chat, logs, prompts, tool output, source files, or command arguments.
- Never inspect browser storage, automate login or QR confirmation, refresh the session, bypass verification, or operate on files/shares/downloads.
- Do not increase the default once-daily frequency to keep a session alive.
- The endpoint is an undocumented web API. Its behavior can change, and this workflow cannot guarantee zero account risk.

If the secret is missing in a gateway or messaging session, direct the owner to Hermes Dashboard → Keys → Custom Keys and create `QUARK_COOKIE`. Hermes messaging sessions must not collect secrets in-band.
