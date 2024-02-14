CREATE TYPE order_status AS ENUM ('current', 'past');

CREATE TABLE inventory (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(100) UNIQUE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE review (
    review_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    item_id INT NOT NULL,
    rating INT NOT NULL,
    subject VARCHAR(255),
    text VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id)
);

CREATE TABLE user (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50)
);

CREATE TABLE shipping_address (
    address_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE payment_info (
    payment_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    encrypted_card_number VARCHAR(255) NOT NULL,
    cardholder_name VARCHAR(100) NOT NULL,
    card_expiry_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    status order_status NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE cart (
    cart_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (item_id) REFERENCES inventory(item_id),
    FOREIGN KEY (order_id) REFERENCES order(order_id)
);
