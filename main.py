from flask import Flask, jsonify, redirect, request
from datetime import timedelta
from db_check import create_tables
from router.router_user import app_user
from router.router_books import app_book
from router.router_bookmarks import app_bookmarks
from router.router_purchase_books import app_purchase_books
from router.router_last_open import app_last_open
import logging
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token, create_refresh_token
import controller.controller_users as controller_users

###################### Запуск API ######################
app = Flask(__name__)
app.register_blueprint(app_user)
app.register_blueprint(app_book)
app.register_blueprint(app_bookmarks)
app.register_blueprint(app_purchase_books)
app.register_blueprint(app_last_open)
app.config['JWT_SECRET_KEY'] = 'PpUM?vFJnErhg(#L{h4j2pfNEj=U=X]$–S%DOM9/qP{Hkb(iVv273OQWLdt+=H~_'
app.config["JWT_ALGORITHM"] = 'HS256'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=10)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
UPLOAD_FOLDER = "img"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)

############### Приветственное сообщение ###############
@app.route('/', methods=['GET'])
@jwt_required()
async def index():
    return jsonify(message="Successful login")

@app.route('/login_user', methods=['POST'])
async def login_user():
    if request.is_json:
        tg_id = request.json['tg_id']
        tg_num_phone = request.json['tg_num_phone']
    result = controller_users.get_users_login(tg_id, tg_num_phone)
    print (result)
    if result:
        access_token = create_access_token(identity=tg_id)
        refresh_token = create_refresh_token(identity=tg_id)
        return jsonify(message='User Successful', access_token=access_token, refresh_token=refresh_token)
    else:
        return jsonify('Bad data'), 401
    
@app.route('/login_bot', methods=['POST'])
async def login_bot():
    try:
        if request.is_json:
            tg_id = request.json['tg_id']
            note = request.json['note']
        result = controller_users.get_bot_login(tg_id, note)
        print (result)
        if result:
            access_token = create_access_token(identity=tg_id)
            refresh_token = create_refresh_token(identity=tg_id)
            return jsonify(message='Bot Successful', access_token=access_token, refresh_token=refresh_token)
        else:
            return jsonify('Bad data'), 401
    except Exception:
        return jsonify('Bad data'), 401
    
@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
async def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

############ CORS ###########
# Access-Control-Allow-Origin указывает домен, из которого будут разрешены запросы. 
# Учетные данные полезны, если вы используете сеансы или файлы cookie. 
# Access-Control-Allow-Methods указывает, какие методы HTTP допустимы для CORS.
# Наконец, Access-Control-Allow-Headers указывает, какие заголовки будут приняты для CORS.

@app.after_request
async def after_request(respoinse):
    respoinse.headers["Access-Control-Allow-Origin"] = "*"
    respoinse.headers["Access-Control-Allow-Credentials"] = "true"
    respoinse.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    respoinse.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return respoinse

if __name__ == "__main__":
    create_tables()
    #logging.basicConfig(filename='api_book.log', encoding='utf-8', level=logging.INFO)
    app.run(host='192.168.146.186', port=7061, debug=True)