#!/usr/bin/env python3
"""
Test script to validate CSV import functionality
"""

import csv
import sys
from pathlib import Path


def test_csv_parsing(csv_file_path: str):
    """Test CSV parsing to identify issues"""
    print(f"Testing CSV file: {csv_file_path}")

    total_rows = 0
    successful_rows = 0
    failed_rows = []

    with open(csv_file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, 1):
            total_rows += 1

            try:
                # Extract and clean data (same logic as utils.py)
                title = row["title"].strip()
                origin = (
                    row["origin_account"].strip()
                    if row["origin_account"].strip() != "-"
                    else None
                )
                destination = (
                    row["destination_account"].strip()
                    if row["destination_account"].strip() != "-"
                    else None
                )
                amount_str = row["amount"].replace(",", ".").strip()
                currency = row["currency"].strip()
                day_of_month = int(row["day_of_month"])
                description = row["description"].strip()

                # Parse amount - handle malformed amounts like "55,99,PLN"
                if currency in amount_str:
                    # Amount contains currency, extract just the number
                    amount_str = (
                        amount_str.replace(currency, "").replace(",", ".").strip()
                    )

                amount = float(amount_str)

                print(f"Row {row_num}: ✓ {title} - {amount} {currency}")
                successful_rows += 1

            except (ValueError, KeyError) as e:
                print(f"Row {row_num}: ✗ Error - {e}")
                print(f"  Raw data: {row}")
                failed_rows.append((row_num, row, str(e)))

    print("\n=== SUMMARY ===")
    print(f"Total rows: {total_rows}")
    print(f"Successfully parsed: {successful_rows}")
    print(f"Failed: {len(failed_rows)}")

    if failed_rows:
        print("\n=== FAILED ROWS ===")
        for row_num, row, error in failed_rows:
            print(f"Row {row_num}: {error}")
            print(f"  Data: {row}")

    return successful_rows == total_rows


if __name__ == "__main__":
    csv_path = "data.csv"
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]

    if not Path(csv_path).exists():
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    success = test_csv_parsing(csv_path)
    sys.exit(0 if success else 1)
