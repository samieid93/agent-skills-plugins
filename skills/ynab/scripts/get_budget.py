#!/usr/bin/env python3
"""Get budget summary and account balances from YNAB."""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ynab_client import fetch, millis


def main():
    budget = fetch("/budgets/last-used")["budget"]
    accounts = fetch("/budgets/last-used/accounts")["accounts"]

    result = {
        "budget_name": budget["name"],
        "currency": budget["currency_format"]["iso_code"],
        "accounts": [
            {
                "id": a["id"],
                "name": a["name"],
                "type": a["type"],
                "balance": millis(a["balance"]),
                "cleared_balance": millis(a["cleared_balance"]),
                "uncleared_balance": millis(a["uncleared_balance"]),
                "on_budget": a["on_budget"],
                "closed": a["closed"],
            }
            for a in accounts
            if not a["deleted"]
        ],
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
