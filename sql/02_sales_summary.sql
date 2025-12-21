SELECT
  COUNT(*) AS num_rows,
  SUM(amount) AS total_amount,
  SUM(tax) AS total_tax,
  MIN(date) AS first_date,
  MAX(date) AS last_date
FROM sales_clean;
