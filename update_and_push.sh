#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: ./update_and_push.sh <domain|email> [more...]" >&2
  exit 1
fi

python3 add_domains.py "$@"
python3 generate_fuckoff_lists.py

git add raw_junk_email_domains.json fuckoff.json fuckoff_debug.json
git commit -m "Update junk domain lists"
git push
