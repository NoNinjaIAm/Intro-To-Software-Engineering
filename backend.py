from flask import Flask, render_template, request, redirect

# Creating the application object
web_app = Flask(__name__)


@web_app.route("/")
def home_page():
  return render_template('home.html')



@web_app.route("/cart")
def cart_page():
  return render_template('cart.html')


@web_app.route("/order_history.html")
def order_history_page():
  return render_template('order_history.html')


@web_app.route("/settings")
def settings_page():
  return render_template('settings.html')
