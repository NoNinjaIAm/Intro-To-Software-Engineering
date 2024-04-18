from flask import Flask, render_template, request, redirect, url_for, abort
import sql_functions as sf
import time
import re


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


class User:
  def __init__(self, userID, username):
    self.userID = 0
    self.username = username
    self.password = None
    self.type = None
    self.fname = None
    self.lname = None
    self.email = None
    self.shippingData = None
    self.shipping_ptr = 0
    self.paymentData = None
    self.payment_ptr = 0
    self.cartData = None
    self.cart_ptr = 0
    # structured like itemID: quantity

  def reset(self):
  	self.userID = 0
  	self.username = None
  	self.password = None
  	self.type = None
  	self.fname = None
  	self.lname = None
  	self.email = None
  	self.shippingData = None
  	self.shipping_ptr = 0
  	self.paymentData = None
  	self.payment_ptr = 0
  	self.cartData = None
  	self.cart_ptr = 0				# formerly cart_ptr

  def from_db_to_class_cart(self):
  	if self.cartData == None or self.cartData == {}:
  		return
  	with sf.create_connection('database.db') as conn:
  		results = sf.execute_statement(conn, f'SELECT itemID, quantity FROM cart WHERE userID={self.userID}')

  		if results == []:
  			self.cartData = None
  		else:
  			self.cartData.clear()
  			for item in results:
  				self.cartData[int(item[0])] = item[1]

  	print("cart =>", self.cartData)

  def from_db_to_class(self):
  	if self.userID != None:
	  	with sf.create_connection('database.db') as conn:
			  # get user data
			  data = sf.execute_statement(conn, f'SELECT username, type, fname, lname, email, cart_ptr FROM user WHERE userID={self.userID}')[0]
			  self.username = data[0]
			  self.type = data[1]
			  self.fname = data[2]
			  self.lname = data[3]
			  self.email = data[4]
			  self.cart_ptr = data[5]
			  
			  # get payment data
			  data = sf.execute_statement(conn, f'SELECT cardNumber, cardholderName, cardDate FROM paymentInfo WHERE userID={self.userID}')

			  if data == []:
			  	self.paymentData = {
						'cardNumber': 0,
						'cardholderName': None,
						'cardDate': None
					}

			  else:
			  	data = data[0]
			  	self.paymentData = {
						'cardNumber': data[0],
						'cardholderName': data[1],
						'cardDate': data[2]
					}

				
			  data = sf.execute_statement(conn, f'SELECT street, city, state, zip, country FROM shippingInfo WHERE userID={self.userID}')
			  if data == []:
			  	self.shippingData = {
						'street': None,
						'city': None,
						'state': None,
						'zip': 0,
						'country': None
					}
			  else:
			  	data = data[0]
			  	self.shippingData = {
						'street': data[0],
						'city': data[1],
						'state': data[2],
						'zip': data[3],
						'country': data[4]
					}


			  data = sf.execute_statement(conn, f'SELECT itemID, quantity FROM cart WHERE userID={self.userID}')
			  if data == []:
			  	self.cartData = None
			  else:
			  	data = data[0]
			  	self.cartData = {
						data[0]: data[1]
					}
 
  def to_db_from_class_user(self):
  	if self.userID != None:
  		with sf.create_connection('database.db') as conn:
  			uname = self.username
  			email = self.email
  			fname = self.fname
  			lname = self.lname
  			type = self.type

  			isUserInTable = sf.execute_statement(conn, f'SELECT userID FROM user WHERE userID={self.userID}')

  			if (isUserInTable == []):
  				self.userID = new_id('userID', 'user')
  				shipping_ptr = new_id('shippingID', 'shippingInfo')
  				payment_ptr = new_id('paymentID', 'paymentInfo')
  				cart_ptr = new_id('cartID', 'cart')


  				# adding to user table
  				sf.execute_statement(conn, f'INSERT INTO user (userID, username, password_hash, email, fname, lname, type, shipping_ptr, payment_ptr, cart_ptr) VALUES ({self.userID}, \'{uname}\', \'{self.password}\', \'{email}\', \'{fname}\', \'{lname}\', {type}, {shipping_ptr}, {payment_ptr}, {cart_ptr})');
  			else:
  				sf.execute_statement(conn, f'UPDATE user SET username=\'{uname}\',email=\'{email}\',fname=\'{fname}\',lname=\'{lname}\' WHERE userID=\'{self.userID}\'')

  def to_db_from_class_payment(self):
  	if self.userID != None:
  		with sf.create_connection('database.db') as conn:
  			# payment information
  			num = self.paymentData['cardNumber']
  			name = self.paymentData['cardholderName']
  			date = self.paymentData['cardDate']


  			isUserInTable = sf.execute_statement(conn, f'SELECT userID FROM paymentInfo WHERE userID={self.userID}')

  			if (isUserInTable == []):
  				newPaymentID = new_id('paymentID', 'paymentInfo')

  				# making connection from user to paymentInfo
  				sf.execute_statement(conn, f'UPDATE user SET payment_ptr={newPaymentID} WHERE userID={self.userID}') 

  				# adding to paymentInfo table
  				sf.execute_statement(conn, f'INSERT INTO paymentInfo (paymentID, userID, cardNumber, cardholderName, cardDate) VALUES ({newPaymentID}, {self.userID}, {num}, \'{name}\', {date}');

  			else:
  				sf.execute_statement(conn, f'UPDATE paymentInfo SET cardNumber=\'{num}\',cardholderName=\'{name}\',cardDate=\'{date}\' WHERE userID=\'{self.userID}\'')
  	
  def to_db_from_class_shipping(self):
  	if self.userID != None:
  		with sf.create_connection('database.db') as conn:
  			street = self.shippingData['street']
  			city = self.shippingData['city']
  			state = self.shippingData['state']
  			zip = self.shippingData['zip']
  			country = self.shippingData['country']


  			isUserInTable = sf.execute_statement(conn, f'SELECT userID FROM shippingInfo WHERE userID={self.userID}')

  			if (isUserInTable == []):
  				newShippingID = new_id('shippingID', 'shippingInfo')

  				# making connection from user to shippingInfo
  				sf.execute_statement(conn, f'UPDATE user SET shipping_ptr={newShippingID} WHERE userID={self.userID}') 

  				# adding to shippingInfo table
  				sf.execute_statement(conn, f'INSERT INTO shippingInfo (shippingID, userID, street, city, state, zip, country) VALUES ({newShippingID}, {self.userID}, \'{street}\', \'{city}\', \'{state}\', \'{zip}\', \'{country}\'');

  			else:
  				sf.execute_statement(conn, f'UPDATE shippingInfo SET street=\'{street}\', city=\'{city}\', state=\'{state}\', zip=\'{zip}\', country=\'{country}\' WHERE userID=\'{self.userID}\'')

  def to_db_from_class_cart(self):
  	if self.userID != None:
  		with sf.create_connection('database.db') as conn:
  			# clearing user from table and sending in new info
  			sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={self.userID}')


  			# if cart empty and if cart unempty
  			print("db cart =>", self.cartData)
  			if self.cartData == None:
  				pass
  			else:
	  			for item in self.cartData:
	  				print("cart item",item,self.cartData[item])
	  				itemID = item
	  				quantity = self.cartData[item]
	  				price = sf.execute_statement(conn, f'SELECT price FROM inventory WHERE itemID={itemID}')
	  				if price == []:
	  					print('not in inventory')
	  				else:
	  					price = price[0][0]

	  				newCartID = new_id('cartID', 'cart')
	  				sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES ({newCartID}, {self.userID}, {itemID}, {quantity})');

  def add_to_cart(self, itemID, quantity=1):
  	with sf.create_connection('database.db') as conn:
  		results = sf.execute_statement(conn, f'SELECT itemID, quantity FROM cart WHERE userID={self.userID}')
  		if results == []:
  			self.cartData = {itemID: quantity}
  			print('add_to_cart =>',self.cartData)
  			self.to_db_from_class_cart()

  		else:
  			cartQuantity = sf.execute_statement(conn, f'SELECT quantity FROM cart WHERE userID={self.userID} AND itemID={itemID}')
  			inventoryQuantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE itemID={itemID}')
  			if inventoryQuantity != []:
  				inventoryQuantity = inventoryQuantity[0][0]
  				print(inventoryQuantity)
  			else:
  					return

  			if (cartQuantity != []):
  				cartQuantity = cartQuantity[0][0]
  				newQuantity = cartQuantity + quantity

  				if newQuantity < 1:
  					sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={self.userID} AND itemID={itemID}')
  					self.from_db_to_class_cart()
  				elif newQuantity > inventoryQuantity:
  					newQuantity = inventoryQuantity

  				sf.execute_statement(conn, f'UPDATE cart SET quantity={newQuantity} WHERE itemID={itemID} AND userID={self.userID}')
  			else:
  				cartQuantity = quantity
  				newCartId = new_id('cartID', 'cart')
  				sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES ({newCartId}, {current_user.userID}, {itemID}, {quantity})')
  		

class ItemsToCompare:
	def __init__(self):
		self.item1 = None
		self.item2 = None



def search_inventory(item):
	with sf.create_connection('database.db') as conn:
		if "FROM" in item.upper() or "CREATE" in item.upper() or "DROP" in item.upper() or "INTO" in item.upper() or "WHERE" in item.upper():
			return None

		results = sf.execute_statement(conn, f'SELECT itemName,quantity,price,itemID FROM inventory WHERE itemName LIKE \'%{item}%\'')
		return results


def admin_inventory_search(item):
	if "FROM" in item.upper() or "CREATE" in item.upper() or "DROP" in item.upper() or "INTO" in item.upper() or "WHERE" in item.upper():
		return None
	with sf.create_connection('database.db') as conn:
		results = sf.execute_statement(conn, f'SELECT itemName,quantity,price,itemID,userID FROM inventory WHERE itemName LIKE \'%{item}%\'')
		uname = ""
		if results == []:
			return []
		else:
			uname = results[0][4]

		data = []
		for item in results:
			username = sf.execute_statement(conn, f'SELECT username FROM user WHERE userID={uname}')
			if username == []:
				return []
			else:
				username = username[0][0]

			itemID = item[3]
			sold = sf.execute_statement(conn, f'SELECT quantitySold FROM analytics WHERE itemID={itemID}')
			if sold == []:
				return []
			else:
				sold = sold[0][0]



			temp = {
			'itemName': item[0],
			'quantity': item[1],
			'price': item[2],
			'sold': sold,
			'itemID': itemID,
			'username': username
			}
			data.append(temp)

		return data


def search_users(username):
	if "FROM" in username.upper() or "CREATE" in username.upper() or "DROP" in username.upper() or "INTO" in username.upper() or "WHERE" in username.upper():
		return []
	with sf.create_connection('database.db') as conn:
		results = sf.execute_statement(conn, f'SELECT userID, username, email, type FROM user WHERE username LIKE \'%{username}%\'')

		data = []
		for account in results:
			userID = account[0]
			pendingBool = bool(sf.execute_statement(conn, f'SELECT * FROM pending WHERE userID={userID}'))



			temp = {
			'userID': account[0],
			'username': account[1],
			'email': account[2],
			'type': account[3],
			'pending': pendingBool
			}
			data.append(temp)

		return data


def get_cart(user):
	user.from_db_to_class_cart()
	returnCart = []
	cart = user.cartData
	total = 0

	if cart != None:
		with sf.create_connection('database.db') as conn:
			for ID in cart:
				results = sf.execute_statement(conn, f'SELECT price, itemName FROM inventory WHERE itemID={ID}')

				if results == []:
					pass
				else:
					price = results[0][0]
					name = results[0][1]
					total += cart[ID] * price
					returnCart.append({'itemID': ID, 'itemName':name, 'quantity': cart[ID], 'price': price})
	else:
		cart = []

	return returnCart,total


def general_sanitize(string):
	if "FROM" in string.upper() or "CREATE" in string.upper() or "DROP" in string.upper() or "INTO" in string.upper() or "WHERE" in string.upper():
		return None
	else:
		return string


def is_valid(pattern, text):
	matches = re.findall(pattern, text)

	print('\nregex =>',matches, bool(matches), '\n')

	return bool(matches)


web_app = Flask(__name__)
current_user = User(None, None)
comparison = ItemsToCompare()



# done
@web_app.route("/", methods=["GET", "POST"])
def home_page():
	print(f'Current User: ',current_user.username)
	results = None
	fruitResults = None
	fruitData = []
	veggieResults = None
	veggieData = []


	current_user.to_db_from_class_cart()


	if current_user.type == 1:
		buyerList=[]
		# removing item
		if request.method == "POST":
			if 'removeItem' in request.form:
				itemID = request.form['removeItem']
				with sf.create_connection('database.db') as conn:
					sf.execute_statement(conn, f'DELETE FROM inventory WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM analytics WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM cart WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM orders WHERE itemID={itemID}')

			if 'buyerList' in request.form:
				with sf.create_connection('database.db') as conn:
					itemID = request.form['buyerList']
					userIDlist = sf.execute_statement(conn, f'SELECT userID FROM orders WHERE itemID={itemID}')

					for userID in userIDlist:
						userID = userID[0]
						username = sf.execute_statement(conn, f'SELECT username FROM user WHERE userID={userID}')

						if username == [] or username == None:
							pass
						else:
							username = username [0][0]
							buyerList.append(username)

				
		
			# adding to inventory
			if 'addToInventory' in request.form:
				price, name, amount = None, None, None
				if request.form['new_price']: price = request.form['new_price']
				if request.form['new_amount']: amount = request.form['new_amount']
				if request.form['item_name']: name = request.form['item_name']

				if None in (price, name, amount):
					pass
				else: 
					with sf.create_connection('database.db') as conn:
						itemID = new_id('itemID', 'inventory')
						userID = current_user.userID
						analyticsID = new_id('dataID', 'analytics')
						itemName = name
						quantity = amount
						print("\nadding item to inventory and analytics...")
						sf.execute_statement(conn, f'INSERT INTO inventory (itemID, userID, analyticsID, itemName, quantity, price) VALUES ({itemID}, {userID}, {analyticsID}, \'{itemName}\', {quantity}, {price})')
						sf.execute_statement(conn, f'INSERT INTO analytics (dataID, itemID, quantitySold) VALUES ({analyticsID}, {itemID}, 0)')




		# getting list
		totalData = []
		print("buyerList =>", buyerList)
		with sf.create_connection('database.db') as conn:
			itemData = sf.execute_statement(conn, f'SELECT itemName,price,itemID FROM inventory WHERE userID={current_user.userID}')
			
			for item in itemData:
				itemMetadata = sf.execute_statement(conn, f'SELECT quantitySold FROM analytics WHERE itemID={item[2]}')
				if itemMetadata == []:
					pass 
				else:
					print("\nsold =>", itemMetadata)
					data = {
						'name': item[0],
						'price': item[1],
						'sold': itemMetadata[0][0],
						'itemID': item[2]
					}
					print(data)
					
					totalData.append(data)


		return render_template('seller_home.html', productList=totalData, buyerList=buyerList)
	elif current_user.type == 0:
		if request.method == "POST" and 'action' in request.form:
			# add to cart
			itemID = request.form['add']

			current_user.add_to_cart(2,1)
					

		with sf.create_connection('database.db') as conn:
			fruitResults = sf.execute_statement(conn, f'SELECT itemID FROM featured WHERE type=0')
			veggieResults = sf.execute_statement(conn, f'SELECT itemID FROM featured WHERE type=1')

			for item in fruitResults:
				results = sf.execute_statement(conn, f'SELECT itemName, price FROM inventory WHERE itemID={item[0]}')
				if results == []:
					return render_template('buyer_home.html')
				else:
					results = results[0]

				name = results[0]
				price = results[1]

				data = {
				'name': name,
				'price': price,
				'itemID': item[0]
				}
				fruitData.append(data)
			for item in veggieResults:
				results = sf.execute_statement(conn, f'SELECT itemName, price FROM inventory WHERE itemID={item[0]}')
				if results == []:
					return render_template('buyer_home.html')
				else:
					results = results[0]

				name = results[0]
				price = results[1]

				data = {
				'name': name,
				'price': price,
				'itemID': item[0]
				}
				veggieData.append(data)

		current_user.from_db_to_class_cart()
		return render_template('buyer_home.html', fruits=fruitData, veggies=veggieData)
	elif current_user.type == 3:
		print("admin portal")
		return redirect(url_for('admin_user'))
	else: 
		return redirect(url_for('login_page'))


# done
@web_app.route("/login", methods=["GET", "POST"])
def login_page():
	if request.method == "POST":
		if 'login' in request.form:
			# gather credentials
			psw = request.form['password']
			uname = request.form['username']


			# sanitizing
			psw = general_sanitize(psw)
			uname = general_sanitize(uname)

			# getting credentials to match against
			credentials = None
			with sf.create_connection('database.db') as conn:
				credentials = sf.execute_statement(conn, f'SELECT username, password_hash FROM user WHERE username=\'{uname}\'')


			# username filter
			if credentials == []:
				print('Incorrect credentials')
				return render_template('login.html', invalid_credentials=True)

			# checking against password
			if psw != credentials[0][1] or uname != credentials[0][0]:
				print('Incorrect credentials')
				return render_template('login.html', invalid_credentials=True)




			print("\nCorrect credentials\n")
			current_user.username = uname


			# setting up user cache
			with sf.create_connection('database.db') as conn:
				userID = sf.execute_statement(conn, f'SELECT userID FROM user WHERE username=\'{current_user.username}\'')
				current_user.userID = userID[0][0]
				current_user.from_db_to_class()

			print("\nusername, ID, type => ", current_user.username, current_user.userID, current_user.type)


			# filtering for pending accounts
			pending = False
			with sf.create_connection('database.db') as conn:
				pending = bool(sf.execute_statement(conn, f'SELECT * FROM pending WHERE userID={current_user.userID}'))

			if (pending == True):
				print(f'{current_user.username} has a pending account...\n')
				current_user.reset()
				return render_template('login.html', pendingAccount=True)


			return redirect(url_for('home_page'))

		if 'registerAccount' in request.form:
			return redirect(url_for("register_page"))

	return render_template('login.html')


# done
@web_app.route("/register", methods=["GET", "POST"])
def register_page():
	if request.method == "POST":
		new_email = general_sanitize(request.form["email"])
		new_uname = general_sanitize(request.form["uname"])
		new_psw = general_sanitize(request.form["psw"])
		psw_repeat = general_sanitize(request.form["psw-repeat"])
		user_type = general_sanitize(request.form["user_type"])


		
		if not is_valid(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', new_email): return render_template('register.html', incorrect=True) 
		if not is_valid(r'^[a-zA-Z0-9_-]{3,20}$', new_uname): return render_template('register.html', incorrect=True)
		if not is_valid(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$', new_psw): return render_template('register.html', incorrect=True)




		uname_filter = None
		with sf.create_connection('database.db') as conn:
			uname_filter = sf.execute_statement(conn, f'SELECT * FROM user WHERE username=\'{new_uname}\'')

		if uname_filter != []:
			return render_template('register.html', taken=True)

		if new_psw != psw_repeat:
			return render_template('register.html', incorrect=True)


		current_user.reset()

		# adding user data to class
		current_user.username = new_uname
		current_user.email = new_email
		current_user.password = new_psw
		current_user.type = int(user_type)


		# missing password and pointers
		current_user.to_db_from_class_user()

		if current_user.type == 1:
			with sf.create_connection('database.db') as conn:
				newPendingID = new_id('pending', 'pending')
				sf.execute_statement(conn, f'INSERT INTO pending (pending, userID) VALUES ({newPendingID}, {current_user.userID})')



		return redirect(url_for('login_page'))
	return render_template('register.html')


# done
@web_app.route("/settings", methods=["GET", "POST"])
def settings_page():
	if current_user.type == 0 or current_user.type == 1:
		setting_data = None

		# editing account
		if request.method == "POST":
			if 'logout' in request.form:
				print(f'{current_user.username} is logging out...')

				current_user.reset()

				return redirect(url_for("login_page"))

			if 'new_info' in request.form:
				if request.form['new_uname'] and is_valid(r'^[a-zA-Z0-9_-]{3,20}$', request.form['new_uname']): 
					current_user.username = general_sanitize(request.form['new_uname'])
				if request.form['new_email'] and is_valid(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}',request.form['new_email']):
						current_user.email = general_sanitize(request.form['new_email'])
				
				# shipping data
				if request.form['new_street'] and is_valid(r'^.{1,100}$', request.form['new_street']): 
					current_user.shippingData['street'] = general_sanitize(request.form['new_street'])
				if request.form['new_state'] and is_valid(r'^[A-Z]{2}', request.form['new_state']): 
					current_user.shippingData['state'] = general_sanitize(request.form['new_state'])
				if request.form['new_city'] and is_valid(r'^.{1,100}$', request.form['new_city']): 
					current_user.shippingData['city'] = general_sanitize(request.form['new_city'])
				if request.form['new_zip'] and is_valid(r'^\d{5}', request.form['new_zip']): 
					current_user.shippingData['zip'] = general_sanitize(request.form['new_zip'])

				# payment data
				if request.form['new_card_num'] and is_valid(r'^\d{16}$', request.form['new_card_num']): 
					current_user.paymentData['cardNumber'] = general_sanitize(request.form['new_card_num'])
				if request.form['new_cardholder_name'] and is_valid(r'^[A-Za-z -]{1,100}$', request.form['new_cardholder_name']): 
					current_user.paymentData['cardholderName'] = general_sanitize(request.form['new_cardholder_name'])
				if request.form['new_date'] and is_valid(r'^(0[1-9]|1[0-2])\/[0-9]{2}$', request.form['new_date']): 
					current_user.paymentData['cardDate'] = general_sanitize(request.form['new_date'])
				


				current_user.to_db_from_class_user()
				current_user.to_db_from_class_payment()
				current_user.to_db_from_class_shipping()

			if 'deleteAccount' in request.form:
				with sf.create_connection('database.db') as conn:
					# deleting all information
					sf.execute_statement(conn, f'DELETE FROM user WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM inventory WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM analytics WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM paymentInfo WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM shippingInfo WHERE userID={current_user.userID}')
					sf.execute_statement(conn, f'DELETE FROM orders WHERE userID={current_user.userID}')
					return redirect(url_for('login_page'))


		settings_data = {
				'username': current_user.username,
				'email': current_user.email,
				'fname': current_user.fname,
				'lname': current_user.lname,
				'street': current_user.shippingData['street'],
				'state': current_user.shippingData['state'],
				'city': current_user.shippingData['city'],
				'zip': current_user.shippingData['zip'],
				'cardNumber': current_user.paymentData['cardNumber'],
				'cardholderName': current_user.paymentData['cardholderName'],
				'cardDate': current_user.paymentData['cardDate']
		}

		if "edit" not in request.form:
			return render_template('buyer_settings.html', data=settings_data)
		else:
			return render_template('buyer_settings.html', edit=True)
	else: 
		return redirect(url_for('login_page'))


# done
@web_app.route("/search", methods=["GET", "POST"])
def search_page():
	if current_user.type == 0:
		if request.method == "GET":
			return render_template('search.html')
		elif request.method == "POST":
			if 'query' in request.form:
				query = request.form['query']

				#sanitizing
				if type(query) != type(None):
					query = general_sanitize(query)

				if query == None:
					return render_template('search.html')
				
				results = search_inventory(query)

				if results != []:
					return render_template('search.html', list=results)


			if 'action' in request.form:
				# add to cart
				itemID = request.form['add']
				
				current_user.add_to_cart(itemID)
				return redirect(url_for('search_page'))
					



			return render_template('search.html')
	else:
		return redirect(url_for('login_page'))


# done
@web_app.route("/cart", methods=["GET", "POST"])
def cart_page():
	if current_user.type == 0:
		totalData, total = get_cart(current_user)



		paid = False
		# item name, price, quantity
		if request.method == "POST" and 'action' in request.form:
			# add to cart
			if request.form['action'] == '+':
				print('\nAdding to cart...')
				itemID = request.form['itemID']


				current_user.add_to_cart(itemID,1)

				return redirect(url_for('cart_page'))

			else:	# remove from cart
				print('Removing from cart')
				# update database
				itemID = request.form['itemID']

				current_user.add_to_cart(itemID,-1)

				return redirect(url_for('cart_page'))

					
		# paying for cart
		if request.method == "POST" and 'payButton' in request.form:
			print("\nPaying...")


			# add data to orders table
			with sf.create_connection('database.db') as conn:
				cart, total = get_cart(current_user)

				# consistent variables
				cardNumber = current_user.paymentData['cardNumber']
				cardholderName = current_user.paymentData['cardholderName']
				cardDate = current_user.paymentData['cardDate']

				street = current_user.shippingData['street']
				city = current_user.shippingData['city']
				state = current_user.shippingData['state']
				zip = current_user.shippingData['zip']
				country = current_user.shippingData['country']

				orderTime = time.time()


				# add data to orders table
				for item in cart:
					orderID=new_id('orderID', 'orders') # add price into orders
					userID = current_user.userID
					itemID = item['itemID']
					quantity = item['quantity']
					price = item['price']
					sf.execute_statement(conn, f'INSERT INTO orders (orderID, userID, itemID, price, quantity, orderTime, cardNumber, cardholderName, cardDate, street, city, state, zip, country) VALUES ({orderID}, {userID}, {itemID}, {price}, {quantity}, 0, {cardNumber}, \'{cardholderName}\', 0, \'{street}\', \'{city}\', \'{state}\', \'{zip}\', \'{country}\')')
					print("insert test => ",sf.execute_statement(conn, f'SELECT * FROM orders WHERE orderID={orderID}'))

			
				# add data to analytics table
				for item in cart:
					itemID = item['itemID']
					quantitySold = sf.execute_statement(conn, f'SELECT quantitySold FROM analytics WHERE itemID={itemID}')

					if quantitySold == []:
						pass 
					else:
						quantitySold = quantitySold[0][0]
						quantitySold += item['quantity']
						sf.execute_statement(conn, f'UPDATE analytics SET quantitySold={quantitySold} WHERE itemID={itemID}')

				# remove items from inventory
				for item in cart:
					itemID = item['itemID']
					currentQuantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE itemID={itemID}')

					if currentQuantity == []:
						pass 
					else:
						currentQuantity = currentQuantity[0][0]
						currentQuantity -= item['quantity']

						sf.execute_statement(conn, f'UPDATE inventory SET quantity={currentQuantity} WHERE itemID={itemID}')


				# clear cart
				current_user.cartData = None
				current_user.to_db_from_class_cart()
				paid = True
				totalData, total = get_cart(current_user)
				request.method = "GET"
				return render_template('cart.html', list=totalData, cartPrice=total, bool=paid)


			
			return render_template('cart.html', list=totalData, cartPrice=total, bool=paid)


		if request.method == "POST" and 'compareButton' in request.form:
			print("comparing =>",request.form['compareButton'])
			with sf.create_connection('database.db') as conn:
				itemID = int(request.form['compareButton'])
				temp = sf.execute_statement(conn, f'SELECT itemName,price, quantity FROM inventory WHERE itemID={itemID}')
				print('item data for compare =>', temp)

				if temp != []:
					temp = temp[0]

					if (comparison.item1 != None and comparison.item2 != None):
						comparison.item1 = {
							'name': temp[0],
							'price': temp[1],
							'quantity': temp[2]
						}

					elif (comparison.item1 == None):
						comparison.item1 = {
							'name': temp[0],
							'price': temp[1],
							'quantity': temp[2]
						}

					else:
						comparison.item2 = {
							'name': temp[0],
							'price': temp[1],
							'quantity': temp[2]
						}
				

		if request.method == "POST" and 'removeFirstItem' in request.form:
			comparison.item1 = None

		if request.method == "POST" and 'removeSecondItem' in request.form:
			comparison.item2 = None


		print("item1 =>", comparison.item1)
		print("item2 =>", comparison.item2)
		return render_template('cart.html', list=totalData, cartPrice=total, bool=paid, compare1=comparison.item1, compare2=comparison.item2)
	else:
		return redirect(url_for('login_page'))


# done
@web_app.route("/order_history", methods=["GET", "POST"])
def order_history_page():
	if current_user.type == 0:
		if 'returnItem' in request.form:
			orderID = request.form['returnItem']
			print("return value", request.form['returnItem'])

			with sf.create_connection('database.db') as conn:
				currentQuantity = None
				itemID = 0
				quantity = 0

				results = sf.execute_statement(conn, f'SELECT itemID,quantity FROM orders WHERE orderID={orderID}')
				if results == []:
					itemID, quantity = results [0]
				else:
					pass
				currentQuantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE itemID={itemID}')

				if (currentQuantity == []):
					print('cannot return item, it doesn\'t exist in inventory')
				else:
					currentQuantity = currentQuantity[0]
					sf.execute_statement(conn, f'UPDATE inventory SET quantity={currentQuantity+amountToAdd} WHERE itemID={itemID}')





		# getting order history
		results = None
		with sf.create_connection('database.db') as conn:
			results = sf.execute_statement(conn, f'SELECT orderID,quantity,itemID FROM orders WHERE userID={current_user.userID}')

		print("results =>", results)

		totalData = []

		if results != []:
			with sf.create_connection('database.db') as conn:
				for item in results:
					itemData = sf.execute_statement(conn, f'SELECT itemName, price FROM inventory WHERE itemID={item[2]}')
					if itemData != []:
						itemData = itemData[0]
					else:
						continue
					data = {
						'orderID': item[0],
						'quantity': item[1],
						'name': itemData[0],
						'price': itemData[1]
					}
					totalData.append(data)


		return render_template('order_history.html', order_history=totalData)
	else:
		return redirect(url_for('login_page'))


# done
@web_app.route("/users", methods=["GET","POST"])
def admin_user():
	if current_user.type == 3:
		query = ""
		if request.method == "POST":
			if 'logoutButton' in request.form:
				current_user.reset()
				print("admin is logging out =>", current_user.username)
				return redirect(url_for('login_page'))

			if 'query' in request.form:
				query = request.form['query']

				#sanitizing
				if type(query) != type(None):
					query = general_sanitize(query)

				if query == None:
					query = ''

			if 'blockUser' in request.form:
				print('user to block =>', request.form['blockUser'])

				with sf.create_connection('database.db') as conn:
					userID = int(request.form['blockUser'])
					sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={userID}')
					sf.execute_statement(conn, f'DELETE FROM user WHERE userID={userID}')
					sf.execute_statement(conn, f'DELETE FROM inventory WHERE userID={userID}')
					sf.execute_statement(conn, f'DELETE FROM orders WHERE userID={userID}')
					sf.execute_statement(conn, f'DELETE FROM paymentInfo WHERE userID={userID}')
					sf.execute_statement(conn, f'DELETE FROM shippingInfo WHERE userID={userID}')

			if 'approval' in request.form:
				with sf.create_connection('database.db') as conn:
					userID = int(request.form['approval'])
					sf.execute_statement(conn, f'DELETE FROM pending WHERE userID={userID}')

		# reuse search_inventory to find users based on search
		users = search_users(query)

		# default search is all users
		return render_template('admin_user.html', userList=users)
	else:
		return redirect(url_for('login_page'))


# done
@web_app.route("/inventory", methods=["GET","POST"])
def admin_inventory():
	if current_user.type == 3:
		query = ""
		if request.method == "POST":
			if 'logoutButton' in request.form:
				current_user.reset()
				print("admin is logging out =>", current_user.username)
				return redirect(url_for('login_page'))

			if 'query' in request.form:
				query = request.form['query']

				#sanitizing
				if type(query) != type(None):
					query = general_sanitize(query)

				if query == None:
					query = ''

			if 'blockItem' in request.form:
				print('item to block =>', request.form['blockItem'])

				with sf.create_connection('database.db') as conn:
					itemID = int(request.form['blockItem'])
					sf.execute_statement(conn, f'DELETE FROM cart WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM inventory WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM orders WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM featured WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM analytics WHERE itemID={itemID}')


		# reuse search_inventory to find users based on search
		items = admin_inventory_search(query)

		# default search is all users
		return render_template('admin_inventory.html', itemList=items)
	else:
		return redirect(url_for('login_page'))


if __name__ == '__main__':
  web_app.run(debug=True)