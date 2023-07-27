from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск всех пользователей ##############
def get_all_users():
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    query = "select tg_id, tg_num_phone, tg_nick from users"
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
    cursor.execute("select tg_id, tg_num_phone, tg_nick from users where tg_id = ?", (params,))
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(rowdict)
    
############## Добавление новых пользователей ##############
def insert_users(tg_id, tg_num_phone, tg_nick):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (tg_id, tg_num_phone, tg_nick)
    cursor.execute("insert into users (tg_id, tg_num_phone, tg_nick) values (?, ?, ?)"), (params,)
    db.commit()
    return True



############## Обновление номера телефона пользователей ##############