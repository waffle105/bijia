from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def money(value, label: str, errors: list[str]) -> Decimal:
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        errors.append(f"{label} is not a valid decimal: {value!r}")
        return Decimal("0")


def validate(plan: dict) -> list[str]:
    errors: list[str] = []
    if not str(plan.get("project_name", "")).strip():
        errors.append("project_name is required")

    items = plan.get("items")
    quotes = plan.get("quotes")
    if not isinstance(items, list) or not items:
        errors.append("items must be a non-empty list")
        items = []
    if not isinstance(quotes, list) or len(quotes) != 3:
        errors.append("quotes must contain exactly three entries")
        quotes = quotes if isinstance(quotes, list) else []

    quantities: list[Decimal] = []
    for index, item in enumerate(items, start=1):
        if not str(item.get("name", "")).strip():
            errors.append(f"item {index} name is required")
        if not str(item.get("unit", "")).strip():
            errors.append(f"item {index} unit is required")
        quantity = money(item.get("quantity"), f"item {index} quantity", errors)
        if quantity <= 0:
            errors.append(f"item {index} quantity must be positive")
        quantities.append(quantity)

    companies: list[str] = []
    for quote_index, quote in enumerate(quotes, start=1):
        company = str(quote.get("company", "")).strip()
        if not company:
            errors.append(f"quote {quote_index} company is required")
        companies.append(company)

        prices = quote.get("unit_prices")
        if not isinstance(prices, list) or len(prices) != len(items):
            errors.append(
                f"quote {quote_index} unit_prices must contain {len(items)} entries"
            )
            continue

        target = money(
            quote.get("target_total"), f"quote {quote_index} target_total", errors
        )
        calculated = Decimal("0")
        for item_index, (quantity, raw_price) in enumerate(
            zip(quantities, prices), start=1
        ):
            price = money(
                raw_price,
                f"quote {quote_index} item {item_index} unit price",
                errors,
            )
            if price < 0:
                errors.append(
                    f"quote {quote_index} item {item_index} unit price cannot be negative"
                )
            calculated += quantity * price

        if calculated != target:
            errors.append(
                f"quote {quote_index} total mismatch: calculated {calculated} != target {target}"
            )

    nonempty_companies = [name for name in companies if name]
    if len(set(nonempty_companies)) != len(nonempty_companies):
        errors.append("quote company names must be unique")

    primary = str(plan.get("primary_company", "")).strip()
    if not primary:
        errors.append("primary_company is required")
    elif primary not in companies:
        errors.append("primary_company must match one of the three quote companies")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_quote_plan.py <plan.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read plan: {exc}", file=sys.stderr)
        return 2

    errors = validate(plan)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: quote plan has three unique companies and all totals reconcile exactly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
