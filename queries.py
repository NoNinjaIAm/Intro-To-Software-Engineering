# SELECT queries
SELECT_USER_BY_ID = """
SELECT * FROM user WHERE user_id = {user_id};
"""

SELECT_ALL_USERS = """
SELECT * FROM user;
"""

SELECT_ITEMS_WITH_QUANTITY_GREATER_THAN = """
SELECT * FROM inventory WHERE quantity > {quantity};
"""

SELECT_REVIEWS_FOR_ITEM = """
SELECT * FROM review WHERE item_id = {item_id};
"""

SELECT_ORDERS_BY_USER_ID = """
SELECT * FROM orders WHERE user_id = {user_id};
"""

# INSERT queries
INSERT_NEW_USER = """
INSERT INTO user (user_id, username, password_hash, email, first_name, last_name)
VALUES ({user_id}, '{username}', '{password_hash}', '{email}', '{first_name}', '{last_name}');
"""

INSERT_NEW_ITEM = """
INSERT INTO inventory (item_id, item_name, quantity, price)
VALUES ({item_id}, '{item_name}', {quantity}, {price});
"""

INSERT_NEW_REVIEW = """
INSERT INTO review (review_id, user_id, item_id, rating, subject, text, created_at)
VALUES ({review_id}, {user_id}, {item_id}, {rating}, '{subject}', '{text}', '{created_at}');
"""

INSERT_NEW_ORDER = """
INSERT INTO orders (order_id, user_id, status, created_at, delivered_at)
VALUES ({order_id}, {user_id}, '{status}', '{created_at}', {delivered_at});
"""

# UPDATE queries
UPDATE_USER_EMAIL = """
UPDATE user SET email = '{new_email}' WHERE user_id = {user_id};
"""

UPDATE_ITEM_PRICE = """
UPDATE inventory SET price = {new_price} WHERE item_id = {item_id};
"""

UPDATE_ORDER_STATUS = """
UPDATE orders SET status = '{new_status}' WHERE order_id = {order_id};
"""

# DELETE queries
DELETE_USER_BY_ID = """
DELETE FROM user WHERE user_id = {user_id};
"""

DELETE_ITEM_BY_ID = """
DELETE FROM inventory WHERE item_id = {item_id};
"""

DELETE_REVIEW_BY_ID = """
DELETE FROM review WHERE review_id = {review_id};
"""

DELETE_ORDER_BY_ID = """
DELETE FROM orders WHERE order_id = {order_id};
"""

# DROP queries
drop_queries = {
    'DROP_CART_TABLE': """
        DROP TABLE IF EXISTS cart;
    """,
    'DROP_ORDERS_TABLE': """
        DROP TABLE IF EXISTS orders;
    """,
    'DROP_PAYMENT_INFO_TABLE': """
        DROP TABLE IF EXISTS payment_info;
    """,
    'DROP_SHIPPING_ADDRESS_TABLE': """
        DROP TABLE IF EXISTS shipping_address;
    """,
    'DROP_REVIEW_TABLE': """
        DROP TABLE IF EXISTS review;
    """,
    'DROP_INVENTORY_TABLE': """
        DROP TABLE IF EXISTS inventory;
    """,
    'DROP_USER_TABLE': """
        DROP TABLE IF EXISTS user;
    """
}
