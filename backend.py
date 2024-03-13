from flask import Flask, render_template, request, redirect, url_for
import time

web_app = Flask(__name__)

nav_query = None
user = {
  'username': 'sbb328',
  'password': 'xxx',
  'email': 'example@gmail.com',
  'shipping_information': {
    'address': '123 EX Rd',
    'state': 'MS',
    'city': 'Columbia',
    'zip': '39429'
  }
}
cart = [
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

featured_fruits = [
    {
    'name': 'Laptop',
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
  if request.method == "GET":
    return render_template('home.html', fruits=featured_fruits, veggies=featured_veggies)

  if request.method == "POST": 
    if request.form['item_data']:
      item_data = request.form['item_data']
      

      #splitting up csv data
      item_data = item_data.split(",")

      cart.append({
        'name': item_data[0],
        'quantity': int(item_data[1]),
        'price': float(item_data[2]),
        'description': item_data[3]
        })


      return render_template('home.html', fruits=featured_fruits, veggies=featured_veggies)


@web_app.route("/cart", methods=["GET", "POST"])
def cart_page():
  if request.method == "POST":
    action = request.form['action']
    itemID = request.form['itemID']
    if action == '+':
      for item in cart:
        if item['name'] == itemID:
          item['quantity'] += 1
    if action == '-':
      for item in cart:
        if item['name'] == itemID:
          if item['quantity'] > 1:
            item['quantity'] -= 1
          else:
            cart.remove(item)

      

  cart_sum = 0
  for item in cart:
    cart_sum += float(item['quantity']) * item['price']

  cart_sum = "{:.2f}".format(cart_sum)
  return render_template('cart.html', list=cart, sum=cart_sum)

@web_app.route("/login", methods=['GET','POST'])
def login_page():
  msg = ''
  if request.method == 'POST':
    valid = False
    username = request.form['uname']
    password = request.form['psw']
    remember_me = request.form['remember']

    # process data
    # TODO: valid inputs based on database


    # insecure; change to a default and a valid==True
    # TODO: redirect to home and be a user
    if valid == False:
      msg = "Invalid username or password."
      return render_template('login.html', failure_message=msg)
    else: 
      # Redirect to the '/home' route
      return redirect(url_for('home_page'))

  if request.method == 'GET':
    return render_template('login.html')


# cart is local and not global for some reason
@web_app.route("/payment-info", methods=["GET","POST"])
def payment_info_page():
  if request.method == "POST":
    # set data
    '''for item in cart:
                  item['time'] = time.time()
                  item['paymentInfo'] = {
                    'name': request.form['cardholder-name'],
                    'number': request.form['card-number'],
                    'cvv': request.form['cvv-code'],
                    'exp': request.form['exp-date']
                  }'''

    # reset cart
    order_history.append(cart)
    cart = []

    # update database
    print(f"cart => {cart}")
    print(f"order history => {order_history}")
    redirect(url_for('/order-history'))
  
  if request.method == "GET":
    cart_sum = 0
    for item in order_history[-1]:
      cart_sum += float(item['quantity']) * item['price']

    total = "{:.2f}".format(cart_sum)
    return render_template('paymentInfo.html', total=total)

@web_app.route("/register-account")
def register_account_page():
  return render_template('registerAccount.html')




@web_app.route("/search", methods=["GET","POST"])
def search_page():
  if request.method == "POST":
    if 'query' in request.form:
      query = request.form['query']
      

      products_to_display = []

      for item in inventory:
        if query in item['name']:
          products_to_display.append(item)

      return render_template('search.html', list=products_to_display)
  


  if request.method == "POST":
    item_data = request.form['item_data']
      

    #splitting up csv data
    item_data = item_data.split(",")

    cart.append({
      'name': item_data[0],
      'quantity': int(item_data[1]),
      'price': float(item_data[2]),
      'description': item_data[3]
      })


    return render_template('search.html')
  if request.method == "GET":
    return render_template('search.html')


@web_app.route("/settings", methods=["GET", "POST"])
def settings_page():
  if request.method == 'GET':
    return render_template('settings.html', edit=False,
      username=user['username'],
      email=user['email'], 
      address=user['shipping_information']['address'],
      state=user['shipping_information']['state'],
      city=user['shipping_information']['city'],
      zip=user['shipping_information']['zip'])

  elif request.method == 'POST':
    if 'edit' in request.form:
      return render_template('settings.html', edit=True,
        username=user['username'],
        email=user['email'], 
        address=user['shipping_information']['address'],
        state=user['shipping_information']['state'],
        city=user['shipping_information']['city'],
        zip=user['shipping_information']['zip'])

    if 'new_info' in request.form:
      if request.form['new_username']: user['username'] = request.form['new_username']
      if request.form['new_email']: user['email'] = request.form['new_email']
      if request.form['new_address']: user['shipping_information']['address'] = request.form['new_address']
      if request.form['new_state']: user['shipping_information']['state'] = request.form['new_state']
      if request.form['new_city']: user['shipping_information']['city'] = request.form['new_city']
      if request.form['new_zip']: user['shipping_information']['zip'] = request.form['new_zip']

      return render_template('settings.html', edit=False,
          username=user['username'],
          email=user['email'], 
          address=user['shipping_information']['address'],
          state=user['shipping_information']['state'],
          city=user['shipping_information']['city'],
          zip=user['shipping_information']['zip'])

    #if logout

@web_app.route("/order-history", methods=["GET","POST"])
def order_history_page():
  cart_sum = 0
  for order in order_history:
    for item in order:
      cart_sum += float(item['quantity']) * item['price']
  return render_template('orderHistory.html', order_history=order_history)



if __name__ == '__main__':
  web_app.run(debug=True)