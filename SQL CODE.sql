CREATE TABLE sales_data (
    invoice_no        TEXT,
    stock_code        TEXT,
    description       TEXT,
    quantity          INTEGER,
    invoice_date      TIMESTAMP,
    unit_price        NUMERIC(10,2),
    customer_id       NUMERIC,   -- IMPORTANT FIX
    country           TEXT,
    revenue           NUMERIC(12,2),
    repeat_purchase   BOOLEAN
);

SELECT COUNT(*) FROM sales_data;
SELECT * FROM sales_data LIMIT 5;

SELECT
  COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer,
  COUNT(*) FILTER (WHERE invoice_no IS NULL) AS missing_invoice
FROM sales_data;

SELECT
  MIN(revenue),
  MAX(revenue),
  AVG(revenue)
FROM sales_data;

CREATE INDEX idx_invoice_date ON sales_data(invoice_date);
CREATE INDEX idx_customer_id ON sales_data(customer_id);
CREATE INDEX idx_country ON sales_data(country);

-- Top revenue countries
SELECT country, SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;

-- Repeat vs one-time customers
SELECT repeat_purchase, COUNT(*) 
FROM sales_data
GROUP BY repeat_purchase;

CREATE VIEW revenue_by_month AS
SELECT
  DATE_TRUNC('month', invoice_date) AS month,
  SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY month
ORDER BY month;

SELECT * FROM revenue_by_month;

CREATE VIEW top_products AS
SELECT
  stock_code,
  description,
  SUM(revenue) AS total_revenue
FROM sales_data
GROUP BY stock_code, description
ORDER BY total_revenue DESC
LIMIT 20;

CREATE VIEW customer_ltv AS
SELECT
  customer_id,
  COUNT(DISTINCT invoice_no) AS total_orders,
  SUM(revenue) AS lifetime_value
FROM sales_data
GROUP BY customer_id;

SELECT *
FROM customer_ltv
ORDER BY lifetime_value DESC
LIMIT 10;

SELECT 
  SUM(revenue) / COUNT(DISTINCT invoice_no) AS avg_order_value
FROM sales_data;

SELECT 
  SUM(revenue) / COUNT(DISTINCT customer_id) AS revenue_per_customer
FROM sales_data;


SELECT 
  DATE_TRUNC('month', invoice_date) AS month,
  COUNT(DISTINCT customer_id) AS active_customers
FROM sales_data
GROUP BY month
ORDER BY month;

SELECT
  CASE
    WHEN lifetime_value >= 200000 THEN 'VIP'
    WHEN lifetime_value >= 100000 THEN 'High'
    WHEN lifetime_value >= 50000 THEN 'Mid'
    ELSE 'Low'
  END AS segment,
  COUNT(*) AS customers
FROM customer_ltv
GROUP BY segment;






