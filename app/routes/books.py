from flask import Blueprint, jsonify, request
from app import db
from app.models.book import Book

books_bp = Blueprint('books', __name__)

# Helper
def get_book_or_404(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return book


@books_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('author'):
        return jsonify({"error": "Title and author are required"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        year=data.get('year')
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({
        "message": "Book created successfully",
        "book": new_book.serialize()
    }), 201


@books_bp.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify({
        "total": len(books),
        "books": [book.serialize() for book in books]
    })


@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_or_404(book_id)
    return jsonify(book.serialize())


@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = get_book_or_404(book_id)
    data = request.get_json()

    if data.get('title'):
        book.title = data['title']
    if data.get('author'):
        book.author = data['author']
    if data.get('year') is not None:
        book.year = data['year']

    db.session.commit()
    return jsonify({
        "message": "Book updated successfully",
        "book": book.serialize()
    })


@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = get_book_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200