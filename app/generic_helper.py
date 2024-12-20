from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Depends
import re
from .database import get_db,get_order_status, get_next_order_id, get_order_price_by_quantity, insert_order, insert_order_status, get_all_foodItems,get_orders_by_id
from pprint import pprint



# automatedpurchasenavigator@automatedpurchasenavigato-bcbj.iam.gserviceaccount.com

def order_tracking(in_process_order:dict,parameters:dict, user_id:int, db:Session=Depends(get_db)):
    try:
        order_id = parameters['number']

        order_status = get_order_status(order_id, db)
        orders = get_orders_by_id(order_id, user_id, db)
        order_str = ",".join([f"{item[1]} {item[0]}" for item in orders])

    
        if order_status is not None and len(orders)>0:
            status = order_status[1]
            total_price = order_status[2]
            if status == 'completed':
                fulfillment_text = f"Your order is {status}.your order was {order_str} and you have paid {total_price}."
            else:
                fulfillment_text = f"Your order is {status}.you have ordered {order_str} and total price of your order is {total_price}."
        else:
            fulfillment_text = f"No order is found for id {int(order_id)}"

        return fulfillment_text
        # return JSONResponse(content={
        #     "fulfillmentText": fulfillment_text
        # })
    except Exception as e:
        pprint({"order tracking error": e})



def complete_order(in_process_order:dict,parameters:dict, user_id:int, db:Session=Depends(get_db)):

    try:
        if user_id not in in_process_order:
            fulfillment_text = f"I'm having a trouble finding your order. Sorry! Can you place a new order please?"
            return fulfillment_text
    
        current_order = in_process_order[user_id]

        if len(current_order.keys()) == 0:
            fulfillment_text = f"I'm having a trouble finding your order. Sorry! Can you place a new order please?"
            return fulfillment_text
        
        new_order_id = get_next_order_id(db)
        
        orders = get_order_price_by_quantity(current_order, db)
        
        payable_price = 0

        for order in orders:
            record = {
                "OrderID": new_order_id,
                "ItemID": order['id'],
                "FoodName": order['food_name'],
                "Quantity": order['quantity'],
                "TotalPrice": order['price'],
                "user_id": user_id
            }
            payable_price += record['TotalPrice']
            is_error = insert_order(record, db)
            if is_error:
                fulfillment_text = f"Sorry! something went wrong. please try again!"
                return fulfillment_text
            
        
        order_status = {
            "OrderID": new_order_id,
            "OrderStatus": "in process",
            "PayablePrice": payable_price
        }

        is_error = insert_order_status(record=order_status, db=db)
        if is_error:
            fulfillment_text = f"Sorry! something went wrong. please try again!"
            return fulfillment_text
            

        del in_process_order[user_id]

        fulfillment_text = f"Your order is accepted. here is you total payable price {payable_price} and order id {new_order_id}. you can track your order now!"
        return fulfillment_text
        # return JSONResponse(content={
        #     "fulfillmentText": fulfillment_text,
        #     "outputContexts": [],
        # })
    except Exception as e:
        pprint({"complete order error ": e})


def remove_ongoing_order(in_process_order:dict,parameters:dict, user_id:int, db:Session=Depends(get_db)):
    try:
        if user_id not in in_process_order:
            fulfillment_text = f"I'm having a trouble finding your order. Sorry! Can you place a new order please?"
            return fulfillment_text
            
    
        fooditem = parameters['food-item']
        current_order = in_process_order[user_id]

        itemNotFound = []
        removedItem = []
        
        for item in fooditem:
            if item not in current_order:
                itemNotFound.append(item)
            else:
                removedItem.append(item)
                del current_order[item]
                in_process_order[user_id] = current_order
        
        if len(removedItem) > 0:
            fulfillment_text = f'Removed {",".join(removedItem)} from your order!'
        
        if len(itemNotFound) > 0:
            fulfillment_text = f' Your current order does not have {",".join(itemNotFound)}'
        
        if len(current_order.keys()) == 0:
            fulfillment_text += " Your order is empty!"
        else:
            order_str = ", ".join([ f"{int(value)} {key}" for key, value in current_order.items()])
            fulfillment_text += f" Here is what is left in your order: {order_str} \nDo you need anything else?"

        return fulfillment_text
        # return JSONResponse(content={
        #     "fulfillmentText": fulfillment_text
        # })
    
    except Exception as e:
        pprint({"remove order error": e})



def add_ongoing_order(in_process_order:dict,parameters:dict, user_id:int, db:Session=Depends(get_db) ):
    
    try:
        foodItem = parameters['food-item']
        number = parameters['number']

        newdict = dict(zip(foodItem, number))

        if user_id in in_process_order:
            item = in_process_order[user_id]
            item.update(newdict)
            in_process_order[user_id] = item
        else:
            in_process_order[user_id]= newdict

        order_string = ", ".join([f"{int(value)} {key}" for key, value in in_process_order[user_id].items()])

        fulfillment_text = f"So far you have: {order_string}. Do you need anything else?"


        return fulfillment_text
        # return JSONResponse(content={
        #     "fulfillmentText":fulfillment_text
        # })

    except Exception as e:
        pprint({"add order error": e})



def get_avaiable_menu(in_process_order:dict,parameters:dict, user_id:int, db:Session=Depends(get_db)):
    
    try:

        fooditems = get_all_foodItems(db=db)

        menu_response = "Here is our today's available menu:\n"

        for menu in fooditems:
            menu_response += f"       {menu[0]} : {menu[1]} taka, \n"
        


        menu_response = menu_response.rstrip(', \n')

        menu_response += " \n . Are you ready to place your order? If so, please feel free to choose items from our menu and specify the exact quantity. For example, you might say, 'two samosa and 2 piyaji.' I’m here to help whenever you’re ready!"

        return menu_response
        # return JSONResponse(content={
        #     "fulfillmentText": menu_response
        # })

    except Exception as e:
        pprint({"avaiable menu error": e})