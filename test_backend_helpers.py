# this is probably the general form of this pytest file but I will need the frontend to be up to complete it

import backend
import data_generation as dg
import sql_functions as sf

# search_inventory with existing item
def test_search_inventory_good():
    with sf.create_connection('database.db') as conn:
        itemName = sf.execute_statement(conn, "SELECT itemName from inventory")[0][0]
            # generate an item if none exist
        if itemName == None:
            dg.generate_item()
            itemName = sf.execute_statement(conn, "SELECT itemID from inventory")[0][0]
    result = backend.search_inventory(itemName)
    assert len(result) > 0

# search_inventory with non-existing item
def test_search_iventory_bad():
    itemName = "TEST_BAD_DATA"
    result = backend.search_inventory(itemName)
    assert len(result) == 0

# get cart with empty cart
def test_get_cart_empty():
    backend.current_user.userID = 9999
    result, total = backend.get_cart()
    assert result == [] and total == None

# get cart with non-empty cart
def test_get_cart_not_empty():
    with sf.create_connection('database.db') as conn:
        backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
            # generate a user if none exist
        if backend.current_user.userID == None:
            dg.generate_user()
            backend.current_user.userID = sf.execute_statement(conn, "SELECT userID from user WHERE type = 0")[0][0]
        itemID = sf.execute_statement(conn, f"SELECT itemID from cart WHERE userID = {backend.current_user.userID}")[0][0]
        if itemID == None:
            dg.generate_cart()
    result, total = backend.get_cart()
    assert len(result) > 0 and total != None

# not testing new_id