CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    passwd VARCHAR(100) NOT NULL
);

INSERT INTO users (username, passwd) VALUES ('admin', '8895f4a67e21c086bedfc5b195450d2b');

