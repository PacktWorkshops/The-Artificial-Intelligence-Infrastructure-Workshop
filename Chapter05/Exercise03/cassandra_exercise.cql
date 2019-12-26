CREATE KEYSPACE fashionmart
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

use fashionmart;

CREATE COLUMNFAMILY user(
u_id int PRIMARY KEY,
u_fname text,
u_lname text,
u_age int,
u_location text,
u_visits int,
u_created_at timestamp,
u_last_visited timestamp,
);


INSERT INTO user(u_id, u_fname, u_lname, u_age, u_location, u_created_at, u_last_visited)
VALUES(1,'Derek', 'Gates', 18, 'San Francisco', toTimestamp(now()), '2019-10-30 12:05:00+0000');

BEGIN BATCH
  INSERT INTO user(u_id, u_fname, u_lname, u_age, u_location, u_created_at, u_last_visited)
  VALUES(2, 'Max', 'Frost', 15, 'London', toTimestamp(now()), toTimestamp(now()));
  INSERT INTO user(u_id, u_fname, u_lname, u_age, u_location, u_created_at, u_last_visited)
  VALUES(3,'Isabela', 'McGuire', 29, 'Seattle', toTimestamp(now()), '2019-11-07 07:30+0000');
  INSERT INTO user(u_id, u_fname, u_lname, u_age, u_location, u_created_at, u_last_visited)
  VALUES(4,'Roger', 'Moore', 68, 'Amsterdam', toTimestamp(now()), '2019-12-02 14:50+0000');
APPLY BATCH;


ALTER COLUMNFAMILY user
ADD salary int;

BEGIN BATCH
  UPDATE user
  SET salary=120000
  WHERE u_id=1;
  UPDATE user
  SET salary=140000
  WHERE u_id=2;
  UPDATE user
  SET salary=175000
  WHERE u_id=3;
  UPDATE user
  SET salary=145000
  WHERE u_id=4;
APPLY BATCH;


1.SELECT
	u_fname,
	u_lname,
	u_location,
	MAX(u_visits) AS max_visits
FROM user;
SELECT
	u_fname,
	u_lname,
	u_location,
	MIN(u_visits) AS min_visits
FROM user

2. SELECT
	SUM(u_visits) AS total_visits
FROM user

3. SELECT AVG(u_age) AS average_age FROM user;



