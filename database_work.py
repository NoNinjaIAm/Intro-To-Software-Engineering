import sql_functions as sf


def generate_users():
	# generating data
	uname = None
	psw = None
	email = None
	fname = None
	lname = None

	shipping_key = None
	payment_key = None
	state = None


	# adding to table
	sf.execute_statement(connection, f'SELECT user_id FROM user')


def generate_inventory():
	pass

print("Working...")

# sf.execute_statement
# (connection, f'SELECT user_id FROM user')
"""
sf.execute_statement
(conn, 
f'UPDATE shipping_address SET state=\'{state}\',postal_code=\'{code}\' WHERE 
user_id={get_current_id(conn)}')
"""


'''with sf.create_connection('database.db') as conn:
	print('Adding pending table..')
	sf.execute_statement(conn, f'CREATE TABLE pending (\
    pending INT PRIMARY KEY,\
    userID INT NOT NULL,\
    FOREIGN KEY (userID) REFERENCES user(userID)\
);')
'''
# checking if tables there
'''with sf.create_connection('database.db') as conn:
	print('\ntesting table')
	sf.execute_statement(conn, f'SELECT userID FROM user')
	sf.execute_statement(conn, f'SELECT itemID FROM inventory')
	sf.execute_statement(conn, f'SELECT dataID FROM analytics')
	sf.execute_statement(conn, f'SELECT cartID FROM cart')
	print('\norders...')
	sf.execute_statement(conn, f'SELECT orderID FROM order')
	sf.execute_statement(conn, f'SELECT paymentID FROM paymentInfo')
	sf.execute_statement(conn, f'SELECT shippingID FROM shippingInfo')
'''

'''with sf.create_connection('database.db') as conn:
	print('\nadding data')
	for num in range(1, 10):
		sf.execute_statement(conn, f'INSERT INTO analytics (dataID, itemID, quantitySold) VALUES ({num}, {num+10}, 1)')
'''
'''with sf.create_connection('database.db') as conn:
	print("\n inserting into featured")
	sf.execute_statement(conn, f'INSERT INTO featured (featuredID,itemID,type) VALUES (1,2,0)')'''



with sf.create_connection('database.db') as conn:
	print("Printing table")
	sf.execute_statement(conn,f'SELECT * FROM inventory')
	sf.execute_statement(conn,f'SELECT * FROM cart')
	sf.execute_statement(conn,f'SELECT * FROM user')



'''with sf.create_connection('database.db') as conn:
	print('\n fixing cart table')
	sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES (1, 1, 1, 4)')
'''

print("End...")