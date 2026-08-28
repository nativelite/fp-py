# fp-py
A device fingerprinting module built entirely on the Python standard library —
**zero runtime dependencies**.

The library mirrors the goals of `fp-js` but is implemented using only Python's
standard library—no external dependencies are required. It gathers a selection
of system attributes—such as CPU details, locale, network information, and
OS-provided machine identifiers—and hashes them into a stable fingerprint.

## Usage

```python
import fp

print(fp.fingerprint())
# Inspect the raw components used for the fingerprint
print(fp.get_components())
```

To run from the command line:

```bash
python -m fp            # print the fingerprint
python -m fp --components  # inspect the raw data
```

## Sending fingerprints to a server

The optional `fp.client` helpers can transmit a fingerprint to an HTTP endpoint
using only the standard library:

```python
from fp.client import post_fingerprint

resp = post_fingerprint("https://example.com/api/fp")
print(resp)
```

You can also retrieve the value directly with `fp.client.get_fingerprint()` if
you prefer to handle network communication yourself.

## Installation

```bash
pip install fp-py            # from a checkout: pip install .
```

`fp-py` has **zero runtime dependencies** — it imports only the Python standard
library. This is declared in `pyproject.toml` (`dependencies = []`) and enforced
in CI by `tools/dep_guard.py`.

## Development

Run the full dev loop locally — no external services, no paid tooling:

```bash
python -m pip install -e ".[dev]"   # one-time (adds coverage, dev-only)
python dev.py check                 # zero-dependency guard + unittest suite
python dev.py cov                   # tests + coverage report
```

`dev.py` is a stdlib-only runner (`python dev.py {check,test,cov,guard}`). CI runs
the same `unittest` suite across Python 3.9–3.13 plus the dependency guard.
