-- Insert dummy test data for the 'user' table
INSERT INTO user (user_id, username, password_hash, email, first_name, last_name)
VALUES
  (1, 'john_doe', 'hashed_password_1', 'john.doe@example.com', 'John', 'Doe'),
  (2, 'jane_smith', 'hashed_password_2', 'jane.smith@example.com', 'Jane', 'Smith');

-- Insert dummy test data for the 'inventory' table
INSERT INTO inventory (item_id, item_name, quantity, price)
VALUES
  (1, 'Laptop', 10, 999.99),
  (2, 'Smartphone', 20, 499.99);

-- Insert dummy test data for the 'review' table
INSERT INTO review (review_id, user_id, item_id, rating, subject, text, created_at)
VALUES
  (1, 1, 1, 5, 'Great product!', 'I love this laptop. It works perfectly.', '2022-01-01 10:00:00'),
  (2, 2, 1, 4, 'Good quality', 'The laptop is good, but the battery life could be better.', '2022-01-02 12:30:00');

-- Insert dummy test data for the 'shipping_address' table
INSERT INTO shipping_address (address_id, user_id, street_address, city, state, postal_code, country)
VALUES
  (1, 1, '123 Main St', 'Cityville', 'CA', '12345', 'USA'),
  (2, 2, '456 Oak Ave', 'Townsville', 'NY', '67890', 'USA');

-- Insert dummy test data for the 'payment_info' table
INSERT INTO payment_info (payment_id, user_id, encrypted_card_number, cardholder_name, card_expiry_date, created_at)
VALUES
  (1, 1, 'encrypted_card_number_1', 'John Doe', '2024-12-31', '2022-01-01 08:45:00'),
  (2, 2, 'encrypted_card_number_2', 'Jane Smith', '2023-11-30', '2022-01-02 10:15:00');

-- Insert dummy test data for the 'orders' table
INSERT INTO orders (order_id, user_id, status, created_at, delivered_at)
VALUES
  (1, 1, 'current', '2022-01-01 09:30:00', NULL),
  (2, 2, 'past', '2022-01-02 11:00:00', '2022-01-03 14:20:00');

-- Insert dummy test data for the 'cart' table
INSERT INTO cart (cart_id, user_id, order_id, item_id)
VALUES
  (1, 1, 1, 1),
  (2, 2, 2, 2);
