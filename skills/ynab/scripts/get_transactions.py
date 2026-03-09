#!/usr/bin/env python3
"""Get transactions from YNAB.

Usage:
  get_transactions.py
  get_transactions.py --since 2026-01-01
  get_transactions.py --since 2026-01-01 --category-id <id>
  get_transactions.py --since 2026-01-01 --account-id <id>
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from ynab_client import fetch, millis


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--category-id", help="Filter by category ID")
    parser.add_argument("--account-id", help="Filter by account ID")
    args = parser.parse_args()

    if args.category_id:
        path = f"/budgets/last-used/categories/{args.category_id}/transactions"
    elif args.account_id:
        path = f"/budgets/last-used/accounts/{args.account_id}/transactions"
    else:
        path = "/budgets/last-used/transactions"

    if args.since:
        path += f"?since_date={args.since}"

    transactions = fetch(path)["transactions"]

    result = [
        {
            "id": t["id"],
            "date": t["date"],
            "amount": millis(t["amount"]),
            "payee_name": t.get("payee_name"),
            "category_name": t.get("category_name"),
            "category_id": t.get("category_id"),
            "account_name": t.get("account_name"),
            "memo": t.get("memo"),
            "cleared": t["cleared"],
            "approved": t["approved"],
        }
        for t in transactions
        if not t.get("deleted")
    ]

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
