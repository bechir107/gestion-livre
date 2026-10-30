
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:4200"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Connexion MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:@localhost/books_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modèle correspondant à la table existante "livre"
class Book(db.Model):
    __tablename__ = 'livre'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    année = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.titre,
            'author': self.auteur,
            'year': self.année
        }


# Vérifier la connexion MySQL
@app.route('/', methods=['GET'])
def home():
    try:
        with db.engine.connect():
            return jsonify({
                'message': 'Connexion à MySQL réussie !',
                'database': 'books_db'
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ : récupérer tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.order_by(Book.id.desc()).all()
        return jsonify([book.to_dict() for book in books]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# CREATE : ajouter un livre
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json(silent=True) or {}

    title = data.get('title')
    author = data.get('author')
    year = data.get('year')

    if not isinstance(title, str) or not title.strip():
        return jsonify({'error': 'Le titre est obligatoire'}), 400

    if not isinstance(author, str) or not author.strip():
        return jsonify({'error': "L'auteur est obligatoire"}), 400

    try:
        year = int(year)
        if year < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': "L'année est invalide"}), 400

    book = Book(
        titre=title.strip(),
        auteur=author.strip(),
        année=year
    )

    try:
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# UPDATE : modifier un livre
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = db.session.get(Book, id)

    if book is None:
        return jsonify({'error': 'Livre introuvable'}), 404

    data = request.get_json(silent=True) or {}

    title = data.get('title', book.titre)
    author = data.get('author', book.auteur)
    year = data.get('year', book.année)

    if not isinstance(title, str) or not title.strip():
        return jsonify({'error': 'Le titre est obligatoire'}), 400

    if not isinstance(author, str) or not author.strip():
        return jsonify({'error': "L'auteur est obligatoire"}), 400

    try:
        year = int(year)
        if year < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': "L'année est invalide"}), 400

    book.titre = title.strip()
    book.auteur = author.strip()
    book.année = year

    try:
        db.session.commit()
        return jsonify(book.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# DELETE : supprimer un livre
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = db.session.get(Book, id)

    if book is None:
        return jsonify({'error': 'Livre introuvable'}), 404

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Livre supprimé avec succès'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='127.0.0.1', port=5000, debug=True)
