CREATE TABLE user (
    userID INT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    type INT NOT NULL,
    shipping_ptr INT,
    payment_ptr INT,
    cart_ptr INT,
    FOREIGN KEY (shipping_ptr) REFERENCES shippingInfo(shippingID),
    FOREIGN KEY (payment_ptr) REFERENCES paymentInfo(paymentID),
    FOREIGN KEY (cart_ptr) REFERENCES cart(cartID)
);

CREATE TABLE inventory (
    itemID INT PRIMARY KEY,
    userID INT NOT NULL,
    analyticsID INT NOT NULL,
    itemName VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL (10,2) NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (analyticsID) REFERENCES analytics(dataID)
);

CREATE TABLE analytics (
    dataID INT PRIMARY KEY,
    itemID INT NOT NULL,
    quantitySold INT NOT NULL,
    FOREIGN KEY (itemID) REFERENCES inventory(itemID)
);

CREATE TABLE cart (
    cartID INT PRIMARY KEY,
    userID INT NOT NULL,
    itemID INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (itemID) REFERENCES inventory(itemID)
);

CREATE TABLE paymentInfo (
    paymentID INT PRIMARY KEY,
    userID INT NOT NULL,
    cardNumber INT VARCHAR(16) NULL,
    cardholderName VARCHAR(100) NOT NULL,
    cardDate DATE NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID)
);

CREATE TABLE shippingInfo (
    shippingID INT PRIMARY KEY,
    userID INT NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip VARCHAR(5) NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID)
);

CREATE TABLE orders (
    orderID INT PRIMARY KEY,
    userID INT NOT NULL,
    itemID INT NOT NULL,
    price INT NOT NULL,
    quantity INT NOT NULL,
    orderTime DATE NOT NULL,
    cardNumber INT VARCHAR(16) NULL,
    cardholderName VARCHAR(100) NOT NULL,
    cardDate DATE NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip VARCHAR(5) NOT NULL,
    country VARCHAR(100) NOT NULL,
    FOREIGN KEY (userID) REFERENCES user(userID),
    FOREIGN KEY (itemID) REFERENCES inventory(itemID)
);

CREATE TABLE featured (
    featuredID INT PRIMARY KEY,
    itemID INT NOT NULL,
    type INT NOT NULL,
    FOREIGN KEY (itemID) REFERENCES inventory(itemID)
);