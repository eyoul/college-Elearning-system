-- Drop existing tables if they exist
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS major;
DROP TABLE IF EXISTS post;

-- Create roles table
CREATE TABLE roles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);

-- Insert role data
INSERT INTO roles (name, description) VALUES ('admin', 'Administrator');
INSERT INTO roles (name, description) VALUES ('lecturer', 'Lecturer');
INSERT INTO roles (name, description) VALUES ('student', 'Student');
-- Create courses table
CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);

INSERT INTO courses (name, description) VALUES ('CoSc 6003', 'Computer security ');
INSERT INTO courses (name, description) VALUES ('CoSc 6301', 'Distributed system');
INSERT INTO courses (name, description) VALUES ('CoSc 6101', 'Software Project Management ');

-- Create major table
CREATE TABLE major (
  id INTEGER PRIMARY KEY,
  name TEXT
);
INSERT INTO major (name) VALUES ('Data and Web Engineering');
INSERT INTO major (name) VALUES ('Software Engineering');
INSERT INTO major (name) VALUES ('Network security');


CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users(id)
);

-- Create users table
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role_id INTEGER NOT NULL,
  FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Create students table
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  major_id INTEGER,
  user_id INTEGER UNIQUE,
  FOREIGN KEY (major_id) REFERENCES major(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO students (major_id, user_id) VALUES (1, 2);
INSERT INTO students (major_id, user_id) VALUES (2, 3);
INSERT INTO students (major_id, user_id) VALUES (3, 4);

-- Create grades table
CREATE TABLE grades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER,
  lecturer_id INTEGER,
  course_id INTEGER,
  grade TEXT,
  creditH INTEGER,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (lecturer_id) REFERENCES users(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

