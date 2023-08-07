from flask import Blueprint, redirect, request
from flask_jwt_extended import jwt_required
import controller.controller_last_open as controller_last_open
from datetime import datetime

app_last_open= Blueprint('route_last_open', __name__)

@app_last_open.route("/last_open", methods = ["GET"])
#@jwt_required()
def get_last_open_by_id():
    id_book = request.args.get('id_book', default=None,type=int)
    id_tg = request.args.get('id_tg', default=None,type=int)
    last_open = controller_last_open.get_last_open(id_book, id_tg)
    if last_open is not None:
        return last_open
    else:
        return redirect("Not Found"), 404

@app_last_open.route("/last_open", methods = ["POST"])
#@jwt_required()
def insert_last_open():
    try:
        last_open = request.get_json()
        id_book = last_open["id_book"]
        id_tg = last_open["id_tg"]
        last_open_book = datetime.today()
        result = controller_last_open.insert_last_open(id_book, id_tg, str(last_open_book))
        if result == True:
            return "Успешное добавление последней книги."
        else:
            return "Ошибка при Ошибка при добавление последней книги.(2)"
    except Exception:
        return "Ошибка при добавление последней книги.(3)"