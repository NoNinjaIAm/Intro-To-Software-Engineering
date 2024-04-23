# helper functions for generating dummy data

import random
import string
from datetime import date
import sql_functions as sf

def new_id(tableID, table):
	with sf.create_connection('database.db') as conn:
		maxID = sf.execute_statement(conn, f'SELECT MAX({tableID}) FROM {table}')

		# empty list filter 2x
		if maxID == [] or maxID == None:
			return 1
		else:
			maxID = maxID[0]
		if maxID == [] or maxID == None:
			return 1
		else:
			maxID = maxID[0]

		if type(maxID) == type(None):
			maxID = 0
		return maxID+1

# default type is customer
def generate_user(type=0):
    with sf.create_connection('database.db') as conn:
        userID = new_id("userID", "user")
		
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
        
        # random generic names for fname and lname
        generic_names = ["Taylor", "Jordan", "Casey", "Morgan", "Alex", "Jamie", "Reese", "Blake", "Avery", "Parker", "Quinn", "Riley", "Sawyer", "Harley", "Ellis"]
        fname = random.choice(generic_names)
        lname = random.choice(generic_names)

        # add generated data to db
        sf.execute_statement(conn, f"""
            INSERT INTO user
            (userID, username, password_hash, email, fname, lname, type, shipping_ptr, payment_ptr, cart_ptr)
            VALUES ({userID}, "{username}", "{password}", "{email}", "{fname}", "{lname}", {type}, {userID}, {userID}, {userID});
            """, fetch_results=False)
        


def generate_item():
    with sf.create_connection('database.db') as conn:
        itemID = new_id("itemID", "inventory")
        
        userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 1")
        # generate a seller if none exist
        if not userID:
            generate_user(1)
            userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 1")[0][0]
        else:
            userID = userID[0][0]
            
        
        analyticsID = sf.execute_statement(conn, "SELECT dataID from analytics")
        # generate an analytics entry if none exist
        if not analyticsID:
            generate_analytics()
            analyticsID = sf.execute_statement(conn, "SELECT dataID from analytics")[0][0]
        else:
            analyticsID = analyticsID[0][0]
        
        # color + fruit/vegetable scheme
        colors = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white", "gray", "beige", "teal", "maroon", "navy"]
        fruits_vegetables = ["apple", "banana", "orange", "grape", "strawberry", "watermelon", "kiwi", "pineapple", "mango", "pear", "peach", "plum", "carrot", "broccoli", "cucumber"]
        itemName = " ".join([random.choice(colors), random.choice(fruits_vegetables)])

        quantity = random.randint(0, 1000)
        price = round(random.random() * 1000, 2)
        
        sf.execute_statement(conn, f"""
            INSERT INTO inventory
            (itemID, userID, analyticsID, itemName, quantity, price)
            VALUES ({itemID}, {userID}, {analyticsID}, "{itemName}", {quantity}, {price});
            """, fetch_results=False)
        
		
def generate_analytics():
    with sf.create_connection('database.db') as conn:
        dataID = new_id("dataID", "analytics")
        itemID = sf.execute_statement(conn, "SELECT itemID from inventory")
        # generate an item if none exist
        if not itemID:
            generate_item()
            itemID = sf.execute_statement(conn, "SELECT itemID from inventory")[0][0]
        else:
            itemID = itemID[0][0]
        quantitySold = random.randint(0, 1000)
		
        sf.execute_statement(conn, f"""
            INSERT INTO analytics
            (dataID, itemID, quantitySold)
            VALUES ({dataID}, {itemID}, {quantitySold});
            """, fetch_results=False)
        

def generate_cart():
    with sf.create_connection('database.db') as conn:
        cartID = new_id("cartID", "cart")
        userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")
        if not userID:
            generate_user(0)
            userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        else:
            userID = userID[0][0]
        itemID = sf.execute_statement(conn, "SELECT itemID from inventory")
        if not itemID:
            generate_item()
            itemID = sf.execute_statement(conn, "SELECT itemID from inventory")[0][0]
        else:
            itemID = itemID[0][0]
        quantity = random.randint(0, 1000)

        sf.execute_statement(conn, f"""
            INSERT INTO cart
            (cartID, userID, itemID, quantity)
            VALUES ({cartID}, {userID}, {itemID}, {quantity});
            """, fetch_results=False)
        
def generate_payment_info():
    with sf.create_connection('database.db') as conn:
        paymentID = new_id("paymentID", "paymentInfo")
        userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")
        if not userID:
            generate_user(0)
            userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        else:
            userID = userID[0][0]
        cardNumber = int(''.join(random.choices(string.digits, k=16)))
        
        generic_names = ["Taylor", "Jordan", "Casey", "Morgan", "Alex", "Jamie", "Reese", "Blake", "Avery", "Parker", "Quinn", "Riley", "Sawyer", "Harley", "Ellis"]
        cardholderName = " ".join(random.choices(generic_names, k=2))
        cardDate = "01/01" 
        
        sf.execute_statement(conn, f"""
            INSERT INTO paymentInfo
            (paymentID, userID, cardNumber, cardholderName, cardDate)
            VALUES ({paymentID}, {userID}, {cardNumber}, "{cardholderName}", "{cardDate}");
            """, fetch_results=False)
        
def generate_shipping_info():
    with sf.create_connection('database.db') as conn:
        shippingID = new_id("shippingID", "shippingInfo")
        userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")
        if not userID:
            generate_user(0)
            userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        else:
            userID = userID[0][0]
        valid_characters = string.ascii_letters + string.digits
        street = ''.join(random.choices(valid_characters, k=10))
        city = ''.join(random.choices(valid_characters, k=10))
        state = ''.join(random.choices(string.ascii_uppercase, k=2))
        zip = ''.join(random.choices(string.digits, k=5))
        country = ''.join(random.choices(valid_characters, k=10))

        sf.execute_statement(conn, f"""
            INSERT INTO shippingInfo
            (shippingID, userID, street, city, state, zip, country)
            VALUES ({shippingID}, {userID}, "{street}", "{city}", "{state}", "{zip}", "{country}");
            """, fetch_results=False)

def generate_order():
    with sf.create_connection('database.db') as conn:
        orderID = new_id("orderID", "orders")
        userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")
        if not userID:
            generate_user(0)
            userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        else:
            userID = userID[0][0]
        itemID = sf.execute_statement(conn, "SELECT itemID from inventory")
        if not itemID:
            generate_item()
            itemID = sf.execute_statement(conn, "SELECT itemID from inventory")[0][0]
        else:
            itemID = itemID[0][0]
        price = random.randint(0, 1000)
        quantity = random.randint(0, 1000)
        orderTime = date.today().strftime('%Y-%m-%d')
        cardNumber = int(''.join(random.choices(string.digits, k=16)))

        generic_names = ["Taylor", "Jordan", "Casey", "Morgan", "Alex", "Jamie", "Reese", "Blake", "Avery", "Parker", "Quinn", "Riley", "Sawyer", "Harley", "Ellis"]
        cardholderName = " ".join(random.choices(generic_names, k=2))
        cardDate = "01/01" 

        valid_characters = string.ascii_letters + string.digits
        street = ''.join(random.choices(valid_characters, k=10))
        city = ''.join(random.choices(valid_characters, k=10))
        state = ''.join(random.choices(string.ascii_uppercase, k=2))
        zip = ''.join(random.choices(string.digits, k=5))
        country = ''.join(random.choices(valid_characters, k=10))

        sf.execute_statement(conn, f"""
            INSERT INTO orders
            (orderID, userID, itemID, price, quantity, orderTime, cardNumber, cardholderName, cardDate, street, city, state, zip, country)
            VALUES ({orderID}, {userID}, {itemID}, {price}, {quantity}, "{orderTime}", {cardNumber}, "{cardholderName}", "{cardDate}", "{street}", "{city}", "{state}", "{zip}", "{country}");
            """, fetch_results=False)

    
def generate_featured(type=random.randint(0,1)):
    with sf.create_connection('database.db') as conn:
        featuredID = new_id("featuredID", "featured")
        itemID = sf.execute_statement(conn, "SELECT itemID from inventory")
        if not itemID:
            generate_item()
            itemID = sf.execute_statement(conn, "SELECT itemID from inventory")[0][0]
        else:
            itemID = itemID[0][0]

        sf.execute_statement(conn, f"""
            INSERT INTO featured
            (featuredID, itemID, type)
            VALUES ({featuredID}, {itemID}, {type});
            """, fetch_results=False)
