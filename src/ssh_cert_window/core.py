from __future__ import annotations
import datetime as dt
import re
import subprocess
from pathlib import Path

_VALID = re.compile(r"^\s*Valid:\s*from\s+(.+?)\s+to\s+(.+?)\s*$", re.M)

def _date(value: str) -> dt.datetime:
    value = value.strip().replace(" UTC", "+00:00").replace("Z", "+00:00")
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)

def parse_key_info(text: str, now: dt.datetime | None = None, warn_days: int = 14) -> dict:
    match = _VALID.search(text)
    if not match:
        raise ValueError("ssh-keygen output has no recognizable Valid: from ... to ... line")
    start, end = _date(match.group(1)), _date(match.group(2))
    now = (now or dt.datetime.now(dt.timezone.utc)).astimezone(dt.timezone.utc)
    principals_block = re.search(r"^\s*Principals:\s*\n((?:\s+.+\n)*)", text, re.M)
    principals = [line.strip() for line in principals_block.group(1).splitlines() if line.strip()] if principals_block else []
    def field(name: str) -> str | None:
        m = re.search(rf"^\s*{re.escape(name)}:\s*(.+)$", text, re.M)
        return m.group(1).strip().strip('"') if m else None
    if now < start:
        status = "NOT_YET_VALID"
    elif now >= end:
        status = "EXPIRED"
    elif end - now <= dt.timedelta(days=warn_days):
        status = "EXPIRING_SOON"
    else:
        status = "VALID"
    return {"status": status, "type": field("Type"), "key_id": field("Key ID"), "serial": field("Serial"), "principals": principals, "valid_after": start.isoformat(), "valid_before": end.isoformat(), "days_remaining": max(0, int((end-now).total_seconds() // 86400)) if now < end else 0}

def inspect_certificate(path: str | Path, warn_days: int = 14, now: dt.datetime | None = None) -> dict:
    proc = subprocess.run(["ssh-keygen", "-L", "-f", str(path)], text=True, capture_output=True, timeout=10)
    if proc.returncode:
        raise RuntimeError(proc.stderr.strip() or "ssh-keygen could not read certificate")
    return parse_key_info(proc.stdout, now=now, warn_days=warn_days)
