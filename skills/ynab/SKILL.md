---
name: ynab
description: >
  Use this skill to read data from YNAB (You Need A Budget). Trigger whenever the user
  asks about their budget, spending, categories, transactions, account balances, or
  anything related to their personal finances in YNAB. Phrases like "check my budget",
  "how much did I spend on X", "what's my balance", "show my transactions", "YNAB",
  or any financial planning question should activate this skill.
---

# YNAB Data Access

Provides access to YNAB budget data via the YNAB API.

## Prerequisites

- `$YNAB_ACCESS_TOKEN` must be set in the environment (from YNAB account → Developer Settings)
- Python 3 must be available
- Scripts live in the `scripts/` directory alongside this file

## Scripts

Run these scripts to fetch YNAB data. All output JSON to stdout. All read
`$YNAB_API_TOKEN` from the environment automatically.

| Script | What it returns |
|--------|-----------------|
| `get_budget.py` | Budget name, currency, accounts with balances |
| `get_categories.py` | All category groups and categories with their IDs |
| `get_month.py [YYYY-MM]` | A month's plan: every category with budgeted, activity, balance. Defaults to current month. |
| `get_transactions.py` | Transactions. Supports `--since YYYY-MM-DD`, `--category-id ID`, `--account-id ID` |

**How to run them** (the skill base path is available from context):

```bash
python skills/ynab/scripts/get_month.py
python skills/ynab/scripts/get_month.py 2026-01
python skills/ynab/scripts/get_transactions.py --since 2026-01-01
python skills/ynab/scripts/get_transactions.py --since 2026-01-01 --category-id <id>
```

## Key Concepts

- **Amounts are in milliunits**: divide by 1000 to get dollars. E.g. `294230 → $294.23`
- **`balance < 0`** on a category means overspent
- **`activity`** is what was spent (negative number), **`budgeted`** is what was assigned
- The budget ID `last-used` always resolves to the user's active budget

## Common Workflows

**"How am I doing this month?"**
→ Run `get_month.py`, look at categories where balance < 0 or activity is close to budgeted

**"How much did I spend on X?"**
→ Run `get_categories.py` to find the category ID, then `get_transactions.py --since <date> --category-id <id>`

**"Show my last 3 months of dining"**
→ Run `get_month.py` for each of the last 3 months and compare activity in the dining category

**"What are my account balances?"**
→ Run `get_budget.py`
