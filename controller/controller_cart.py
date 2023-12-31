from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск всех книг в корзине по tg id ##############
def get_cart(id_tg):
    db = get_db()
    params = (id_tg)
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    row = cursor.execute("select * from cart where id_tg = ?", (params,)).fetchall()
    cart_json = [{k: item[k] for k in item.keys()} for item in row]
    return jsonify(cart_json)

############## Добавить книги в корзину ##############
def insert_book_cart(id_tg, id_book):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (id_tg, id_book)
    res = cursor.execute("select count(id_tg) from cart where id_tg = ? and id_book = ?", params)
    for row in res:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("insert_trigger",row_s2)
        int_rows = int(row_s2)
    if int_rows == 0:
        try:
            cursor.execute("insert into cart (id_tg, id_book) values (?, ?)", params)
        except Exception:
            print("Ошибка при добавлении книги в корзину.")
            return False
        db.commit()
        return True
    else:
        print("Книга уже в корзине.")
        return False

############## Обновить триггер книг ##############
def update_cart_trigger(id_tg):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    trigger_buy = 1
    params = (trigger_buy, id_tg)
    params_check = (id_tg)
    res = cursor.execute("select count(id_tg) from cart where id_tg = ?", (params_check,))
    for row in res:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("update_trigger",row_s2)
        int_rows = int(row_s2)
    if int_rows != 0:
        try:
            cursor.execute("update cart set trigger_buy = ? where id_tg = ?", params)
            db.commit()
            return "Purchase_ok"
        except:
            print("check1")
            return "Purchase_error"
    else:
        return "Purchase_error"
