-- Create students table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL
);

-- Insert sample data into students table
INSERT INTO students (student_name) VALUES
    ('Alice'),
    ('Bob'),
    ('Charlie'),
    ('David');

-- Create grades table
CREATE TABLE grades (
    grade_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(student_id),
    exam_type VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL
);

-- Insert sample data into grades table
INSERT INTO grades (student_id, exam_type, score) VALUES
    (1, 'Midterm', 80),
    (1, 'Final', 90),
    (2, 'Midterm', 75),
    (2, 'Final', 85),
    (3, 'Midterm', 95),
    (3, 'Final', 92),
    (4, 'Midterm', 88),
    (4, 'Final', 78);
