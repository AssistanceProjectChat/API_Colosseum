from flask import Blueprint, redirect, request
import controller.controller_users as controller_users

app_user = Blueprint('route', __name__)

@app_user.route("/users", methods = ["GET"])
def get_all_users_by_id():
    all_users = controller_users.get_all_users()
    return all_users

@app_user.route("/users/<tg_id>", methods = ["GET"])
def get_user_by_id(tg_id):
    user = controller_users.get_users(tg_id)
    if user is not None:
        return user
    else:
        return redirect("Not Found"), 404

@app_user.route("/users", methods = ["POST"])
def insert_user():
    tg_user = request.get_json()
    tg_id = tg_user["tg_id"]
    tg_num_phone = tg_user["tg_num_phone"]
    tg_nick = tg_user["tg_nick"]
    result = controller_users.insert_users(tg_id, tg_num_phone, tg_nick)
    if result == True:
        return "Пользователь успешно добавлен!!!"
    else:
        return "Ошибка при добавлении пользователя!!!"

@app_user.route("/users", methods = ["PUT"])
def update_users():
    tg_user = request.get_json()
    tg_id = tg_user["tg_id"]
    tg_num_phone = tg_user["tg_num_phone"]
    result = controller_users.update_users(tg_id, tg_num_phone)
    print(result)
    if result == 1:
        return "Номера телефона успешно обновлён!!!"
    else:
        return "Ошибка при обновление номера телефона пользователя!!!!!!"