# Tapo P115 TPAP v2 — experimental Home Assistant integration

## Compatibility validation (19 October 2026)

Both plugs have now been **read successfully on Windows 11** using the
SHA-pinned experimental TPAP branch from
[python-kasa PR #1592](https://github.com/python-kasa/python-kasa/pull/1592).

| Room | IP | Hardware | Firmware | Local read |
|---|---|---|---|---|
| P115 A | `192.0.2.10` | P115 EU v1.0 | 1.4.0 Build 251020 | PASS |
| P115 B | `192.0.2.11` | P115 EU v1.0 | 1.4.8 Build 260804 | PASS |

Both devices expose state, current consumption (W), voltage (V), current
(A), today's and this month's energy (kWh). One P115 reported live electrical measurements in the read-only test.

**No actual relay ON/OFF command was sent during verification.**

## Architecture

- Standalone `tapo_tpap` integration domain, separate from HA's built-in
  `tplink` integration.
- No MQTT broker, Windows process or LXC is required for runtime operation.
- Individual config entries for both P115 IP addresses.
- Polling coordinator with per-device sensors and opt-in outlet relay entity
  (relay switch is **disabled by default**).
- The experimental TPAP code is **vendored under a private package namespace**
  `custom_components.tapo_tpap._vendor.kasa`. No global `kasa` replacement.
- Vendored source built by GitHub Actions from an exact upstream commit
  `e7084472972f08f2e2235b342f3964aedbfaeb3b`, preserving
  original GPL-3.0-or-later license attribution.
- Dependency requirements list only supplementary crypto libraries, not
  `python-kasa` itself.

### Build pipeline

[Preview build workflow](https://github.com/razvanu/python-kasa/actions/workflows/build-tapo-hacs.yml)

The pipeline compiles all vendored modules and verifies a smoke import that
does **not** load or modify the globally installed `kasa` module.
The resulting `tapo-tpap-hacs-preview.zip` is a **preview artifact**,
not yet a supported HACS release.

## Important: not yet tested inside Home Assistant

A successful Python import is **not** proof that config flow, HA entity
registries, polling and writes work as expected under Home Assistant OS
2026.10.1. A staged Home Assistant test is still required before recommending
installation on the production HA server.

### Release criteria

1. Run an HA 2026.10.1 integration test using the generated isolated vendor.
2. Confirm sensors report correct units and device state for each firmware.
3. Exercise write enable/disable on a non-critical appliance only.
4. Package and publish as a standalone HACS repository, with downloadable
   release (current repo is still a fork of python-kasa).

### AC safety

For air conditioner, use Broadlink IR for normal air-conditioner ON/OFF.
Do **not** routinely cut the AC mains power at its P115 relay.
