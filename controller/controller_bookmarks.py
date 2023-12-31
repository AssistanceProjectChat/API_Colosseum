from db_check import get_db
from flask import jsonify
import sqlite3


############## Поиск конкретной закладки ##############
def get_bookmarks(id_book, id_tg):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (id_book, id_tg)
    cursor.execute("select * from bookmarks where id_book = ? and id_tg = ?", params)
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(str(rowdict))

############## Добавление новых закладок ##############
def insert_bookmarks(id_book, id_tg, position):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (id_book, id_tg, position)
    param_check = (id_book, id_tg)
    #сделать проверку на существование закладки на выбранную книгу
    #на одну книгу одну закладку
    check_s = cursor.execute("select count(id_book) from bookmarks where id_book = ? and id_tg = ?", param_check)
    for row in check_s:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("checkpoint1",row_s2)
        int_rows = int(row_s2)
        if int_rows == 0:
            cursor.execute("insert into bookmarks (id_book, id_tg, position) values (?, ?, ?)", params)
            db.commit()
            return True
        else:
            print("Ошибка при добавлении закладки.(2)")
            return False

############## Обновление параметров закладки ##############
def update_bookmarks(id_book, id_tg, position):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (id_tg, position, id_book)
    params_check = (id_book)
    res = cursor.execute("select count(id_book) from bookmarks where id_book = ?", (params_check,))
    print(res)
    for row in res:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("checkpoint1",row_s2)
        int_rows = int(row_s2)
        if int_rows != 1:
            print("Ошибка при обновление закладки.")
            print('checkpoint2',int_rows)
            return 1
        else:
            cursor.execute("update bookmarks set position =? where id_book = ?, id_tg = ?", params)
            db.commit()
            print('checkpoint3',int_rows)
            return 2

############## Удаление закладки ##############
def delete_bookmarks(id_book,id_tg):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params_check = (id_book, id_tg)
    res = cursor.execute("delete from bookmarks where id_book = ? and id_tg = ?", params_check)
    print("deletecheck1", params_check)
    db.commit()
    res_count = cursor.execute("select count(id_book) from bookmarks where id_book = ? and id_tg = ?", params_check)
    res_count = res.fetchone()
    row_s1 = str(res_count).replace("(",'')
    row_s2 = row_s1.replace(",)",'')
    print("checkpoint1",row_s2)
    int_rows = int(row_s2)
    if int_rows == 0:
        return 2
    else:
        return "Ошибка при удалении закладки."
        