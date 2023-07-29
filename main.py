from flask import Flask, jsonify, redirect, request
from db_check import create_tables
from router.router_user import app_user
import logging
###################### Запуск API ######################
app = Flask(__name__)
app.register_blueprint(app_user)

############ CORS ###########
# Access-Control-Allow-Origin указывает домен, из которого будут разрешены запросы. 
# Учетные данные полезны, если вы используете сеансы или файлы cookie. 
# Access-Control-Allow-Methods указывает, какие методы HTTP допустимы для CORS.
# Наконец, Access-Control-Allow-Headers указывает, какие заголовки будут приняты для CORS.

@app.after_request
def after_request(respoinse):
    respoinse.headers["Access-Control-Allow-Origin"] = "*"
    respoinse.headers["Access-Control-Allow-Credentials"] = "true"
    respoinse.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    respoinse.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return respoinse

if __name__ == "__main__":
    create_tables()
    #logging.basicConfig(filename='api_book.log', encoding='utf-8', level=logging.INFO)
    app.run(host='192.168.146.186', port=7061, debug=True)