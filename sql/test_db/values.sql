INSERT INTO users (first_name, last_name, email, phone_number, ip_address, username, street_address, cuil_cuit_dni)
VALUES
('John', 'Doe', 'john.doe@example.com', '1123456789', '192.168.0.1', 'jdoe', '123 Main St', '20345678901'),
('Jane', 'Smith', 'jane.smith@mail.com', '1123456780', '172.16.0.2', 'jsmith', '456 Elm St', '27456789012'),
('Carlos', 'Perez', 'carlos.perez@domain.net', '3412345678', '10.0.0.3', 'cperez', '789 Oak St', '30234567891'),
('Maria', 'Lopez', 'maria.lopez@mail.org', '3412345670', '192.168.1.10', 'mlopez', '321 Pine St', '33456789015'),
('Laura', 'Garcia', 'laura.garcia@gmail.com', '1198765432', '8.8.8.8', 'lgarcia', '222 Cedar St', '23123456789'),
('Pedro', 'Gomez', 'pedro.gomez@mail.net', '1134567890', '172.16.254.1', 'pgomez', '654 Walnut St', '20123456789'),
('Ana', 'Martinez', 'ana.martinez@example.com', '1145678901', '192.168.100.2', 'amartinez', '987 Maple St', '27123456789'),
('Luis', 'Hernandez', 'luis.hernandez@corp.com', '3412345671', '203.0.113.1', 'lhernandez', '111 Birch St', '33123456789'),
('Sofia', 'Gonzalez', 'sofia.gonzalez@mail.com', '1123345678', '192.168.2.10', 'sgonzalez', '888 Spruce St', '23123456789'),
('Miguel', 'Torres', 'miguel.torres@mail.com', '1122234567', '192.168.3.15', 'mtorres', '444 Fir St', '30123456789');


INSERT INTO transactions (credit_card_number, email, transaction_ip, amount)
VALUES
('4111111111111111', 'buyer1@mail.com', '203.0.113.5', 100.00),
('5500000000000004', 'buyer2@mail.com', '198.51.100.10', 200.50),
('340000000000009', 'buyer3@mail.com', '203.0.113.10', 300.75),
('370000000000002', 'buyer4@mail.com', '192.0.2.15', 400.25),
('6011000000000004', 'buyer5@mail.com', '203.0.113.20', 500.00),
('4111111111111111', 'buyer6@mail.com', '198.51.100.25', 600.35),
('5500000000000004', 'buyer7@mail.com', '203.0.113.25', 700.40),
('340000000000009', 'buyer8@mail.com', '192.0.2.30', 800.00),
('370000000000002', 'buyer9@mail.com', '198.51.100.35', 900.75),
('6011000000000004', 'buyer10@mail.com', '203.0.113.40', 1000.00);
