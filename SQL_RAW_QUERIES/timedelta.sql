-- This is for the Fasting Timedelta raw sql queries

---- Raw Table Creation
CREATE TABLE eat2 (
    id SERIAL PRIMARY KEY,
    meal TEXT,
    datetime TIMESTAMP DEFAULT NOW(),
    timedelta INTERVAL
);


-- some inserts. If creating table later change days to have two consecutive days
INSERT INTO eat2 (meal, datetime, timedelta) VALUES
    ('value1', '2023-12-21 00:00:00', INTERVAL '1 day 2 hours 30 minutes'),
    ('value2', '2023-12-21 12:00:00', INTERVAL '3 days 4 hours 15 minutes'),
    ('value3', '2023-12-21 18:00:00', INTERVAL '5 days 6 hours 45 minutes'),
    ('value4', '2023-12-22 06:00:00', INTERVAL '2 days 3 hours 20 minutes');



-- Raw Timedelta calc - offred by GPT4 andworking

SELECT (MAX(datetime) - MIN(datetime)) AS time_difference
FROM eat2
WHERE datetime >= DATE_TRUNC('day', NOW() - INTERVAL '1 day') AND datetime < DATE_TRUNC('day', NOW());
 time_difference 

