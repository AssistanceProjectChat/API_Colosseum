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