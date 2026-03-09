#!/usr/bin/env python3
"""Get all category groups and categories from YNAB."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ynab_client import fetch


def main():
    groups = fetch("/budgets/last-used/categories")["category_groups"]

    result = [
        {
            "group_id": g["id"],
            "group_name": g["name"],
            "categories": [
                {"id": c["id"], "name": c["name"]}
                for c in g["categories"]
                if not c["deleted"] and not c["hidden"]
            ],
        }
        for g in groups
        if not g["deleted"] and not g["hidden"] and g["categories"]
    ]

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
