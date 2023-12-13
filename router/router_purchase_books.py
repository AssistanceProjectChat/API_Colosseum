from flask import Blueprint, redirect, request
from flask_jwt_extended import jwt_required
import controller.controller_purchase_books as controller_purchase_books
from datetime import datetime

app_purchase_books= Blueprint('route_purchase_books', __name__)

@app_purchase_books.route("/purchases_books", methods = ["GET"])
#@jwt_required()
def get_purchase_books_by_id():
    id_book = request.args.get('id_book', default=None,type=int)
    id_tg = request.args.get('id_tg', default=None,type=int)
    bookmarks = controller_purchase_books.get_purchases_books(id_book, id_tg)
    if bookmarks is not None:
        return bookmarks
    else:
        return redirect("Not Found"), 404

# @app_purchase_books.route("/purchases_books", methods = ["POST"])
# #@jwt_required()
# def insert_purchase_books():
#     try:
#         purchases_books = request.get_json()
#         id_book = purchases_books["id_book"]
#         id_tg = purchases_books["id_tg"]
#         datatime_purchase = datetime.today()
#         result = controller_purchase_books.insert_purchases_books(id_book, id_tg, str(datatime_purchase))
#         if result == True:
#             return "Покупка прошла успешно."
#         else:
#             return "Ошибка при покупке.(2)"
#     except Exception:
#         return "Ошибка при покупке.(3)"