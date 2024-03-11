from flask import Flask, render_template, request, redirect

web_app = Flask(__name__)



@web_app.route("/")
def home_page():
  return render_template('home.html')

@web_app.route("/cart")
def cart_page():
  return render_template('cart.html')

@web_app.route("/login")
def login_page():
  return render_template('login.html')

@web_app.route("/payment-info")
def payment_info_page():
  return render_template('paymentInfo.html')

@web_app.route("/register-account")
def register_account_page():
  return render_template('registerAccount.html')

@web_app.route("/search")
def search_page():
  return render_template('search.html')

@web_app.route("/settings")
def settings_page():
  return render_template('settings.html')

@web_app.route("/order-history")
def order_history_page():
  return render_template('orderHistory.html')


if __name__ == '__main__':
  web_app.run(debug=True)