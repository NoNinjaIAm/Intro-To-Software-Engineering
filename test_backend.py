# this is probably the general form of this pytest file but I will need the frontend to be up to complete it

import pytest
from flask import Flask
import backend

@pytest.fixture
def client():
    with backend.test_client() as client:
        yield client

def test_login_page(client):
    # response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    # assert b'STRING_FROM_LOGINPAGE' in response.data

def test_home_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/')
    assert response.status_code == 200
    # assert b'STRING_FROM_HOMEPAGE' in response.data

def test_cart_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/cart')
    assert response.status_code == 200
    # assert b'STRING_FROM_CARTPAGE' in response.data

def test_payment_info_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/payment-info')
    assert response.status_code == 200
    # assert b'STRING_FROM_PAYMENTPAGE' in response.data

def test_register_account_page(client):
    # response = client.post('/register-account', data={DATAAAAA})
    assert response.status_code == 200
    # assert b'STRING_FROM_REGISTERPAGE' in response.data

def test_search_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/search')
    assert response.status_code == 200
    # assert b'STRING_FROM_SEARCHPAGE' in response.data

def test_settings_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/settings')
    assert response.status_code == 200
    # assert b'STRING_FROM_SETTINGSPAGE' in response.data

def test_order_history_page(client):
    # client.post('/login', data={'username': 'testuser', 'password': 'testpassword'})
    response = client.get('/order-history')
    assert response.status_code == 200
    # assert b'STRING_FROM_ORDERSPAGE' in response.data
