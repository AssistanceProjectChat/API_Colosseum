from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск конкретной последней октрытой книги ##############
def get_last_open(id_book, id_tg):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (id_book, id_tg)
    cursor.execute("select * from last_open where id_book = ? and id_tg = ?", params)
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(str(rowdict))

############## Добавление новых открытых книг ##############
def insert_last_open(id_book, id_tg, last_open_book):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (id_tg, id_book, last_open_book)
    print (params)
    param_check = (id_tg)
    check_s = cursor.execute("select count(id_book) from last_open where id_tg = ?", (param_check,))
    for row in check_s:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("checkpoint1",row_s2)
        int_rows = int(row_s2)
        if int_rows == 0:  
            cursor.execute("insert into last_open (id_tg, id_book, last_open_book) values (?, ?, ?)", params)
            db.commit()
            return True
        else:
            print("Ошибка при добавление последней книги.(1)")
            db.rollback()
            otvet_def = update_last_open(id_book, id_tg, last_open_book)
            return otvet_def

def update_last_open(id_book, id_tg, last_open_book):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (last_open_book, id_book, id_tg)
    print (params)
    param_check = (id_tg)
    check_s = cursor.execute("select count(id_tg) from last_open where id_tg = ?", (param_check,))
    for row in check_s:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("checkpoint1",row_s2)
        int_rows = int(row_s2)
        if int_rows == 1:  
            cursor.execute("update last_open set last_open_book = ?, id_book = ? where id_tg = ?", params)
            db.commit()
            return True
        else:
            print("Ошибка при обновлении последней книги.(4)")
            db.rollback()
            return False