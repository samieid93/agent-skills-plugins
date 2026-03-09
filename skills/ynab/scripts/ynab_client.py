"""Shared YNAB API client."""

import json
import os
import sys
import urllib.request

TOKEN = os.environ.get("YNAB_ACCESS_TOKEN")
BASE = "https://api.ynab.com/v1"


def fetch(path):
    if not TOKEN:
        print("Error: YNAB_ACCESS_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    req = urllib.request.Request(
        f"{BASE}{path}",
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["data"]


def millis(amount):
    """Convert YNAB milliunits to dollars."""
    return amount / 1000.0
