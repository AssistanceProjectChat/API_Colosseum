from flask import Blueprint, redirect, request
from flask_jwt_extended import jwt_required
import controller.controller_cart as controller_cart


app_cart= Blueprint('route_cart', __name__)

@app_cart.route("/cart", methods = ["GET"])
#@jwt_required()
def get_cart_by_id():
    id_tg = request.args.get('id_tg', default=None,type=str)
    user_cart = controller_cart.get_cart(id_tg)
    if user_cart is not None:
        return user_cart
    else:
        return redirect("Not Found"), 404
    
@app_cart.route("/cart", methods = ["POST"])
#@jwt_required()
def insert_cart():
    try:
        add_cart = request.get_json()
        id_tg = add_cart["id_tg"]
        id_book = add_cart["id_book"]
        result = controller_cart.insert_book_cart(id_tg, id_book)
        if result == True:
            return "Успешное добавление книги в корзину."
        else:
            return "Ошибка при добавление книги в корзину.(2)"
    except Exception:
        return f"Ошибка при добавление книги в корзину.(3)"
    
@app_cart.route("/cart", methods = ["PATCH"])
#@jwt_required()
def update_cart_trigger_buy():
    try:
        update_cart = request.get_json()
        id_tg = update_cart["id_tg"]
        result = controller_cart.update_cart_trigger(id_tg)
        print(result)
        if result == "Purchase_ok":
            return "Покупка успешна."
        else:
            return "Ошибка при покупке."
    except Exception:
        return "Ошибка при покупке."