# Tapo P115 TPAP v2 — companion controls

This is an experimental companion to [python-kasa TPAP pull request #1592](https://github.com/python-kasa/python-kasa/pull/1592), not a replacement of that protocol implementation.

## Verified
- Tapo P115 `192.168.10.186`, firmware 1.4.0: read-only `kasa state` **works** with PR #1592 on Windows 11.
- Tapo P115 `192.168.10.150`: not yet tested using the experimental CLI.
- Relay ON/OFF: implemented as explicit opt-in operations, **not yet hardware-tested**.

## Install / run
Use the experimental python-kasa environment installed by the Windows test script, which provides `%USERPROFILE%\Tapo-P115-Test\.venv\Scripts\kasa.exe`.

Download `tapo_control.py` to `C:\codex-ha`, then run:

```powershell
cd C:\codex-ha
$env:KASA_USERNAME = Read-Host "Tapo email"
$env:KASA_PASSWORD = Read-Host "Tapo password"
$python = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"

# Read state; no relay operation
& $python .\tapo_control.py --host 192.168.10.186 status

# Simulate an ON operation without contacting the plug
& $python .\tapo_control.py --host 192.168.10.186 --allow-write --confirm-host 192.168.10.186 --dry-run on

# Real ON, only when explicitly intended
& $python .\tapo_control.py --host 192.168.10.186 --allow-write --confirm-host 192.168.10.186 on

# Real OFF: WARNING, cuts mains power to Tesla AC
& $python .\tapo_control.py --host 192.168.10.186 --allow-write --confirm-host 192.168.10.186 off

Remove-Item Env:\KASA_USERNAME,Env:\KASA_PASSWORD
```

Never commit credentials, tokens, MAC addresses, full diagnostic logs, or secrets.

## Safety
- Reading does not need write confirmation.
- `on` and `off` require both `--allow-write` and `--confirm-host` exactly matching the target IP.
- `--dry-run` doesn't contact the plug.
- No background service is installed.
- **Use Broadlink IR for normal Tesla AC control; do not power-cycle the compressor by cutting the smart plug.**
- MQTT/Home Assistant is a later phase, not part of this module.

Run local unit tests using `python -m unittest discover -s tests -v`.
