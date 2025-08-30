# fp-py
A fast, lightweight device fingerprinting module that is anti-bloat.

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
