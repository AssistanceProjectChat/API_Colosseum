from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск конкретной покупки ##############
def get_purchases_books(id_book, id_tg):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (id_book, id_tg)
    cursor.execute("select * from purchases_books where id_book = ? and id_tg = ?", params)
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(str(rowdict))

############## Добавление новых покупок ##############
def insert_purchases_books(id_book, id_tg, datatime_purchase):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (id_tg, id_book, datatime_purchase)
    print (params)
    try:    
        cursor.execute("insert into purchases_books (id_tg, id_book, datatime_purchase) values (?, ?, ?)", params)
        db.commit()
        return True
    except Exception:
        print("Ошибка при покупке.(1)")
        db.rollback()
        return False