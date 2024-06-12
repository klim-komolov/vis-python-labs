from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import hashlib
import bleach 

app = Flask(__name__)
application = app
app.config.from_object('config.Config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
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



from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import hashlib
import bleach

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Определение моделей...

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Вы успешно вошли в систему.')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('login'))

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = Book.query.order_by(Book.year.desc()).paginate(page, 10, False)
    return render_template('index.html', books=books.items, pagination=books)

@app.route('/book/<int:book_id>')
def book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)

@app.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для удаления этой книги')
        return redirect(url_for('index'))

    try:
        db.session.delete(book)
        db.session.commit()
        flash('Книга успешно удалена')
    except Exception as e:
        db.session.rollback()
        flash('Произошла ошибка при удалении книги')

    return redirect(url_for('index'))

@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role.name != 'admin':
        flash('У вас недостаточно прав для добавления книги')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        description = bleach.clean(request.form['description'])
        year = request.form['year']
        publisher = request.form['publisher']
        author = request.form['author']
        pages = request.form['pages']
        genres = request.form.getlist('genres')
        cover_file = request.files['cover']

        if cover_file:
            cover_filename = secure_filename(cover_file.filename)
            cover_mimetype = cover_file.mimetype
            cover_data = cover_file.read()
            cover_md5 = hashlib.md5(cover_data).hexdigest()

            existing_cover = Cover.query.filter_by(md5_hash=cover_md5).first()
            if existing_cover:
                cover = existing_cover
            else:
                cover = Cover(file_name=cover_filename, mime_type=cover_mimetype, md5_hash=cover_md5)
                db.session.add(cover)
                db.session.commit()
                cover_path = os.path.join(app.root_path, 'static', 'covers', str(cover.id) + os.path.splitext(cover_filename)[1])
                with open(cover_path, 'wb') as f:
                    f.write(cover_data)

        book = Book(title=title, description=description, year=year, publisher=publisher, author=author, pages=pages, cover=cover)
        db.session.add(book)

        for genre_id in genres:
            genre = Genre.query.get(genre_id)
            book.genres.append(genre)

        try:
            db.session.commit()
            flash('Книга успешно добавлена')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.')
            return render_template('add_book.html', genres=Genre.query.all())

    return render_template('add_book.html', genres=Genre.query.all())

@app.route('/book/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if current_user.role.name not in ['admin', 'moderator']:
        flash('У вас недостаточно прав для редактирования этой книги')
        return redirect(url_for('index'))

    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.year = request.form['year']
        book.publisher = request.form['publisher']
        book.author = request.form['author']
        book.pages = request.form['pages']
        genres = request.form.getlist('genres')

        book.genres = []
        for genre_id in genres:
            genre = Genre.query.get(genre_id)
            book.genres.append(genre)

        try:
            db.session.commit()
            flash('Книга успешно отредактирована')
            return redirect(url_for('book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('При сохранении данных возникла ошибка. Проверьте корректность введённых данных.')
            return render_template('edit_book.html', book=book, genres=Genre.query.all())

    return render_template('edit_book.html', book=book, genres=Genre.query.all())

if __name__ == '__main__':
    app.run(debug=True)
