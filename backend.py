from flask import Flask, render_template, request, redirect, url_for, abort
import sql_functions as sf
import datetime

class User:
    def __init__(self, userID, username):
      self.userID = userID
      self.username = username
      self.type = None
      self.fname = None
      self.lname = None
      self.email = None
      self.shippingData = None
      self.paymentData = None
      self.cart_ptr = None

    def reset(self):
    	self.userID = None
    	self.username = None
    	self.type = None
    	self.fname = None
    	self.lname = None
    	self.email = None
    	self.shippingData = None
    	self.paymentData = None
    	self.cart_ptr = None

    def update_database(self):
    		if self.userID != None:
	    		with sf.create_connection('database.db') as conn:
	    			# user data
	    			sf.execute_statement(conn, f'UPDATE user SET username=\'{self.username}\',fname=\'{self.fname}\',lname=\'{self.lname}\',email=\'{self.email}\' WHERE userID={self.userID}')

	    			# shipping data
	    			street = self.shippingData['street']
	    			city = self.shippingData['city']
	    			state = self.shippingData['state']
	    			zip = self.shippingData['zip']
	    			sf.execute_statement(conn, f'UPDATE shippingInfo SET street=\'{street}\',city=\'{city}\',state=\'{state}\',zip=\'{zip}\' WHERE userID=\'{self.userID}\'')

	    			# payment data
	    			num = self.paymentData['cardNumber']
	    			name = self.paymentData['cardholderName']
	    			date = self.paymentData['cardDate']
	    			sf.execute_statement(conn, f'UPDATE paymentInfo SET cardNumber=\'{num}\',cardholderName=\'{name}\',cardDate=\'{date}\' WHERE userID=\'{self.userID}\'')
	    			sf.execute_statement(conn, f'UPDATE user SET cart_ptr={self.cart_ptr} WHERE userID=\'{self.userID}\'')

    def set_data(self):
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
	    					'cardNumber': None,
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

	    			print(f'Payment data => {self.paymentData}')
	    			# get shipping data
	    			data = sf.execute_statement(conn, f'SELECT street, city, state, zip, country FROM shippingInfo WHERE userID={self.userID}')

	    			if data == []:
	    				self.shippingData = {
	    					'street': None,
	    					'city': None,
	    					'state': None,
	    					'zip': None,
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






def search_inventory(item):
	with sf.create_connection('database.db') as conn:
		results = sf.execute_statement(conn, f'SELECT itemName,quantity,price,itemID FROM inventory WHERE itemName LIKE \'%{item}%\'')
		return results

def get_cart():
	with sf.create_connection('database.db') as conn:
		results = sf.execute_statement(conn, f'SELECT itemID, quantity FROM cart WHERE userID={current_user.userID}')

		print("Cart =>",results)

		# if the cart isn't empty
		if results != []:
			totalData = []
			total = 0
			# getting data of all items in cart
			for item in results:
				itemID, quantity = item

				itemData = sf.execute_statement(conn, f'SELECT itemName, price, itemID FROM inventory WHERE itemID={itemID}')
				
				print("itemData =>",itemData)
				# filtering for empty cart pt 2
				if itemData == []:
					return [], None

				else:
					itemData = itemData[0]


				data = [
					itemData[0],
					quantity,
					itemData[1],
					itemData[2]
				]
				totalData.append(data)


			# getting the total price
			for item in totalData:
				total += item[1]*item[2]

			return totalData, total 
		return [], None

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





web_app = Flask(__name__)
current_user = User(None, None)




@web_app.route("/", methods=["GET", "POST"])
def home_page():
	print(f'Current User: ',current_user.username)
	results = None
	fruitResults = None
	fruitData = []
	veggieResults = None
	veggieData = []
	if current_user.type == 1:
		# removing item
		if request.method == "POST":
			if 'removeItem' in request.form:
				itemID = request.form['removeItem']
				with sf.create_connection('database.db') as conn:
					sf.execute_statement(conn, f'DELETE FROM inventory WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM cart WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM analytics WHERE itemID={itemID}')
					sf.execute_statement(conn, f'DELETE FROM featured WHERE itemID={itemID}')
		
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
						analyticsID = new_id('analyticsID', 'analytics')
						itemName = name
						quantity = amount
						print("\nadding item to inventory...")
						sf.execute_statement(conn, f'INSERT INTO inventory (itemID, userID, analyticsID, itemName, quantity, price) VALUES ({itemID}, {userID}, {analyticsID}, \'{itemName}\', {quantity}, {price})')




		# getting list
		totalData = []
		with sf.create_connection('database.db') as conn:
			itemData = sf.execute_statement(conn, f'SELECT analyticsID,itemName,price,itemID FROM inventory WHERE userID={current_user.userID}')
			
			for item in itemData:
				itemMetadata = sf.execute_statement(conn, f'SELECT quantitySold FROM analytics WHERE dataID={item[0]}')
				print("\nsold =>", itemMetadata)
				data = {
					'name': item[1],
					'price': item[2],
					'sold': itemMetadata[0][0],
					'itemID': item[3]
				}
				print(data)
				
				totalData.append(data)


		return render_template('seller_home.html', productList=totalData)
	elif current_user.type == 0:
		if request.method == "POST" and 'action' in request.form:
			# add to cart
			itemID = request.form['add']
			with sf.create_connection('database.db') as conn:
				cartID = sf.execute_statement(conn, f'SELECT cart_ptr FROM user WHERE userID={current_user.userID}')[0][0]
				currentQuantity = sf.execute_statement(conn, f'SELECT quantity FROM cart WHERE userID={current_user.userID} AND itemID={itemID}')
				print("c quant =>",currentQuantity)


				if currentQuantity == []:
					print("\nmaking new cart entry")
					newID = new_id('cartID', 'cart')
					sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES ({newID},{current_user.userID},{itemID},1)')
				else:
					print("\nupdating cart entry")
					currentQuantity = currentQuantity[0][0]
					sf.execute_statement(conn, f'UPDATE cart SET quantity={currentQuantity+1} WHERE userID={current_user.userID} AND itemID={itemID}')
					

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


		return render_template('buyer_home.html', fruits=fruitData, veggies=veggieData)
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
				current_user.set_data()

			print("\nusername, ID, type => ", current_user.username, current_user.userID, current_user.type)
			return redirect(url_for('home_page'))

		if 'registerAccount' in request.form:
			return redirect(url_for("register_page"))

	return render_template('login.html')


# done
@web_app.route("/register", methods=["GET", "POST"])
def register_page():
	if request.method == "POST":
		new_email = request.form["email"]
		new_uname = request.form["uname"]
		new_psw = request.form["psw"]
		psw_repeat = request.form["psw-repeat"]
		user_type = request.form["user_type"]

		uname_filter = None
		with sf.create_connection('database.db') as conn:
			uname_filter = sf.execute_statement(conn, f'SELECT * FROM user WHERE username={new_uname}')

		#if uname_filter != []:
		#	return render_template('register.html', taken=True)

		if new_psw != psw_repeat:
			return render_template('register.html', incorrect=True)

		userID = new_id('userID', 'user')
		shipping_ptr = new_id('shippingID','shippingInfo')
		payment_ptr = new_id('paymentID','paymentInfo')
		cart_ptr = new_id('cartID', 'cart')

		with sf.create_connection('database.db') as conn:
			sf.execute_statement(conn, f'INSERT INTO user (userID, username, password_hash, email, fname, lname, type, shipping_ptr, payment_ptr, cart_ptr) VALUES ({userID},\'{new_uname}\',\'{new_psw}\',\'{new_email}\',\'None\', \'None\', {user_type}, {shipping_ptr}, {payment_ptr}, {cart_ptr})')

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
				if request.form['new_uname']: current_user.username = request.form['new_uname']
				if request.form['new_email']: current_user.email = request.form['new_email']
				
				# shipping data
				if request.form['new_street']: current_user.shippingData['street'] = request.form['new_street']
				if request.form['new_state']: current_user.shippingData['state'] = request.form['new_state']
				if request.form['new_city']: current_user.shippingData['city'] = request.form['new_city']
				if request.form['new_zip']: current_user.shippingData['zip'] = request.form['new_zip']

				# payment data
				if request.form['new_card_num']: current_user.paymentData['cardNumber'] = request.form['new_card_num']
				if request.form['new_cardholder_name']: current_user.paymentData['cardholderName'] = request.form['new_cardholder_name']
				if request.form['new_date']: current_user.paymentData['cardDate'] = request.form['new_date']
				

				current_user.update_database()

			if 'deleteAccount' in request.form:
				with sf.create_connection('database.db') as conn:
					# getting pointers
					pointers = sf.execute_statement(conn, f'SELECT shipping_ptr, payment_ptr, cart_ptr FROM user WHERE userID={current_user.userID}')[0]

					print("pointers =>",pointers)
					# deleting payment information
					sf.execute_statement(conn, f'DELETE FROM user WHERE userID={current_user.userID}')
					# deleting shipping information
					sf.execute_statement(conn, f'DELETE FROM shippingInfo WHERE shippingID={pointers[0]}')
					# deleting cart
					sf.execute_statement(conn, f'DELETE FROM paymentInfo WHERE paymentID={pointers[1]}')
					# deleting orders
					sf.execute_statement(conn, f'DELETE FROM cart WHERE cartID={pointers[2]}')


		settings_data = {
				'username': current_user.username,
				'email': current_user.email,
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
				results = search_inventory(request.form['query'])
				print("\nresults =>", results)

				if results != []:
					return render_template('search.html', list=results)


			if 'action' in request.form:
				# add to cart
				itemID = request.form['add']
				with sf.create_connection('database.db') as conn:
					cartID = sf.execute_statement(conn, f'SELECT cart_ptr FROM user WHERE userID={current_user.userID}')[0][0]
					currentQuantity = sf.execute_statement(conn, f'SELECT quantity FROM cart WHERE userID={current_user.userID} AND itemID={itemID}')
					print("c quant =>",currentQuantity)


					if currentQuantity == []:
						print("\nmaking new cart entry")
						newID = new_id('cartID', 'cart')
						sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES ({newID},{current_user.userID},{itemID},1)')
					else:
						print("\nupdating cart entry")
						currentQuantity = currentQuantity[0][0]
						sf.execute_statement(conn, f'UPDATE cart SET quantity={currentQuantity+1} WHERE userID={current_user.userID} AND itemID={itemID}')
					



			return render_template('search.html')
	else:
		return redirect(url_for('login_page'))


# issues buying
@web_app.route("/cart", methods=["GET", "POST"])
def cart_page():
	if current_user.type == 0:
		totalData, total = get_cart()
		paid = False
		# item name, price, quantity
		if request.method == "POST" and 'action' in request.form:
			# add to cart
			if request.form['action'] == '+':
				print('\nAdding to cart...')
				itemID = request.form['itemID']
				currentQuantity = None
				for item in totalData:
					if int(item[3]) == int(itemID):
						item[1] += 1
						currentQuantity = item[1]

				print("current quantity",currentQuantity)

				# removing the capability to have more in cart than inventory
				inventoryQuantity = None
				with sf.create_connection('database.db') as conn:
					inventoryQuantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE itemID={itemID}')[0][0]
				if currentQuantity > inventoryQuantity:
					return redirect(url_for('cart_page'))

				# updating database
				with sf.create_connection('database.db') as conn:
					sf.execute_statement(conn, f'UPDATE cart SET quantity={currentQuantity} WHERE userID={current_user.userID} AND itemID={itemID}')

			else:	# remove from cart
				print('Removing from cart')
				# update database
				itemID = request.form['itemID']
				currentQuantity = None
				for item in totalData:
					if int(item[3]) == int(itemID):
						item[1] -= 1
						currentQuantity = item[1]

				print("current quantity",currentQuantity)
				
				if currentQuantity == 0 or type(currentQuantity) == type(None):
					with sf.create_connection('database.db') as conn:
						sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={current_user.userID} AND itemID={itemID}')
					return redirect(url_for('cart_page'))

				# updating database
				with sf.create_connection('database.db') as conn:
					sf.execute_statement(conn, f'UPDATE cart SET quantity={currentQuantity} WHERE userID={current_user.userID} AND itemID={itemID}')

					
		# paying for cart
		if request.method == "POST" and 'payButton' in request.form:
			print("\nPaying...")


			# moving cart to orders
			with sf.create_connection('database.db') as conn:
				# getting cart information
				itemData = sf.execute_statement(conn, f'SELECT itemID, quantity FROM cart WHERE userID={current_user.userID}')

				print('item data =>',itemData,'\n')

				# getting payment and shipping information
				#paymentData = sf.execute_statement(conn, f'SELECT cardNumber, cardholderName, cardDate FROM paymentInfo WHERE paymentID={current_user.userID}')[0]
				#print('payment data =>',paymentData,'\n')
				#shippingData = sf.execute_statement(conn, f'SELECT street, city, state, country, zip FROM shippingInfo WHERE userID={current_user.userID}')[0]
				#print('shipping data =>',shippingData,'\n')


				orderID = 1
				analyticsID = 1
				try: 
					orderID = new_id('orderID', 'orders')
				except TypeError:
					pass

				try: 
					analyticsID = new_id('dataID', 'analytics')
				except TypeError:
					pass

				# getting data into variable
				cardNumber, cardholderName, cardDate = None, None, None
				street, city, state, country, zip = None,None,None,None,None

				current_date = datetime.date.today()
				orderTime = current_date.strftime("%Y-%m-%d")


				# inserting into table
				for item in itemData:
					itemID = item[0]
					quantity = item[1]
					print("item info =>", itemID, quantity)
					# adding to orders
					print("quantity ==============================")
					cQuant = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE itemID={itemID}')[0][0]
					sf.execute_statement(conn,f'UPDATE inventory SET quantity={cQuant+quantity} WHERE itemID={itemID}')
					#sf.execute_statement(conn, f'INSERT INTO orders (orderID, userID, itemID, quantity, orderTime, cardNumber, cardholderName, cardDate, street, city, state, zip, country) VALUES ({orderID}, {current_user.userID}, {itemID}, {quantity}, 0, {cardNumber}, \'{cardholderName}\', {cardDate}, \'{street}\', \'{city}\', \'{state}\', \'{zip}\', \'{country}\')')
					



				# adding to analytics



				# clearing cart
				sf.execute_statement(conn, f'DELETE FROM cart WHERE userID={current_user.userID}')
				sf.execute_statement(conn, f'INSERT INTO cart (cartID, userID, itemID, quantity) VALUES (1, 1, 1, 1)')

				# refreshing page
				paid=True
				totalData, total = get_cart()
				return render_template('cart.html', list=totalData, cartPrice=total, bool=paid)





		return render_template('cart.html', list=totalData, cartPrice=total, bool=paid)
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




if __name__ == '__main__':
  web_app.run(debug=True)