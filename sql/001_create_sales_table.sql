CREATE TABLE IF NOT EXISTS sales (
    order_id      INT,
    customer_id   INT,
    amount        NUMERIC(10,2),
    tax           NUMERIC(10,2),
    order_date    DATE
);
