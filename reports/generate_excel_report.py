import os
from datetime import datetime
import psycopg2
from openpyxl import Workbook

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "etldb")
DB_USER = os.environ.get("DB_USER", "etluser")
DB_PASS = os.environ["DB_PASS"]

QUERY = """
SELECT
  COUNT(*) AS num_rows,
  COALESCE(SUM(amount), 0) AS total_amount,
  COALESCE(SUM(tax), 0) AS total_tax,
  MIN(date) AS first_date,
  MAX(date) AS last_date
FROM sales_clean;
"""

def main():
  conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
  )
  try:
    with conn.cursor() as cur:
      cur.execute(QUERY)
      num_rows, total_amount, total_tax, first_date, last_date = cur.fetchone()

    wb = Workbook()
    ws = wb.active
    ws.title = "Sales Summary"

    ws.append(["Generated (UTC)", datetime.utcnow().isoformat() + "Z"])
    ws.append([])
    ws.append(["Metric", "Value"])
    ws.append(["Rows", int(num_rows)])
    ws.append(["Total Amount", float(total_amount)])
    ws.append(["Total Tax", float(total_tax)])
    ws.append(["First Date", str(first_date) if first_date else ""])
    ws.append(["Last Date", str(last_date) if last_date else ""])

    out = "sales_report.xlsx"
    wb.save(out)
    print(f"✅ Wrote {out}")
  finally:
    conn.close()

if __name__ == "__main__":
  main()
