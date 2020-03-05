
-- MySQL script : Solution to the MySQL Activities for chapter 5. Databases
-- Creating structure

Create database PacktFashion;
use PacktFashion;

CREATE TABLE manufacturer (m_id INT,
m_name TEXT,
m_created_at TIMESTAMP,
PRIMARY KEY (m_id)
);

CREATE TABLE products (p_id INT,
p_name TEXT,
p_buy_price FLOAT,
p_manufacturer_id INT,
p_created_at TIMESTAMP,
PRIMARY KEY (p_id),
FOREIGN KEY (p_manufacturer_id)
    REFERENCES manufacturer(m_id)
    ON DELETE CASCADE
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

CREATE TABLE location (loc_id INT,
loc_name TEXT,
loc_created_at TIMESTAMP,
PRIMARY KEY (loc_id)
);

CREATE TABLE status (status_id INT,
status_name TEXT,
status_created_at TIMESTAMP,
PRIMARY KEY (status_id)
);

CREATE TABLE inventory (inv_id INT,
inv_loc_id INT,
inv_p_id INT,
inv_status_id INT,
inv_created_at TIMESTAMP,
PRIMARY KEY (inv_id),
FOREIGN KEY (inv_loc_id)
    REFERENCES location(loc_id)
    ON DELETE CASCADE,
FOREIGN KEY (inv_p_id)
    REFERENCES products(p_id)
    ON DELETE CASCADE,
FOREIGN KEY (inv_status_id )
    REFERENCES status(status_id)
    ON DELETE CASCADE
);



-- Loading data

INSERT INTO manufacturer(m_id, m_name, m_created_at)
VALUES
(1,"Z-1", now()),
(2,"XIMO", now()),
(3,"NY", now());

INSERT INTO products(p_id, p_name, p_buy_price, p_manufacturer_id, p_created_at)
VALUES
(1, 'Z-1 Running shoe', 34, 1, now()),
(2, 'XIMO Trek shirt', 15, 2, now()),
(3, 'XIMO Trek shorts', 18, 2, now()),
(4, 'NY cap', 18, 3, now());

INSERT INTO sales(s_id, p_id, s_sale_price, s_profit, s_created_at)
VALUES
(1,2,18,3,now()),
(2,3,20,2,now()),
(3,3,19,1,now()),
(4,1,40,6,now()),
(5,1,34,0,now());


INSERT INTO location(loc_id, loc_name, loc_created_at)
VALUES
(1, 'California', now()),
(2, 'London', now()),
(3, 'Prague', now());

INSERT INTO status(status_id, status_name, status_created_at)
VALUES
(1, 'IN', now()),
(2, 'OUT', now());

INSERT INTO inventory(inv_id ,
inv_loc_id,
inv_p_id,
inv_status_id,
inv_created_at)
VALUES
(1,1,3,1,now()),
(2,3,4,1,now()),
(3,2,2,2,now()),
(4,3,2,2,now()),
(5,1,1,2,now());

SELECT * FROM manufacturer;
SELECT * FROM products;
SELECT * FROM sales;
SELECT * FROM location;
SELECT * FROM status;
SELECT * FROM inventory;


SELECT count(inventory.inv_p_id) as total_in_stock_products
     FROM inventory
     JOIN status
     ON status.status_id=inventory.inv_status_id
     WHERE status.status_name='IN';


SELECT count(inventory.inv_p_id) as total_out_of_stock_products
     FROM inventory
     JOIN status
     ON status.status_id=inventory.inv_status_id
     WHERE status.status_name='OUT';


SELECT status.status_name as status
     FROM inventory, status, products, location
     WHERE status.status_id=inventory.inv_status_id
     AND products.p_id = inventory.inv_p_id
     AND location.loc_id = inventory.inv_loc_id
     AND products.p_name='XIMO Trek shirt'
     AND location.loc_name='Prague';


