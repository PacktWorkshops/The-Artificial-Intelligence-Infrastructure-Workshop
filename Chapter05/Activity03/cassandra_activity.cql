use fashionmart;

CREATE COLUMNFAMILY feedback_logs(
fl_id int PRIMARY KEY,
fl_feedback text,
fl_location text,
user_id int,
fl_created_at timestamp);

BEGIN BATCH
INSERT INTO feedback_logs(fl_id, fl_feedback, fl_location, user_id, fl_created_at)
VALUES(1, 'Great website', 'London', 3, '2019-10-30 12:05:00+0000');
INSERT INTO feedback_logs(fl_id, fl_feedback, fl_location, user_id, fl_created_at)
VALUES(2, 'Good work', 'Seattle', 2, '2019-10-03 12:05:00+0000');
INSERT INTO feedback_logs(fl_id, fl_feedback, fl_location, user_id, fl_created_at) VALUES(3, 'Amazing', 'Seattle', 2, '2019-11-04 11:05:00+0000');
INSERT INTO feedback_logs(fl_id, fl_feedback, fl_location, user_id, fl_created_at) VALUES(4, 'Not so good', 'Hong kong', 1, '2019-11-04 11:05:00+0000');
INSERT INTO feedback_logs(fl_id, fl_feedback, fl_location, user_id, fl_created_at) VALUES(4, 'Informative website', 'Shanghai', 1, '2018-11-04 11:05:00+0000');
APPLY BATCH;


SELECT COUNT(fl_id) AS total_feedbacks
FROM feedback_logs;
