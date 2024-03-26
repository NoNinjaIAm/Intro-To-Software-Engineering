import pytest
from sql_functions import *
from backend import *


#   -- -- --TESTING FOR create_connection FUNCTION-- -- --  #

# Error testing with integers (wrong data type) (Should Pass)
def test_create_connection_one():
    # Try function for Type Error
    try:
        create_connection(1)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Error testing with too many arguments (Should Pass)
def test_create_connection_two():
    try:
        create_connection("This is nothing", "IncorrectStrings", "BRRRRRRRRR", "sjdjsdj")
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Error testing with string (Should pass)
def test_create_connection_three(capsys):
    create_connection("SQLFunctionsBlankFileTest")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout.strip() == "Connected to SQLite database: SQLFunctionsBlankFileTest"

# Error testing with no arguments (Should Pass)
def test_create_connection_four():
    try:
        create_connection()
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Error testing with empty string (Should fail)
def test_create_connection_five(capsys):
    create_connection("")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout.strip() == "Couldn't Connect to Database: No name provided..."





#   -- -- --TESTING FOR execute_statement FUNCTION-- -- --  #

# Error testing with integers (wrong data type) (Should Pass)
def test_execute_statement_one():
    try:
        execute_statement(1, 2)
        assert False
    except AttributeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Error testing with incorect strings (wrong data type) (should pass)
def test_execute_statement_two():
    try:
        execute_statement("WrongConnection", "RandomStatement")
        assert False
    except AttributeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Testing with no parameters (should pass)
def test_execute_statement_three():
    try:
        execute_statement()
        assert False
    except TypeError:
        assert True
    else:
        assert False

# Testing with cursor type but an invalid statement (should pass)
def test_execute_statement_four(capsys):
    execute_statement(sqlite3.connect("SQLFunctionsBlankFileTest"), "NothingStatement", False)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout.strip() == 'Error executing statement: near "NothingStatement": syntax error'
    
# Testing empty cursor connection and empty statement (should fail) (Error Handling needed for empty statement)
def test_execute_statement_five(capsys):
    execute_statement(sqlite3.connect(""), "", True)
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout.strip() == 'Error executing... No Statement Detected'





#   -- -- --TESTING FOR execute_sql_file FUNCTION-- -- --   #

# Error testing with integers (wrong data type) (Should Pass)
def test_execute_sql_file_one():
    try:
        execute_sql_file(1, 2)
        assert False
    except AttributeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type
    
# Error testing with incoreect strings (wrong data type) (Should Pass)
def test_execute_sql_file_two():
    try:
        execute_sql_file("InvalidConnection", "WrongFilePath")
        assert False
    except AttributeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

# Error testing with no parameters (should pass)
def test_execute_sql_file_three():
    try:
        execute_sql_file()
        assert False
    except TypeError:
        assert True
    else:
        assert False

# Error testing with cursor type but nonsense file path (should pass)
def test_execute_sql_file_four():
    try:
        execute_sql_file(sqlite3.connect("SQLFunctionsBlankFileTest"), "InvalidFilePath/Nowhere/DollarGeneral")
        assert False
    except FileNotFoundError:
        assert True
    else:
        assert False

# Error testing with cursor type but with empty file path (should fail)
def test_execute_sql_file_five():
    execute_sql_file(sqlite3.connect("SQLFunctionsBlankFileTest"), "")
    captured_stdout, captured_stderr = capsys.readouterr()
    assert captured_stdout.strip() == "Error: No File Name Detected"





#   -- -- --TESTING FOR add_to_inventory FUNCTION-- -- --   #
randomDictionary = {"name": 'Nicholas', "desc": 'Is', "ID": 'Epic'}

#Error testing with wrong data type integer (should pass)
def test_add_to_inventory_one():
    try:
        add_to_inventory(1, 2)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

#Error testing null parameters (should pass)
def test_add_to_inventory_two():
    try:
        add_to_inventory(None, None)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

#Error testing with random dictionary (should pass)
def test_add_to_inventory_three():
    try:
        add_to_inventory(randomDictionary, "hurhur")
        assert False
    except KeyError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type





#   -- -- --TESTING FOR adding_to_cart FUNCTION-- -- --   #

#Error testing with wrong data type integer (should pass)
def test_adding_to_cart_one():
    try:
        adding_to_cart(1, 2)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

#Error testing null parameters (should pass)
def test_adding_to_cart_two():
    try:
        adding_to_cart(None, None)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type

#Error testing with random dictionary (should pass)
def test_adding_to_cart_three():
    try:
        adding_to_cart(randomDictionary, randomDictionary)
        assert False
    except TypeError:
        assert True
    else: 
        return False #Return false if Error happens but its wrong error type