#!/usr/bin/env python3
import json
from pathlib import Path


RAW_PATH = Path("raw_junk_email_domains.json")
OUTPUT_PATH = Path("fuckoff.json")
DEBUG_OUTPUT_PATH = Path("fuckoff_debug.json")
DEBUG_DOMAIN = "proton.me"


def dedupe_preserve_order(values):
    seen = set()
    deduped = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def main():
    raw_domains = json.loads(RAW_PATH.read_text(encoding="utf-8"))
    deduped = dedupe_preserve_order(raw_domains)

    OUTPUT_PATH.write_text(
        json.dumps(deduped, indent=2) + "\n", encoding="utf-8"
    )

    debug_domains = list(deduped)
    if DEBUG_DOMAIN not in debug_domains:
        debug_domains.append(DEBUG_DOMAIN)

    DEBUG_OUTPUT_PATH.write_text(
        json.dumps(debug_domains, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
