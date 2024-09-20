CREATE DATABASE meli_challenge_test;
USE meli_challenge_test;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    ip_address VARCHAR(45),
    username VARCHAR(50),
    street_address VARCHAR(100),
    cuil_cuit_dni VARCHAR(20)
);


CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    credit_card_number VARCHAR(20),
    email VARCHAR(100),
    transaction_ip VARCHAR(45),
    amount DECIMAL(10, 2)
);
