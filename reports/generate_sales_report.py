import os
from datetime import datetime
import psycopg2
from openpyxl import Workbook

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ.get("DB_NAME", "etldb")
DB_USER = os.environ.get("DB_USER", "etluser")
DB_PASS = os.environ["DB_PASS"]

SUMMARY_SQL = """
SELECT
  COUNT(*) AS num_orders,
  COALESCE(SUM(amount), 0) AS total_amount,
  COALESCE(SUM(tax), 0) AS total_tax,
  MIN(order_date) AS first_date,
  MAX(order_date) AS last_date
FROM sales;
"""

DETAIL_SQL = """
SELECT order_id, customer_id, amount, tax, order_date
FROM sales
ORDER BY order_date, order_id
LIMIT 200;
"""

def main():
  conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
  )

  try:
    with conn.cursor() as cur:
      cur.execute(SUMMARY_SQL)
      summary = cur.fetchone()

      cur.execute(DETAIL_SQL)
      rows = cur.fetchall()

    wb = Workbook()

    # Summary sheet
    ws = wb.active
    ws.title = "Summary"
    ws.append(["Generated (UTC)", datetime.utcnow().isoformat() + "Z"])
    ws.append([])
    ws.append(["Metric", "Value"])
    ws.append(["Number of Orders", int(summary[0])])
    ws.append(["Total Amount", float(summary[1])])
    ws.append(["Total Tax", float(summary[2])])
    ws.append(["First Date", str(summary[3]) if summary[3] else ""])
    ws.append(["Last Date", str(summary[4]) if summary[4] else ""])

    # Detail sheet
    ws2 = wb.create_sheet("Orders (sample)")
    ws2.append(["order_id", "customer_id", "amount", "tax", "order_date"])
    for r in rows:
      ws2.append([r[0], r[1], float(r[2]), float(r[3]), str(r[4])])

    out = "sales_report.xlsx"
    wb.save(out)
    print(f"✅ Wrote {out}")

  finally:
    conn.close()

if __name__ == "__main__":
  main()
