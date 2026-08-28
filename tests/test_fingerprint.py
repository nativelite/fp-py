"""Tests for fp core fingerprinting (stdlib unittest only)."""
from __future__ import annotations

import hashlib
import io
import unittest
from unittest import mock

import fp


class FingerprintTests(unittest.TestCase):
    def test_fingerprint_is_64_char_hex(self):
        digest = fp.fingerprint()
        self.assertEqual(len(digest), 64)
        int(digest, 16)  # raises if not hex

    def test_fingerprint_deterministic_for_fixed_components(self):
        components = {"b": "2", "a": "1"}
        raw = "|".join(f"{k}:{components[k]}" for k in sorted(components))
        expected = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        with mock.patch.object(fp, "get_components", return_value=dict(components)):
            self.assertEqual(fp.fingerprint(), expected)

    def test_get_components_returns_string_map(self):
        comps = fp.get_components()
        self.assertIsInstance(comps, dict)
        for key in ("system", "machine", "python_version", "machine_id",
                    "locale", "mac", "ip", "timezone"):
            self.assertIn(key, comps)
            self.assertIsInstance(comps[key], str)

    def test_get_components_fallbacks_on_error(self):
        with mock.patch("fp.socket.gethostbyname", side_effect=OSError), \
             mock.patch("fp.uuid.getnode", side_effect=OSError), \
             mock.patch("fp.locale.getlocale", side_effect=OSError):
            comps = fp.get_components()
        self.assertEqual(comps["ip"], "unknown")
        self.assertEqual(comps["mac"], "unknown")
        self.assertEqual(comps["locale"], "unknown")


class MachineIdTests(unittest.TestCase):
    def test_linux_reads_machine_id_file(self):
        with mock.patch.object(fp.sys, "platform", "linux"), \
             mock.patch.object(fp.Path, "read_text", return_value="abc123\n"):
            self.assertEqual(fp.machine_id(), "abc123")

    def test_darwin_parses_ioreg(self):
        out = b'"IOPlatformUUID" = "DEAD-BEEF"'
        with mock.patch.object(fp.sys, "platform", "darwin"), \
             mock.patch.object(fp.subprocess, "check_output", return_value=out):
            self.assertEqual(fp.machine_id(), "DEAD-BEEF")

    def test_unknown_when_platform_unsupported(self):
        with mock.patch.object(fp.sys, "platform", "sunos"):
            self.assertEqual(fp.machine_id(), "unknown")

    def test_unknown_on_linux_read_failure(self):
        with mock.patch.object(fp.sys, "platform", "linux"), \
             mock.patch.object(fp.Path, "read_text", side_effect=OSError):
            self.assertEqual(fp.machine_id(), "unknown")


class CliTests(unittest.TestCase):
    def _run(self, argv):
        buf = io.StringIO()
        with mock.patch.object(fp.sys, "argv", argv), \
             mock.patch("sys.stdout", buf):
            from fp.__main__ import main
            main()
        return buf.getvalue()

    def test_cli_default_prints_hash(self):
        with mock.patch("fp.__main__.fingerprint", return_value="d" * 64):
            out = self._run(["fp"])
        self.assertIn("d" * 64, out)

    def test_cli_components_prints_json(self):
        with mock.patch("fp.__main__.get_components", return_value={"a": "1"}):
            out = self._run(["fp", "--components"])
        self.assertIn('"a": "1"', out)


if __name__ == "__main__":
    unittest.main()
