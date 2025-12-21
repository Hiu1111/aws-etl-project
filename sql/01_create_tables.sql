CREATE TABLE IF NOT EXISTS sales_clean (
  order_id     BIGINT,
  customer_id  BIGINT,
  amount       DOUBLE PRECISION,
  date         DATE,
  tax          DOUBLE PRECISION,
  loaded_at    TIMESTAMP DEFAULT NOW()
);
