from flask import Flask, render_template, request, redirect, url_for
import time
import datetime
import sql_functions as sf
import random
import string
import hashlib

# important global variable
web_app = Flask(__name__)

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username
username='\'jane_smith\''

current_user = User(None, '\'None\'')


def check_used_ids(connection):
  used_ids = sf.execute_statement(connection, f'SELECT item_id FROM inventory')

  for id in used_ids:
    id = id[0]

  x = random.randrange(1, 100000000)
  while x in used_ids:
    print("ID in use...")
    x = random.randrange(1, 100000000)

  return x

def get_current_id(connection):
  return sf.execute_statement(connection, f'SELECT user_id FROM user WHERE username={current_user.username}')[0][0]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_data():
  with sf.create_connection('database.db') as conn:
    user_data = sf.execute_statement(conn, f'SELECT username, email FROM user WHERE username={current_user.username}')[0]
    try:
      shipping_data = sf.execute_statement(conn, f'SELECT street_address, city, state, postal_code FROM shipping_address WHERE user_id={get_current_id(conn)}')[0]
      formatted_data = {
        'username': user_data[0],
        'email': user_data[1],
        'address': shipping_data[0],
        'city': shipping_data[1],
        'state': shipping_data[2],
        'zip': shipping_data[3]
      }


      return formatted_data

    except IndexError:
      return {
        'username': '\'None\'',
        'email': '\'None\'',
        'address': '\'None\'',
        'city': '\'None\'',
        'state': '\'None\'',
        'zip': '\'None\''
      }



def update_user_data(data):
  with sf.create_connection('database.db') as conn:
    email = data['email']
    address = data['address']
    city = data['city']
    state = data['state']
    code = data['zip']
    print('\nUpdating user...')
    sf.execute_statement(conn, f'UPDATE user SET username=\'{current_user.username}\',email=\'{email}\' WHERE user_id={get_current_id(conn)}')

    print('\nUpdating shipping...')
    sf.execute_statement(conn, f'UPDATE shipping_address SET street_address=\'{address}\',city=\'{city}\' WHERE user_id={get_current_id(conn)}')
    sf.execute_statement(conn, f'UPDATE shipping_address SET state=\'{state}\',postal_code=\'{code}\' WHERE user_id={get_current_id(conn)}')

def get_inventory():
  with sf.create_connection('database.db') as conn:
    return sf.execute_statement(conn, f'SELECT * FROM inventory')

def add_to_inventory(item_data):
  with sf.create_connection('database.db') as conn:


    search_value = bool(sf.execute_statement(conn, f'SELECT * FROM inventory WHERE item_name=\'{item_data[0]}\''))
    print(f'search_value: {search_value}')

    if search_value:
      item_id = sf.execute_statement(conn, f'SELECT item_id FROM inventory WHERE item_name=\'{item_data[0]}\'')[0][0]
      quantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE item_id={item_id}')[0][0]
      new_quantity = quantity + 1


      sf.execute_statement(conn, f'UPDATE inventory SET quantity={new_quantity} WHERE item_id={item_id}')




    else:
      print('Not in cart')
      used_ids = sf.execute_statement(conn, f'SELECT item_id FROM inventory')
      print('\n\n')


      x = check_used_ids(conn)

      sf.execute_statement(conn, f'INSERT INTO inventory (item_id, item_name, quantity, price) VALUES ({x}, \'{item_data[0]}\', {item_data[1]}, {item_data[2]})')

    

    print(f'inventory: {get_inventory()}')

def get_cart():
  with sf.create_connection('database.db') as conn:
    user_id = sf.execute_statement(conn, f'SELECT user_id FROM user WHERE username={current_user.username}')[0][0]
    item_id = sf.execute_statement(conn, f'SELECT item_id FROM cart WHERE user_id={user_id}')[0][0]
    cart = sf.execute_statement(conn, f'SELECT * FROM inventory WHERE item_id={item_id}')
    print(f'\n{current_user.username[1:-1]}\'s cart: {cart}\n')
    

    return cart

def update_cart(item_id, new_quantity):
  with sf.create_connection('database.db') as conn:
    sf.execute_statement(conn, f'UPDATE inventory SET quantity={new_quantity} WHERE item_id={item_id}')

def delete_from_cart(item_id):
  with sf.create_connection('database.db') as conn:
    sf.execute_statement(conn, f'DELETE FROM inventory WHERE item_id={item_id}')

def adding_to_cart(item_data):
  with sf.create_connection('database.db') as conn:
    cart = get_cart()

    '''# clearing orders for testing
                    sf.execute_statement(conn, f'DELETE FROM orders')
                    orders = sf.execute_statement(conn, f'SELECT * FROM orders')
                    print(f'orders: {orders}\n')'''
    
    user_id = sf.execute_statement(conn, f'SELECT user_id FROM user WHERE username={current_user.username}')[0][0]
    print(f'user id: {user_id}')


    # search value issue
    search_value = sf.execute_statement(conn, f'SELECT * FROM cart WHERE user_id=\'{user_id}\'') != []
    print(f'search_value: {search_value}')
    item_id = sf.execute_statement(conn, f'SELECT item_id FROM inventory WHERE item_name=\'{item_data[0]}\'')[0][0]

    if search_value:
      # generating new id
      used_ids = sf.execute_statement(conn, f'SELECT item_id FROM inventory')
      print('\n\n')
      for id in used_ids:
        id = id[0]

      x = random.randrange(1, 100000000)
      y = random.randrange(1, 100000000)
      while x in used_ids:
        print("ID in use...")
        x = random.randrange(1, 100000000)

      while y in used_ids:
        print("ID in use...")
        y = random.randrange(1, 100000000)
      print(x,y,'\n')


      sf.execute_statement(conn, f'INSERT INTO cart (cart_id, user_id, order_id, item_id) VALUES ({x}, {user_id}, {y}, {item_id})')
      sf.execute_statement(conn, f'INSERT INTO orders (order_id, user_id, status, created_at, delivered_at) VALUES ({y}, {user_id}, \'current\', {time.time()}, NULL)')
      sf.execute_statement(conn, f'SELECT * FROM cart')
      sf.execute_statement(conn, f'SELECT * FROM orders')


    else: 
      for item in cart:
        print (item)

def register_account(password, email):
  with sf.create_connection('database.db') as conn:
    hashed_password = hash_password(password)
    print(hashed_password)


    user_id = check_used_ids(conn)

    u = ""

    for i in range(0,5):
      u += random.choice(string.ascii_letters)


    # store data
    sf.execute_statement(conn, f'INSERT INTO user (user_id, username, password_hash, email, first_name, last_name) VALUES ({user_id}, \'{u}\', \'{hashed_password}\', \'{email}\', \'None\', \'None\')')

    current_user.username = f'\'{u}\''
    current_user.user_id = user_id

    return False

def change_user(new_username):
  with sf.create_connection('database.db') as conn:
    users_list = sf.execute_statement(conn, f'SELECT username FROM user WHERE username={new_username}')
    if (users_list == []):
      return False
    print(f'Username is now {new_username}')
    return new_username









featured_fruits = [
    {
    'name': 'Desktop',
    'quantity': 1,
    'price': 999.00,
    'description': 'dfsfdsdfsdfsdf'
    },
    {
    'name': 'IPad',
    'quantity': 3,
    'price': 100000.00,
    'description': 'expensive'
    }
]
featured_veggies = [
    {
    'name': 'PS4',
    'quantity': 1,
    'price': 999.00,
    'description': 'dfsfdsdfsdfsdf'
    },
    {
    'name': 'XBox',
    'quantity': 3,
    'price': 100000.00,
    'description': 'expensive'
    }
]



inventory = [
  {
    'name': 'phone',
    'quantity': 47,
    'price': 10.00,
    'description': 'kinda sucks'
  },
  
  {
    'name': 'PS4',
    'quantity': 100,
    'price': 999.00,
    'description': 'dfsfdsdfsdfsdf'
  },

  {
    'name': 'XBox',
    'quantity': 345,
    'price': 100000.00,
    'description': 'expensive'
  },

  {
    'name': 'Laptop',
    'quantity': 1444,
    'price': 999.00,
    'description': 'dfsfdsdfsdfsdf'
  },
  
  {
    'name': 'IPad',
    'quantity': 39,
    'price': 100000.00,
    'description': 'expensive'
  },
  {
    'name': 'Smartphone',
    'quantity': 39,
    'price': 100000.00,
    'description': 'expensive'
  }
]
order_history = [
  [
    {
      'orderID': 10332,
      'name': 'phone',
      'quantity': 47,
      'price': 10.00,
      'description': 'kinda sucks',
      'time': time.time(),
      'paymentInfo': {
        'name': 'Shawn Butler',
        'number': '1111111111',
        'cvv': '123',
        'exp': 'fffff'
      }
    },
    {
      'orderID': 10332,
      'name': 'ipod',
      'quantity': 7,
      'price': 15.00,
      'description': 'sucks',
      'time': time.time(),
      'paymentInfo': {
        'name': 'Shawn Butler',
        'number': '1111111111',
        'cvv': '123',
        'exp': 'fffff'
      }
    }
  ]
]




@web_app.route("/", methods=["GET", "POST"])
def home_page():
  with sf.create_connection('database.db' ) as conn:
    sf.execute_statement(conn, f'SELECT * FROM user')
  if request.method == "GET":
    return render_template('home.html', fruits=featured_fruits, veggies=featured_veggies)

  if request.method == "POST": 
    if request.form['item_data']:
      item_data = request.form['item_data']
      

      #splitting up csv data
      item_data = item_data.split(",")
      adding_to_cart(item_data)


      return render_template('home.html', fruits=featured_fruits, veggies=featured_veggies)


# done
@web_app.route("/cart", methods=["GET", "POST"])
def cart_page():
  cart = get_inventory()
  if request.method == "POST":
    action = request.form['action']
    itemID = request.form['itemID']
    if action == '+':
      for item in cart:
        if int(item[0]) == int(itemID):
          new_quantity = item[2] + 1
          update_cart(item[0], new_quantity)

    if action == '-':
      print('-')
      for item in cart:
        if int(item[0]) == int(itemID):
          if item[2] >= 1:
            new_quantity = item[2] - 1
            update_cart(item[0], new_quantity)
          else:
            delete_from_cart(item[0])

      

  cart_sum = 0
  for item in cart:
    cart_sum += float(item[2]) * item[3]

  cart_sum = "{:.2f}".format(cart_sum)
  return render_template('cart.html', list=cart, sum=cart_sum)



@web_app.route("/login", methods=['GET','POST'])
def login_page():
  msg = ''
  if request.method == 'POST':
    valid = False
    given_username = request.form['uname']
    given_password = request.form['psw']
    remember_me = request.form['remember']

    # processing
    print(f'Given: {given_username}\n',f'Actual: {current_user.username}')



    if valid == False:
      msg = "Invalid username or password."
      return render_template('login.html', failure_message=msg)
    else: 
      # Redirect to the '/home' route
      return redirect(url_for('home_page'))

  if request.method == 'GET':
    return render_template('login.html')



# done
@web_app.route("/payment-info", methods=["GET","POST"])
def payment_info_page():
  if request.method == "GET":
    cart_sum = 0
    for item in order_history[-1]:
      cart_sum += float(item['quantity']) * item['price']

    total = "{:.2f}".format(cart_sum)
    return render_template('paymentInfo.html', total=total)

  if request.method == "POST":
    return render_template('paymentInfo.html', paid=True)


# done
@web_app.route("/register-account", methods=["GET","POST"])
def register_account_page():
  if request.method == "GET":
    return render_template('registerAccount.html')

  if request.method == "POST":
    new_email = request.form["email"]
    new_psw = request.form["psw"]
    psw_repeat = request.form["psw-repeat"]

    if new_psw != psw_repeat:
      return render_template('registerAccount.html', incorrect=True)


    register_account(new_psw, new_email)
    return render_template('registerAccount.html', incorrect=False)


#done
@web_app.route("/search", methods=["GET","POST"])
def search_page():
  if request.method == "POST":
    products_to_display = []

    # searching items
    if 'query' in request.form:
      query = request.form['query']

      inventory = get_inventory()

      for item in inventory:
        if query in item[1]:
          products_to_display.append(item)

      return render_template('search.html', list=products_to_display)
    


    # adding to cart
    if 'add' in request.form:
      item_id = request.form['add']
      quantity = None
      with sf.create_connection('database.db') as conn:
        quantity = sf.execute_statement(conn, f'SELECT quantity FROM inventory WHERE item_id={item_id}')
        print(f'\nq: {quantity[0][0]}')
      update_cart(item_id, quantity[0][0]+1)

      return render_template('search.html', list=products_to_display)
  

  if request.method == "GET":
    return render_template('search.html')

# done
@web_app.route("/settings", methods=["GET", "POST"])
def settings_page():
  if request.method == 'GET':
    user = get_user_data()
    return render_template('settings.html', edit=False,
                  username=user['username'],
                  email=user['email'], 
                  address=user['address'],
                  state=user['state'],
                  city=user['city'],
                  zip=user['zip'])

  elif request.method == 'POST':
    if 'edit' in request.form:
      return render_template('settings.html', edit=True)

    if 'new_info' in request.form:
      user = get_user_data()
      if request.form['new_email']: user['email'] = request.form['new_email']
      if request.form['new_address']: user['address'] = request.form['new_address']
      if request.form['new_state']: user['state'] = request.form['new_state']
      if request.form['new_city']: user['city'] = request.form['new_city']
      if request.form['new_zip']: user['zip'] = request.form['new_zip']


      update_user_data(user)


      return render_template('settings.html', edit=False,
                  username=user['username'],
                  email=user['email'], 
                  address=user['address'],
                  state=user['state'],
                  city=user['city'],
                  zip=user['zip'])

    #if logout

# done? 
# item data not showing but that probably is a database problem
@web_app.route("/order-history", methods=["GET","POST"])
def order_history_page():
  cart_sum = 0

  order_history = None

  with sf.create_connection('database.db') as conn:
    order_history = sf.execute_statement(conn, f'SELECT * FROM orders WHERE user_id={get_current_id(conn)}')

  formatted_history = []

  for item in order_history:
    order_id = item[0]
    print(order_id)

    item_id = sf.execute_statement(conn, f'SELECT item_id FROM cart WHERE order_id={order_id}')
    print(f'\nitem id: {item_id}')
    item_data = sf.execute_statement(conn, f'SELECT item_name, quantity, price FROM inventory WHERE item_id={item_id}')
    print(f'\nitem data: {item_data}')

    data = {
      'orderID': order_id,
      'item_name': item_data[0],
      'quantity': item_data[1],
      'price': item_data[2]
    }
    formatted_history.append(data)

  return render_template('orderHistory.html', order_history=formatted_history)








if __name__ == '__main__':

  web_app.run(debug=True)