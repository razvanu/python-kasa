#!/usr/bin/env python3
"""Tapo P115 state reading and deliberately opt-in relay commands."""
import argparse
import ipaddress
import os
from pathlib import Path
import subprocess
import sys

DEFAULT_KASA = Path.home() / "Tapo-P115-Test" / ".venv" / "Scripts" / "kasa.exe"


def cli_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, help="Tapo IPv4 address")
    parser.add_argument("--kasa", type=Path, default=DEFAULT_KASA)
    parser.add_argument("--allow-write", action="store_true")
    parser.add_argument("--confirm-host", help="Repeat exact target IP to confirm write")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("action", choices=("status", "on", "off"))
    return parser.parse_args(argv)


def build_command(args):
    ip = str(ipaddress.IPv4Address(args.host))
    if ip != args.host:
        raise ValueError("Specify a canonical IPv4 address")
    if args.action in ("on", "off"):
        if not args.allow_write or args.confirm_host != ip:
            raise PermissionError("Write requires --allow-write and --confirm-host matching IP")
    return [str(args.kasa), "--host", ip, args.action]


def main(argv=None):
    args = cli_args(argv)
    try:
        command = build_command(args)
        if args.dry_run:
            print("DRY RUN (no device contact): " + " ".join(command))
            return 0
        if not args.kasa.is_file():
            raise FileNotFoundError(f"Cannot find experimental kasa.exe at {args.kasa}")
        if not os.environ.get("KASA_USERNAME") or not os.environ.get("KASA_PASSWORD"):
            raise RuntimeError("Set KASA_USERNAME and KASA_PASSWORD locally")
        return subprocess.run(command, check=False).returncode
    except (ValueError, PermissionError, FileNotFoundError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
