from db_check import get_db
from flask import jsonify
import sqlite3

############## Поиск всех книг ##############
def get_all_books():
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    query = "select book_id, name_book, episode_num, text_book, date_add, price_book from books"
    row = cursor.execute(query).fetchall()
    # тут один цикл вложен в другой, первый цикл проходится по наименованиям столбцов
    # а второй сопоставляет значения с этими столбцами
    books_json = [{k: item[k] for k in item.keys()} for item in row]
    return jsonify(books_json)

############## Поиск конкретной книги ##############
def get_book(book_id):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (book_id)
    cursor.execute("select * from books where book_id = ?", (params,))
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        return jsonify(str(rowdict))

############## Добавление новых книг ##############
def insert_book(name_book, episode_num, img_book, text_book, date_add, price_book):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (name_book, episode_num, img_book, text_book, date_add, price_book)
    try:
        cursor.execute("insert into books (name_book, episode_num, img_book, text_book, date_add, price_book) values (?, ?, ?, ?, ?, ?)", params)
    except Exception:
        print("Ошибка при добавлении книги.")
        return False
    db.commit()
    return True

############## Обновление параметров книги у существующих книг ##############
def update_book(book_id, name_book, episode_num, img_book, text_book, date_add, price_book):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params = (name_book, episode_num, img_book, text_book, date_add, price_book, book_id)
    params_check = (book_id)
    res = cursor.execute("select count(book_id) from books where book_id = ?", (params_check,))
    print(res)
    for row in res:
        row_s1 = str(row).replace("(",'')
        row_s2 = row_s1.replace(",)",'')
        print("checkpoint1",row_s2)
        int_rows = int(row_s2)
        if int_rows != 1:
            print("Ошибка при обновление книги.")
            print('checkpoint2',int_rows)
            return 1
        else:
            cursor.execute("update books set name_book = ?, episode_num =?, img_book = ?, text_book = ?, date_add = ?, price_book = ? where book_id = ?", params)
            db.commit()
            print('checkpoint3',int_rows)
            return 2

############## Удаление книги ##############
def delete_book(book_id):
    db = get_db()
    cursor = db.cursor()
    db.row_factory = sqlite3.Row
    params_check = (book_id)
    res = cursor.execute("delete from books where book_id = ?", params_check)
    print("deletecheck1", params_check)
    db.commit()
    res_count = cursor.execute("select count(book_id) from books where book_id = ?", (params_check,))
    res_count = res.fetchone()
    row_s1 = str(res_count).replace("(",'')
    row_s2 = row_s1.replace(",)",'')
    print("checkpoint1",row_s2)
    int_rows = int(row_s2)
    if int_rows == 0:
        return 2
    else:
        return "Ошибка при удалении книги."
        
        