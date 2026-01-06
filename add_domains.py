#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


RAW_PATH = Path("raw_junk_email_domains.json")


def normalize_domain(value):
    value = value.strip()
    if "@" in value:
        value = value.split("@")[-1]
    return value.strip().lower()


def load_entries(payload):
    if isinstance(payload, dict):
        payload = payload.get("domains", [])
    entries = []
    for item in payload:
        if isinstance(item, dict):
            domain = item.get("domain")
            if domain:
                entries.append(
                    {"domain": domain, "added_at": item.get("added_at")}
                )
        elif isinstance(item, str):
            entries.append({"domain": item, "added_at": None})
    return entries


def main(argv):
    if len(argv) < 2:
        print("Usage: python3 add_domains.py <domain|email> [more...]", file=sys.stderr)
        return 1

    payload = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    entries = load_entries(payload)
    now = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )

    latest_by_domain = {}
    for entry in entries:
        domain = normalize_domain(entry["domain"])
        if not domain:
            continue
        added_at = entry.get("added_at")
        if not added_at:
            added_at = now
        current = latest_by_domain.get(domain)
        if current is None or added_at > current["added_at"]:
            latest_by_domain[domain] = {"domain": domain, "added_at": added_at}

    added = []
    for raw in argv[1:]:
        domain = normalize_domain(raw)
        if not domain:
            continue
        current = latest_by_domain.get(domain)
        if current is None or now > current["added_at"]:
            latest_by_domain[domain] = {"domain": domain, "added_at": now}
            added.append(domain)

    RAW_PATH.write_text(
        json.dumps(list(latest_by_domain.values()), indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Added {len(added)} domain(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
