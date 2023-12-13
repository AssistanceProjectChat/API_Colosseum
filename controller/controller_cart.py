from db_check import get_db
from flask import jsonify
import sqlite3

def get_cart(id_tg):
    db = get_db()
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    params = (id_tg)
    cursor.execute("select * from cart where id_tg = ?", (params,))
    row = cursor.fetchone()
    desc = list(zip(*cursor.description))[0]
    if row is not None:
        rowdict = dict(zip(desc,row))
        print(rowdict)
        return jsonify(str(rowdict))
