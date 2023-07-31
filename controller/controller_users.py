from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск всех пользователей ##############
def get_all_users():
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    query = "select tg_id, tg_num_phone, tg_nick, tg_chat_id from users"
    row = cursor.execute(query).fetchall()
    # тут один цикл вложен в другой, первый цикл проходится по наименованиям столбцов
    # а второй сопоставляет значения с этими столбцами
    users_json = [{k: item[k] for k in item.keys()} for item in row]
    return jsonify(users_json)

############## Поиск конкретного пользователя ##############
def get_users(tg_id):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (tg_id)
    cursor.execute("select tg_id, tg_num_phone, tg_nick, tg_chat_id from users where tg_id = ?", (params,))
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(rowdict)

############## Поиск пользователя для логина ##############
def get_users_login(tg_id, tg_num_phone):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (tg_id, tg_num_phone)
    cursor.execute("select tg_id, tg_num_phone from users where tg_id = ? and tg_num_phone = ?", params)
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(rowdict)

############## Добавление новых пользователей ##############
def insert_users(tg_id, tg_num_phone, tg_nick, tg_chat_id):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (tg_id, tg_num_phone, tg_nick, tg_chat_id)
    try:
        cursor.execute("insert into users (tg_id, tg_num_phone, tg_nick, tg_chat_id) values (?, ?, ?, ?)", params)
    except Exception:
        print("Ошибка при добавлении пользователя!!!")
        return False
    db.commit()
    return True

############## Обновление номера телефона у существующих пользователей ##############
def update_users(tg_id, tg_num_phone):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (tg_num_phone, tg_id)
    params_check = (tg_id)
    res = cursor.execute("select count(tg_id) from users where tg_id = ?", (params_check,))
    for row in res:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        int_row = int(row_s2)
        if int_row != 1:
            print("Ошибка при обновление номера телефона пользователя!!!")
            print('1',int_row)
            return int_row
        else:
            cursor.execute("update users set tg_num_phone = ? where tg_id = ?", params)
            db.commit()
            print('2',int_row)
            return int_row