import pytest
import backend
import sql_functions as sf
import data_generation as dg
import random
import string
from flask.testing import FlaskClient

@pytest.fixture
def app():
    return backend.web_app

# test home page as seller
def test_home_page_seller(app):
    backend.current_user.type = 1
    with sf.create_connection('database.db') as conn:
        backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 1")
            # generate a seller if none exist
        if not backend.current_user.userID:
            dg.generate_user(1)
            backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 1")[0][0]
        else:
            backend.current_user.userID = backend.current_user.userID[0][0]

    with app.test_client() as client:
        response = client.post('/')
        assert response.status_code == 200
    
# test home page as customer
def test_home_page_customer(app):
    backend.current_user.type = 0
    with sf.create_connection('database.db') as conn:
        backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")
            # generate a customer if none exist
        if not backend.current_user.userID:
            dg.generate_user(0)
            backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        else:
            backend.current_user.userID = backend.current_user.userID[0][0]

    with app.test_client() as client:
        response = client.post('/')
        assert response.status_code == 200

# test home page as invalid user
def test_home_page_invalid(app):
    backend.current_user.type = None
    
    with app.test_client() as client:
        response = client.post('/')
        assert response.status_code == 302

# test login page with correct credentials
def test_successful_login(app):
    credentials = []
    with sf.create_connection('database.db') as conn:
        userID = sf.execute_statement(conn, "SELECT userID from user")
            # generate a customer if none exist
        if not userID:
            dg.generate_user()
            userID = sf.execute_statement(conn, "SELECT userID from user")[0][0]
        else:
            userID = userID[0][0]
        credentials = sf.execute_statement(conn, f'SELECT username, password_hash FROM user WHERE userID = {userID}')
    with app.test_client() as client:
        response = client.post("/login", data={"login": "", "username": credentials[0][0], "password": credentials[0][1]})
        assert response.status_code == 302

# test login page with incorrect credentials
def test_unsuccessful_login(app):
    with app.test_client() as client:
        response = client.post("/login", data={"login": "", "username": "INVALID_USERNAME", "password": "INVALID_PASSWORD"})
        assert response.status_code == 200

# test register page with valid info
def test_register_good(app):
    valid_characters = string.ascii_letters + string.digits
    # random 10-character string for username, password, email
    username = ''.join(random.choices(valid_characters, k=10))
    password = ''
    password += random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += '$'
    password += ''.join(random.choices(valid_characters, k=5))
    
    email = username + "@gmail.com"
    with app.test_client() as client:
        response = client.post("/register", data={"email": email, "uname": username, "psw": password, "psw-repeat": password, "user_type": 0})
        assert response.status_code == 302

# test register page with taken username
def test_register_bad_username(app):
    valid_characters = string.ascii_letters + string.digits
    # random 10-character string for username, password, email
    username = ''
    with sf.create_connection('database.db') as conn:
        username = sf.execute_statement(conn, "SELECT username from user")
        if username:
            username = username[0][0]
        else:
            pass
    password = ''
    password += random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += '$'
    password += ''.join(random.choices(valid_characters, k=5))
    email = username + "@gmail.com"
    with app.test_client() as client:
        response = client.post("/register", data={"email": email, "uname": username, "psw": password, "psw-repeat": password, "user_type": 0})
        assert response.status_code == 200


# test register page with incorrectly-repeated password
def test_register_bad_password(app):
    valid_characters = string.ascii_letters + string.digits
    # random 10-character string for username, password, email
    username = ''.join(random.choices(valid_characters, k=10))
    password = ''
    password += random.choice(string.ascii_lowercase)
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.digits)
    password += '$'
    password += ''.join(random.choices(valid_characters, k=5))
    email = username + "@gmail.com"
    with app.test_client() as client:
        response = client.post("/register", data={"email": email, "uname": username, "psw": password, "psw-repeat": "INVALID_PASSWORD", "user_type": 0})
        assert response.status_code == 200


# settings page - test new data upload
def test_settings_new_data(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0
    valid_characters = string.ascii_letters + string.digits
    username = ''.join(random.choices(valid_characters, k=10))
    email = username + "@gmail.com"
    # shipping data
    street = ''.join(random.choices(valid_characters, k=10))
    city = ''.join(random.choices(valid_characters, k=10))
    state = ''.join(random.choices(string.ascii_uppercase, k=2))
    zip = ''.join(random.choices(string.digits, k=5))
    # payment data
    cardNumber = int(''.join(random.choices(string.digits, k=16)))
    generic_names = ["Taylor", "Jordan", "Casey", "Morgan", "Alex", "Jamie", "Reese", "Blake", "Avery", "Parker", "Quinn", "Riley", "Sawyer", "Harley", "Ellis"]
    cardholderName = " ".join(random.choices(generic_names, k=2))
    cardDate = "01/01" 

    with app.test_client() as client:
        response = client.post('/settings', data={'new_info': '', 'new_uname': username, 'new_email': email, 'new_street': street, 'new_state': state, 'new_city': city, 'new_zip': zip, 'new_card_num': cardNumber, 'new_cardholder_name': cardholderName, 'new_date': cardDate})
        print({'new_info': '', 'new_uname': username, 'new_email': email, 'new_street': street, 'new_state': state, 'new_city': city, 'new_zip': zip, 'new_card_num': cardNumber, 'new_cardholder_name': cardholderName, 'new_date': cardDate})

        assert response.status_code == 200

# settings page - test delete account
def test_settings_delete_account(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0
    with sf.create_connection('database.db') as conn:
        backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user")
        if not backend.current_user.userID:
            dg.generate_user()
            backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user")[-1][0]
        else:
            backend.current_user.userID = backend.current_user.userID[-1][0]
    with app.test_client() as client:
        response = client.post('/settings', data={'deleteAccount': ''})
        assert response.status_code == 302

# settings page - test log out
def test_settings_logout(app):
    backend.current_user.type = 0
    backend.current_user.username = "logout test"

    with app.test_client() as client:
        response = client.post('/settings', data={'logout': ''})
        assert response.status_code == 302

# settings page = test not logged in
def test_settings_unauthenticated(app):
    backend.current_user.type = None
     
    with app.test_client() as client:
        response = client.post('/settings')
        assert response.status_code == 302

# search - test search query
def test_search_query(app):
    backend.current_user.type = 0
    query = ''
    with sf.create_connection('database.db') as conn:
        query = sf.execute_statement(conn, "SELECT itemName from inventory")
        if not backend.current_user.userID:
            dg.generate_item()
            query = sf.execute_statement(conn, "SELECT itemName from inventory")[0][0]
        else:
            query = query[0][0]
    with app.test_client() as client:
        response = client.post('/search', data={'query': query})
        assert response.status_code == 200


# search - test not logged in
def test_search_unauthenticated(app):
    backend.current_user.type = None
    with app.test_client() as client:
        response = client.get('/search')
        assert response.status_code == 302

# search - test add to cart
def test_search_add_to_cart(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0
    itemID = ''
    with sf.create_connection('database.db') as conn:
        maxQty = sf.execute_statement(conn, f"SELECT MAX(quantity) FROM cart WHERE userID = {backend.current_user.userID}")[0][0]
        if not maxQty:
            dg.generate_cart()
            maxQty = sf.execute_statement(conn, f"SELECT MAX(quantity) FROM cart WHERE userID = {backend.current_user.userID}")[0][0]
        itemID = sf.execute_statement(conn, f"SELECT itemID from inventory WHERE quantity > {maxQty}")
        if not itemID:
            dg.generate_item()
            itemID = sf.execute_statement(conn, f"SELECT itemID from inventory WHERE quantity > {maxQty}")[0][0]
        else:
            itemID = itemID[0][0]

    
    with app.test_client() as client:
        response = client.post('/search', data={'action': '', 'add': itemID})
        assert response.status_code == 302

# cart - test not logged in
def test_cart_unauthenticated(app):
    backend.current_user.type = None
    with app.test_client() as client:
        response = client.post('/cart')
        assert response.status_code == 302

# cart - test add to cart
def test_cart_add_to_cart(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0
    itemID = ''
    with sf.create_connection('database.db') as conn:
        maxQty = sf.execute_statement(conn, f"SELECT MAX(quantity) FROM cart WHERE userID = {backend.current_user.userID}")
        if not maxQty:
            dg.generate_cart()
            maxQty = sf.execute_statement(conn, f"SELECT MAX(quantity) FROM cart WHERE userID = {backend.current_user.userID}")[0][0]
        else:
            maxQty = maxQty[0][0]
        itemID = sf.execute_statement(conn, f"SELECT itemID from inventory WHERE quantity > {maxQty}")
        if not itemID:
            dg.generate_item()
            itemID = sf.execute_statement(conn, f"SELECT itemID from inventory WHERE quantity > {maxQty}")[0][0]
        else:
            itemID = itemID[0][0]
    
    with app.test_client() as client:
        response = client.post('/cart', data={'action': '+', 'itemID': itemID})
        assert response.status_code == 302

# cart - test remove from cart
def test_cart_remove_from_cart(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0
    itemID = ''
    with sf.create_connection('database.db') as conn:
        itemID = sf.execute_statement(conn, f"SELECT itemID from cart WHERE userID = {backend.current_user.userID} AND quantity > 0")
        if not itemID:
            dg.generate_cart()
            itemID = sf.execute_statement(conn, f"SELECT itemID from cart WHERE userID = {backend.current_user.userID} AND quantity > 0")[0][0]
        else:
            itemID = itemID[0][0]

    with app.test_client() as client:
        response = client.post('/cart', data={'action': '-', 'itemID': itemID})
        assert response.status_code == 302

# cart - test pay for cart
def test_cart_pay_for_cart(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0

    with sf.create_connection('database.db') as conn:
        itemID = sf.execute_statement(conn, f"SELECT itemID from cart WHERE userID = {backend.current_user.userID} AND quantity > 0")
        if not itemID:
            dg.generate_cart()

    with app.test_client() as client:
        response = client.post('/cart', data={'payButton': ''})
        assert response.status_code == 200

# orders - test return item
def test_order_history_return_item(app):
    backend.current_user.userID = 1
    backend.current_user.type = 0

    orderID = ''
    with sf.create_connection('database.db') as conn:
        orderID = sf.execute_statement(conn, f"SELECT orderID from orders WHERE userID = {backend.current_user.userID}")
        if orderID == None:
            dg.generate_order()
            orderID = sf.execute_statement(conn, f"SELECT orderID from orders WHERE userID = {backend.current_user.userID}")

    with app.test_client() as client:
        response = client.post('order_history', data={'returnItem': orderID})
        assert response.status_code == 200