"""Negative control. No config file and no inline directive names this directory,
so this marker must NEVER appear in a lint log. If it does, the probe is unsound."""
from sqlfluff.core.errors import SQLTemplaterError
raise SQLTemplaterError("PROBE9F2C_NEGATIVE_CONTROL")
