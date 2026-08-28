"""Tests for fp.client (stdlib unittest + mock; no live network)."""
from __future__ import annotations

import json
import unittest
from unittest import mock
from urllib.error import URLError

from fp import client


def _fake_response(body: bytes):
    resp = mock.MagicMock()
    resp.read.return_value = body
    cm = mock.MagicMock()
    cm.__enter__.return_value = resp
    return cm


class GetFingerprintTests(unittest.TestCase):
    def test_delegates_to_fingerprint(self):
        with mock.patch("fp.client.fingerprint", return_value="x" * 64):
            self.assertEqual(client.get_fingerprint(), "x" * 64)


class PostFingerprintTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("fp.client.get_fingerprint", return_value="fp123")
        self.addCleanup(patcher.stop)
        patcher.start()

    def test_success_returns_decoded_json(self):
        with mock.patch("fp.client.urllib.request.urlopen",
                        return_value=_fake_response(b'{"ok": true}')):
            self.assertEqual(client.post_fingerprint("http://x"), {"ok": True})

    def test_merges_extra_data_into_payload(self):
        captured = {}

        def fake_urlopen(req, timeout=5):
            captured["body"] = json.loads(req.data.decode("utf-8"))
            return _fake_response(b'{}')

        with mock.patch("fp.client.urllib.request.urlopen", side_effect=fake_urlopen):
            client.post_fingerprint("http://x", data={"user": "a"})
        self.assertEqual(captured["body"], {"fingerprint": "fp123", "user": "a"})

    def test_invalid_json_raises_valueerror(self):
        with mock.patch("fp.client.urllib.request.urlopen",
                        return_value=_fake_response(b'not json')):
            with self.assertRaises(ValueError):
                client.post_fingerprint("http://x")

    def test_urlerror_returns_error_dict(self):
        with mock.patch("fp.client.urllib.request.urlopen",
                        side_effect=URLError("boom")):
            out = client.post_fingerprint("http://x")
        self.assertEqual(out["error"]["type"], "URLError")

    def test_timeout_returns_error_dict(self):
        with mock.patch("fp.client.urllib.request.urlopen",
                        side_effect=TimeoutError("slow")):
            out = client.post_fingerprint("http://x")
        self.assertEqual(out["error"]["type"], "TimeoutError")


if __name__ == "__main__":
    unittest.main()
