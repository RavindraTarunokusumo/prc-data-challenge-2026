"""PRC Data Challenge 2026 research package."""

import os

# The competition files were written from R; polars warns about an unknown extension type.
# Polars reads this at import time, so import `prc` before `polars`.
os.environ.setdefault("POLARS_UNKNOWN_EXTENSION_TYPE_BEHAVIOR", "load_as_storage")
