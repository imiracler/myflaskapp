from flask import Blueprint

book = Blueprint("book", __name__)

@book.route("/book/get")
def get_book():
    return "this is my first book"