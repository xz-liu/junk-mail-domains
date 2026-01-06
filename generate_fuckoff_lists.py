#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


RAW_PATH = Path("raw_junk_email_domains.json")
OUTPUT_PATH = Path("fuckoff.json")
DEBUG_OUTPUT_PATH = Path("fuckoff_debug.json")
DEBUG_DOMAIN = "proton.me"
DEFAULT_LIMIT = 3000


def parse_timestamp(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate deduplicated domain lists for Power Automate."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=f"Max number of domains to output (default {DEFAULT_LIMIT}).",
    )
    args = parser.parse_args()

    env_limit = os.getenv("FUCKOFF_LIMIT")
    try:
        env_limit_value = int(env_limit) if env_limit else None
    except ValueError:
        env_limit_value = None
    limit = args.limit or env_limit_value or DEFAULT_LIMIT

    raw_payload = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    raw_domains = []
    timestamps = {}
    if isinstance(raw_payload, dict):
        raw_payload = raw_payload.get("domains", [])
    for item in raw_payload:
        if isinstance(item, dict):
            domain = item.get("domain")
            added_at = parse_timestamp(item.get("added_at"))
        else:
            domain = item
            added_at = None
        if domain:
            raw_domains.append(domain)
            current = timestamps.get(domain)
            if current is None or (added_at and added_at > current):
                timestamps[domain] = added_at

    seen = set()
    deduped = []
    for domain in raw_domains:
        if domain in seen:
            continue
        seen.add(domain)
        deduped.append(domain)

    if len(deduped) > limit:
        deduped = sorted(
            deduped,
            key=lambda d: timestamps.get(d) or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )[:limit]

    OUTPUT_PATH.write_text(
        json.dumps(deduped, separators=(",", ":")) + "\n", encoding="utf-8"
    )

    debug_domains = list(deduped)
    if DEBUG_DOMAIN not in debug_domains:
        debug_domains.append(DEBUG_DOMAIN)

    DEBUG_OUTPUT_PATH.write_text(
        json.dumps(debug_domains, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
