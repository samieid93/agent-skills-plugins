#!/usr/bin/env python3
"""Get a month's budget plan from YNAB.

Usage:
  get_month.py             # current month
  get_month.py 2026-01     # specific month (YYYY-MM)
"""

import json
import sys
import os
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from ynab_client import fetch, millis


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        month_str = f"{arg}-01" if len(arg) == 7 else arg
    else:
        today = date.today()
        month_str = f"{today.year}-{today.month:02d}-01"

    month = fetch(f"/budgets/last-used/months/{month_str}")["month"]

    # Group flat category list by category_group_name
    groups = {}
    for cat in month["categories"]:
        if cat.get("deleted") or cat.get("hidden"):
            continue
        gname = cat.get("category_group_name", "Uncategorized")
        groups.setdefault(gname, []).append({
            "id": cat["id"],
            "name": cat["name"],
            "budgeted": millis(cat["budgeted"]),
            "activity": millis(cat["activity"]),
            "balance": millis(cat["balance"]),
            "overspent": cat["balance"] < 0,
        })

    result = {
        "month": month["month"],
        "income": millis(month["income"]),
        "budgeted": millis(month["budgeted"]),
        "activity": millis(month["activity"]),
        "to_be_budgeted": millis(month["to_be_budgeted"]),
        "category_groups": [
            {"group_name": name, "categories": cats}
            for name, cats in groups.items()
        ],
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
