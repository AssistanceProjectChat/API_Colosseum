from flask import Flask, jsonify, redirect, request
from db_check import create_tables
from router.router_user import app_user
import logging
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import controller.controller_users as controller_users

###################### Запуск API ######################
app = Flask(__name__)
app.register_blueprint(app_user)
app.config['JWT_SECRET_KEY'] = 'PpUM?vFJnErhg(#L{h4j2pfNEj=U=X]$–S%DOM9/qP{Hkb(iVv273OQWLdt+=H~_'
jwt = JWTManager(app)

############### Приветственное сообщение ###############
@app.route('/', methods=['GET'])
@jwt_required()
def index():
    return jsonify(message="Hello Flask!")

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        tg_id = request.json['tg_id']
        tg_num_phone = request.json['tg_num_phone']
    result = controller_users.get_users_login(tg_id, tg_num_phone)
    print (result)
    if result:
        access_token = create_access_token(identity=tg_id)
        return jsonify(message='Login Successful', access_token=access_token)
    else:
        return jsonify('Bad data'), 401

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