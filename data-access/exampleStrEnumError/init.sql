-- create example table

CREATE TYPE status_enum AS ENUM ('pending', 'final');

CREATE TABLE IF NOT EXISTS EXAMPLE (
    id INT PRIMARY KEY,
    status status_enum
);

-- insert initial default roles
INSERT INTO EXAMPLE (id,status) VALUES (0,'pending'),(1,'final');