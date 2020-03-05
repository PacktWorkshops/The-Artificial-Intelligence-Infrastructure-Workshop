create database fashionmart;
use fashionmart;

CREATE TABLE products (p_id INT,
p_name TEXT,
p_buy_price FLOAT,
p_manufacturer TEXT,
p_created_at TIMESTAMP,
PRIMARY KEY (p_id)
);

CREATE TABLE sales (s_id INT,
p_id INT,
s_sale_price FLOAT,
s_profit FLOAT,
s_created_at TIMESTAMP,
PRIMARY KEY (s_id),
FOREIGN KEY (p_id)
    REFERENCES products(p_id)
    ON DELETE CASCADE
);


INSERT INTO products(p_id, p_name, p_buy_price, p_manufacturer, p_created_at)
VALUES
(1, 'Z-1 Running shoe', 34, 'Z-1', now()),
(2, 'XIMO Trek shirt', 15, 'XIMO', now()),
(3, 'XIMO Trek shorts', 18, 'XIMO', now()),
(4, 'NY cap', 18, 'NY', now());

INSERT INTO sales(s_id, p_id, s_sale_price, s_profit, s_created_at)
VALUES
(1,2,18,3,now()),
(2,3,20,2,now()),
(3,3,19,1,now()),
(4,1,40,6,now()),
(5,1,34,0,now());

-- simple join
SELECT
	products.p_name AS product_name,
	products.p_manufacturer AS manufacturer,
	sales.s_profit AS profit
FROM products
JOIN sales
ON products.p_id=sales.p_id;

-- aggregated sum with join

SELECT
	products.p_name AS product_name,
	products.p_manufacturer AS manufacturer,
	sales_subq.profit AS total_profit
FROM products
JOIN
	(SELECT
	  sales.p_id AS p_id,
	  SUM(sales.s_profit) AS profit
	 FROM sales
	 GROUP BY sales.p_id) AS sales_subq
ON products.p_id=sales_subq.p_id;


-- left outer join
SELECT
    products.p_name AS product_name,
    products.p_manufacturer AS manufacturer,
    IFNULL(sales_subq.profit,0) AS total_profit
FROM products
LEFT OUTER JOIN
	(SELECT
	  sales.p_id AS p_id,
	  SUM(sales.s_profit) AS profit
	 FROM sales
	 GROUP BY sales.p_id) AS sales_subq
ON products.p_id=sales_subq.p_id;
