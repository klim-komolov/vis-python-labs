from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import hashlib
import bleach

app = Flask(__name__)
application = app
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_message = 'Для доступа к данной странице необходимо авторизоваться'
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    middle_name = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    users = db.relationship('User', backref='role', cascade='all, delete-orphan', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('cover.id', ondelete='CASCADE'), nullable=False)
    cover = db.relationship('Cover', backref=db.backref('books', lazy=True, cascade='all, delete-orphan'))
    reviews = db.relationship('Review', backref='book', cascade='all, delete-orphan', lazy=True)
    genres = db.relationship('Genre', secondary='books_genres', lazy='subquery',
                             backref=db.backref('book_list', lazy=True))
    @property
    def average_rating(self):
        average = db.session.query(func.avg(Review.rating)).filter(Review.book_id == self.id).scalar()
        return round(average, 2) if average is not None else None
    
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Cover(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(255), nullable=False)
    md5_hash = db.Column(db.String(255), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BooksGenres(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='CASCADE'), primary_key=True)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', back_populates='collections')
    books = db.relationship('Book', secondary='collection_books', back_populates='collections')

class CollectionBooks(db.Model):
    __tablename__ = 'collection_books'
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)

User.collections = db.relationship('Collection', back_populates='user', lazy=True)
Book.collections = db.relationship('Collection', secondary='collection_books', back_populates='books')


@property
def average_rating(self):
    average = db.session.query(func.avg(Review.rating)).filter(Review.book_id == self.id).scalar()
    return round(average, 2) if average is not None else None
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        logins = request.form['login']
        password = request.form['password']
        user = User.query.filter_by(login=logins).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Вы успешно вошли в систему.')
            return redirect(url_for('index'))
        else:
            flash('Невозможно аутентифицироваться с указанными логином и паролем')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы')
    return redirect(url_for('login'))

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books_pagination = Book.query.order_by(Book.year.desc()).paginate(page, 10, False)
    books = books_pagination.items
    return render_template('index.html', books=books, pagination=books_pagination)


@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    user_review = None
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    return render_template('book.html', book=book, user_review=user_review)

@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    genres = Genre.query.all()
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        description = bleach.clean(request.form['description'])
        year = request.form['year']
        publisher = request.form['publisher']
        author = request.form['author']
        pages = request.form['pages']
        genre_ids = request.form.getlist('genres')

        cover = request.files['cover']
        cover_data = cover.read()
        cover.seek(0)
        cover_hash = hashlib.md5(cover_data).hexdigest()
        cover_record = Cover.query.filter_by(md5_hash=cover_hash).first()

        if not cover_record:
            cover_record = Cover(
                file_name=secure_filename(cover.filename),
                mime_type=cover.mimetype,
                md5_hash=cover_hash
            )
            db.session.add(cover_record)
            db.session.flush() 

        new_book = Book(
            title=title,
            description=description,
            year=year,
            publisher=publisher,
            author=author,
            pages=pages,
            cover_id=cover_record.id
        )
        for genre_id in genre_ids:
            genre = Genre.query.get(genre_id)
            if genre:
                new_book.genres.append(genre)

        try:
            db.session.add(new_book)
            db.session.commit()
            cover.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_record.file_name))
            flash('Книга успешно добавлена!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            return render_template('add_book.html', genres=genres, selected_genres=new_book.genres, cover_required=True)

    return render_template('add_book.html', genres=genres, selected_genres=[], cover_required=True)

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    genres = Genre.query.all()
    if current_user.role.name not in ['admin', 'moderator']:
        flash('У вас недостаточно прав для выполнения данного действия')
        return redirect(url_for('index'))
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = bleach.clean(request.form['description'])
        book.year = request.form['year']
        book.publisher = request.form['publisher']
        book.author = request.form['author']
        book.pages = request.form['pages']
        genre_ids = request.form.getlist('genres')

        book.genres = []
        for genre_id in genre_ids:
            genre = Genre.query.get(genre_id)
            if genre:
                book.genres.append(genre)

        try:
            db.session.commit()
            flash('Книга успешно обновлена!', 'success')
            return redirect(url_for('book_detail', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.', 'danger')
            return render_template('edit_book.html', book=book, genres=genres, selected_genres=book.genres, cover_required=False)

    return render_template('edit_book.html', book=book, genres=genres, selected_genres=book.genres, cover_required=False)

@app.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    cover = book.cover
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для выполнения данного действия')
        return redirect(url_for('index'))
    
    try:
        db.session.delete(book)
        db.session.commit()
        if cover:
            cover_path = os.path.join(app.config['UPLOAD_FOLDER'], cover.file_name)
            if os.path.exists(cover_path):
                os.remove(cover_path)
        flash('Книга успешно удалена.')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении книги. Попробуйте еще раз.')
    
    return redirect(url_for('index'))

@app.route('/book/<int:book_id>/review/add', methods=['GET', 'POST'])
@login_required
def add_review(book_id):
    book = Book.query.get_or_404(book_id)
    existing_review = Review.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if existing_review:
        flash('Вы уже написали рецензию на эту книгу')
        return redirect(url_for('book_detail', book_id=book_id))

    if request.method == 'POST':
        rating = request.form['rating']
        text = bleach.clean(request.form['text'])
        review = Review(rating=rating, text=text, user_id=current_user.id, book_id=book_id)
        db.session.add(review)
        db.session.commit()
        flash('Рецензия успешно добавлена')
        return redirect(url_for('book_detail', book_id=book_id))

    return render_template('add_review.html', book=book)

@app.route('/collections', methods=['GET'])
@login_required
def collections():
    collections = Collection.query.filter_by(user_id=current_user.id).all()
    return render_template('collections.html', collections=collections)

@app.route('/collection/add', methods=['POST'])
@login_required
def add_collection():
    name = request.form.get('name')
    new_collection = Collection(name=name, user_id=current_user.id)
    db.session.add(new_collection)
    db.session.commit()
    flash('Подборка успешно добавлена!', 'success')
    return redirect(url_for('collections'))

@app.route('/collection/<int:collection_id>', methods=['GET'])
@login_required
def view_collection(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    if collection.user_id != current_user.id:
        abort(403)
    return render_template('collection_books.html', collection=collection)

@app.route('/book/<int:book_id>/add_to_collection', methods=['POST'])
@login_required
def add_book_to_collection(book_id):
    collection_id = request.form.get('collection_id')
    collection = Collection.query.get_or_404(collection_id)
    if collection.user_id != current_user.id:
        abort(403)
    book = Book.query.get_or_404(book_id)
    collection.books.append(book)
    db.session.commit()
    flash('Книга успешно добавлена в подборку!', 'success')
    return redirect(url_for('book_detail', book_id=book_id))

if __name__ == '__main__':
    app.run(debug=True)
