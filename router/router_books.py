from flask import Blueprint, redirect, request
from flask_jwt_extended import jwt_required
import controller.controller_books as controller_books

app_book= Blueprint('route_book', __name__)

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
    try:
        book = request.get_json()
        name_book = book["name_book"]
        episode_num = book["episode_num"]
        img_book = book["img_book"]
        text_book = book["text_book"]
        date_add = book["date_add"]
        price_book = book["price_book"]
        result = controller_books.insert_book(name_book, episode_num, img_book, text_book, date_add, price_book)
        if result == True:
            return "Книга успешно добавлена."
        else:
            return "Ошибка при добавлении книги."
    except Exception:
        return "Ошибка при добавлении книги."

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