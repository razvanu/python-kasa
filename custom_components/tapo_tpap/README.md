# Experimental Tapo P115 HACS integration

**Status: prototype — NOT YET READY FOR INSTALLATION.** It has not been tested on Home Assistant. No hardware control was performed.

- Separate integration domain `tapo_tpap`, independent from built-in `tplink`.
- Intended for P115 at `192.168.10.186` (fw 1.4.0) and `192.168.10.150` (fw 1.4.8).
- Adds a config entry per plug, power/voltage/current/daily/monthly sensors, and a switch disabled by default.
- The only confirmed TPAP communication is **Windows kasa CLI read-only at .186**.
- Firmware 1.4.8 on .150 has **NOT** been tested with the experimental transport.
- Does not install or override the global `python-kasa` dependency.

## Blocking issue

The official Home Assistant `python-kasa` does not support TPAP v2 for these plugs.
This prototype will **not** load the P115 entries until a compatible isolated
TPAP library can be packaged. Installing
`python-kasa @ git+https://github.com/ZeliardM/python-kasa.git@...` from
`manifest.json` would overwrite HA's **shared** `kasa` library and could
affect the existing Kasa HS100/HS110 integrations. We deliberately do not do it.

Upstream TPAP work: https://github.com/python-kasa/python-kasa/pull/1592

## Release criteria

1. Isolate TPAP implementation from HA's shared kasa Python package.
2. Prove read-only P115 .186 and .150 connections, firmware versions 1.4.0/1.4.8.
3. Verify HA 2026.10.1 startup, config flow, sensors, error recovery.
4. Explicitly opt-in and hardware-test relay writes on non-critical loads.
5. Publish as a **dedicated** HACS repository (not inside full python-kasa fork).

## Normal Tesla operation

Do not cut mains power to the Tesla AC with the P115 switch during compressor operation.
Use the existing Broadlink IR controls; the P115 is for telemetry.
