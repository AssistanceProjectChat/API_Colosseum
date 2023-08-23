from flask import Blueprint, redirect, request, render_template, send_from_directory, url_for
from flask_jwt_extended import jwt_required
import controller.controller_books as controller_books
import string
import os
from werkzeug.utils import secure_filename


app_book= Blueprint('route_book', __name__)

if not os.path.isdir("img"):
            os.mkdir("img")

@app_book.route("/books", methods = ["GET"])
#@jwt_required()
def get_all_books_by_id():
    all_books = controller_books.get_all_books()
    return all_books

@app_book.route("/books/<book_id>", methods = ["GET"])
#@jwt_required()
def get_book_by_id(book_id):
    book = controller_books.get_book(book_id)
    if book is not None:
        return book
    else:
        return redirect("Not Found"), 404

@app_book.route("/books", methods = ["POST"])
#@jwt_required()
def insert_book():
    import main
    try:             
        book = request.get_json()
        name_book = book["name_book"]
        episode_num = book["episode_num"]
        img_name = str(name_book).translate({ord(c): None for c in string.whitespace})
        img_book = img_name
        text_book = book["text_book"]
        date_add = book["date_add"]
        price_book = book["price_book"]
        result = controller_books.insert_book(name_book, episode_num, img_book, text_book, date_add, price_book)
        if result == True:
            return "Книга успешно добавлена."
        else:
            return "Ошибка при добавлении книги."
    except Exception as e:
        return "Ошибка при добавлении книги."
    
@app_book.route("/books/uploads", methods = ["POST","GET"])
def upload_img():
    if request.method == "POST":
        try:
            import main
            name_book = request.args.get('name_book', default=None,type=str)
            img_name = str(name_book).translate({ord(c): None for c in string.whitespace})
            file = request.files['file']           
            filename = secure_filename(file.filename)
            if filename.find(".jpg") != -1:
                filename_jpg = img_name + '.jpg'
                file.save(os.path.join(main.app.config['UPLOAD_FOLDER'], filename_jpg))
                return "File upload"
            else:
                return "The file must have the only JPG extension"
        except Exception:
            return "File error"

@app_book.route("/books/uploads/<name>")
def display_img(name):
    import main
    return send_from_directory(main.app.config["UPLOAD_FOLDER"], name)

@app_book.route("/books", methods = ["PUT"])
#@jwt_required()
def update_book():
    try:
        book = request.get_json()
        book_id = book["book_id"]
        name_book = book["name_book"]
        episode_num = book["episode_num"]
        img_book = book["img_book"]
        text_book = book["text_book"]
        date_add = book["date_add"]
        price_book = book["price_book"]
        result = controller_books.update_book(book_id, name_book, episode_num, img_book, text_book, date_add, price_book)
        print(result)
        if result == 2:
            return "Книга успешно обновлена."
        else:
            return "Ошибка при обновление книги."
    except Exception:
        return "Ошибка при обновление книги."

@app_book.route("/books/delete/<book_id>", methods = ["DELETE"])
#@jwt_required()
def delete_book(book_id):
    try:
        result = controller_books.delete_book(book_id)
        print("checkrouter",result)
        if result == 2:
            return "Книга не найдена или успешно удалена."
        else:
            return "Ошибка при удалении книги."
    except Exception:
        return "Ошибка при удалении книги."