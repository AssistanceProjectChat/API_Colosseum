from flask import Blueprint, redirect, request
from flask_jwt_extended import jwt_required
import controller.controller_bookmarks as controller_bookmarks

app_bookmarks= Blueprint('route_bookmarks', __name__)

@app_bookmarks.route("/bookmarks", methods = ["GET"])
#@jwt_required()
def get_bookmarks_by_id():
    id_book = request.args.get('id_book', default=None,type=int)
    id_tg = request.args.get('id_tg', default=None,type=int)
    bookmarks = controller_bookmarks.get_bookmarks(id_book, id_tg)
    if bookmarks is not None:
        return bookmarks
    else:
        return redirect("Not Found"), 404

@app_bookmarks.route("/bookmarks", methods = ["POST"])
#@jwt_required()
def insert_bookmarks():
    try:
        bookmarks = request.get_json()
        id_book = bookmarks["id_book"]
        id_tg = bookmarks["id_tg"]
        position = bookmarks["position"]
        print(bookmarks)
        result = controller_bookmarks.insert_bookmarks(id_book, id_tg, position)
        if result == True:
            return "Закладка успешно добавлена."
        else:
            return "Ошибка при добавлении закладки.(3)"
    except Exception:
        return "Ошибка при добавлении закладки.(4)"

@app_bookmarks.route("/bookmarks", methods = ["PUT"])
#@jwt_required()
def update_bookmarks():
    try:
        bookmarks = request.get_json()
        id_book = bookmarks["id_book"]
        id_tg = bookmarks["id_tg"]
        position = bookmarks["position"]
        result = controller_bookmarks.update_bookmarks(id_book, id_tg, position)
        print(result)
        if result == 2:
            return "Закладка успешно обновлена."
        else:
            return "Ошибка при обновление закладки."
    except Exception:
        return "Ошибка при обновление закладки."

@app_bookmarks.route("/bookmarks/delete", methods = ["DELETE"])
#@jwt_required()
def delete_bookmarks():
    try:
        id_book = request.args.get('id_book', default=None,type=int)
        id_tg = request.args.get('id_tg', default=None,type=int)
        result = controller_bookmarks.delete_bookmarks(id_book, id_tg)
        print("checkrouter",result)
        if result == 2:
            return "Закладка не найдена или успешно удалена."
        else:
            return "Ошибка при удалении закладки."
    except Exception:
        return "Ошибка при удалении закладки."