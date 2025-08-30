"""Client-side helpers for fp.

Provides convenience functions to obtain a fingerprint and optionally send it
via HTTP to a remote endpoint. Only standard library modules are used so the
module remains lightweight.
"""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict, Optional
from urllib.error import URLError

from . import fingerprint


def get_fingerprint() -> str:
    """Return the local machine fingerprint."""
    return fingerprint()


def post_fingerprint(
    url: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 5,
) -> Dict[str, Any]:
    """Send the fingerprint to ``url`` and return the decoded JSON response.

    Parameters
    ----------
    url: str
        Endpoint that accepts a JSON body.
    data: Optional[Dict[str, Any]]
        Extra key/value pairs to include in the request body.
    headers: Optional[Dict[str, str]]
        Optional HTTP headers. ``{"Content-Type": "application/json"}``
        is used by default.
    timeout: int
        Timeout in seconds for the request; defaults to ``5``.
    """
    payload: Dict[str, Any] = {"fingerprint": get_fingerprint()}
    if data:
        payload.update(data)
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers or {"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            try:
                return json.loads(resp.read().decode("utf-8"))
            except json.JSONDecodeError as exc:
                raise ValueError("Response returned invalid JSON") from exc
    except URLError as exc:
        return {
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            }
        }
    except TimeoutError as exc:
        return {
            "error": {
                "type": exc.__class__.__name__,
                "message": str(exc),
            }
        }
