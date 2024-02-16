-- date_trunc function to find the start of the current week (which is Monday) 
-- and then compares the date_added column against this starting point. 
-- It also checks that date_added is not greater than the current date 
-- to ensure you're only selecting records until the current date.
-- This modification adds + interval '1 day' to include records up to the end of today

COPY fit TO '/home/tro/projects/fit.csv' DELIMITER ',' CSV HEADER;



SELECT * FROM fit           
WHERE date_added >= date_trunc('week', current_date) AND date_added <= current_date + interval '1 day' ; 


-- With STATS General

SELECT
    exercise,
    COUNT(*) AS total_entries,
    SUM(exercise_count) AS total_exercise_count,
    AVG(exercise_count) AS avg_exercise_count,
    MIN(exercise_count) AS min_exercise_count,
    MAX(exercise_count) AS max_exercise_count
FROM
    fit
WHERE
    date_added >= date_trunc('week', current_date)  -- Start of the current week (Monday)
    AND date_added <= current_date + interval '1 day'  -- Today (including today)
GROUP BY
    exercise;

----- STats for each day days are numbers
SELECT
    exercise,
    EXTRACT(DOW FROM date_added) AS day_of_week,
    COUNT(*) AS total_entries,
    SUM(exercise_count) AS total_exercise_count,
    MIN(exercise_count) AS min_exercise_count,
    MAX(exercise_count) AS max_exercise_count
FROM
    fit
WHERE
    date_added >= date_trunc('week', current_date)  -- Start of the current week (Monday)
    AND date_added <= current_date + interval '1 day'  -- Today (including today)
GROUP BY
    exercise, day_of_week
ORDER BY
    exercise, day_of_week;


---- stats for each day days are Monday
SELECT
    exercise,
    to_char(date_added, 'Day') AS day_of_week,
    COUNT(*) AS total_entries,
    SUM(exercise_count) AS total_exercise_count,
    MIN(exercise_count) AS min_exercise_count,
    MAX(exercise_count) AS max_exercise_count
FROM
    fit
WHERE
    date_added >= date_trunc('week', current_date)  -- Start of the current week (Monday)
    AND date_added <= current_date + interval '1 day'  -- Today (including today)
GROUP BY
    exercise, day_of_week
ORDER BY
    exercise, day_of_week;

--- MODIFIED Most correct in terms of Week Day ordering 

SELECT 
    EXTRACT(ISODOW FROM date_added) as day_of_week,
    exercise,
    SUM(exercise_count) as total_exercise_count
FROM 
    fit
WHERE
    date_added >= date_trunc('week', CURRENT_DATE)
    AND date_added <= CURRENT_DATE + interval '1 day'
GROUP BY 
    day_of_week, 
    exercise
ORDER BY 
    day_of_week, 
    total_exercise_count DESC;


---- WITH WEEKDAYS 
SELECT 
    to_char(date_added, 'Day') as day_of_week,
    exercise,
    SUM(exercise_count) as total_exercise_count
FROM 
    fit
WHERE
    date_added >= date_trunc('week', CURRENT_DATE)
    AND date_added <= CURRENT_DATE + interval '1 day'
GROUP BY 
    day_of_week, 
    exercise
ORDER BY 
    day_of_week, 
    total_exercise_count DESC;



