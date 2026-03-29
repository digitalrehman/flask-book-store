from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ====================== Database Model ======================
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

# ====================== Create Database Tables ======================
with app.app_context():
    db.create_all()

# ====================== CRUD Routes ======================

# CREATE - New Book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('author'):
        return jsonify({"error": "Title and Author are required"}), 400

    new_book = Book(
        title=data['title'],
        author=data['author'],
        year=data.get('year')
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({
        "message": "Book added successfully",
        "book": new_book.to_dict()
    }), 201


# READ ALL - Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify({
        "total": len(books),
        "books": [book.to_dict() for book in books]
    })


# READ ONE - Get single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)   # get() id ke through directly search karta hai
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    return jsonify(book.to_dict())


# UPDATE
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
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
        "book": book.to_dict()
    })


# DELETE
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message": "Book deleted successfully"})


# Home
@app.route('/')
def home():
    return jsonify({"message": "Flask CRUD with Database is running"})


if __name__ == '__main__':
    app.run(debug=True)