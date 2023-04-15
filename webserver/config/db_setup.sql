-- Create the database titled "paul_vault"
CREATE DATABASE paul_vault;

-- Use the database titled "paul_vault"
USE paul_vault;

-- Create the user "dave" with the password "change-this-password-immediately"
CREATE USER dave IDENTIFIED BY 'change-this-password-immediately';

-- Grant the user "dave" all privileges on the database "paul_vault"
GRANT ALL PRIVILEGES ON paul_vault.* TO dave;

-- Create the table titled "highscores" that includes "id", "name", "game", "score", and "date" columns.
CREATE TABLE highscores (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    game VARCHAR(255) NOT NULL,
    score INT NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (id)
);