import argparse
from pathlib import Path
import unittest

from tapo_control import build_command


class SafetyTests(unittest.TestCase):
    def args(self, action, allow_write=False, confirm_host=None):
        return argparse.Namespace(host="192.0.2.10", kasa=Path("kasa.exe"),
                                  action=action, allow_write=allow_write,
                                  confirm_host=confirm_host)

    def test_read_without_confirmation(self):
        self.assertEqual(build_command(self.args("status"))[-1], "state")

    def test_on_requires_write_flag(self):
        with self.assertRaises(PermissionError):
            build_command(self.args("on"))

    def test_off_requires_matching_ip(self):
        with self.assertRaises(PermissionError):
            build_command(self.args("off", True, "192.0.2.11"))

    def test_explicit_write(self):
        self.assertEqual(build_command(self.args("on", True, "192.0.2.10"))[-1], "on")


if __name__ == "__main__":
    unittest.main()
