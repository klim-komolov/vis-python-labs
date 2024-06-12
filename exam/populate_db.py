from app import db, User, Role, Book, Genre, Cover, Review
from werkzeug.security import generate_password_hash

def create_roles():
    roles = [
        {'name': 'admin', 'description': 'Administrator with full access'},
        {'name': 'moderator', 'description': 'Moderator with limited access'},
        {'name': 'user', 'description': 'Regular user'}
    ]
    for role_data in roles:
        role = Role(name=role_data['name'], description=role_data['description'])
        db.session.add(role)
    db.session.commit()

def create_users():
    users = [
        {'login': 'admin', 'password': 'adminpass', 'last_name': 'Admin', 'first_name': 'Admin', 'role': 'admin'},
        {'login': 'moderator', 'password': 'modpass', 'last_name': 'Mod', 'first_name': 'Moderator', 'role': 'moderator'},
        {'login': 'user', 'password': 'userpass', 'last_name': 'User', 'first_name': 'Regular', 'role': 'user'}
    ]
    for user_data in users:
        role = Role.query.filter_by(name=user_data['role']).first()
        user = User(login=user_data['login'], last_name=user_data['last_name'], first_name=user_data['first_name'], role_id=role.id)
        user.set_password(user_data['password'])
        db.session.add(user)
    db.session.commit()

def create_genres():
    genres = ['Фантастика', 'Наука', 'Биография', 'Фэнтези']
    for genre_name in genres:
        genre = Genre(name=genre_name)
        db.session.add(genre)
    db.session.commit()

def create_cover():
    cover = Cover(
        file_name='book.jpg',
        mime_type='image/jpeg',
        md5_hash='d41d8cd98f00b204e9800998ecf8427e'
    )
    db.session.add(cover)
    db.session.commit()
    return cover

def create_books(common_cover):
    books = [
        {
            'title': 'Великий Гэтсби',
            'description': 'Роман, написанный американским писателем Ф. Скоттом Фицджеральдом.',
            'year': 1925,
            'publisher': 'Скрибнер',
            'author': 'Ф. Скотт Фицджеральд',
            'pages': 218,
            'cover_id': common_cover.id
        },
        {
            'title': 'Убить пересмешника',
            'description': 'Роман Харпер Ли, опубликованный в 1960 году.',
            'year': 1960,
            'publisher': 'Джей Би Липпинкотт и компания',
            'author': 'Харпер Ли',
            'pages': 281,
            'cover_id': common_cover.id
        }
    ]
    for book_data in books:
        book = Book(
            title=book_data['title'], 
            description=book_data['description'], 
            year=book_data['year'], 
            publisher=book_data['publisher'], 
            author=book_data['author'], 
            pages=book_data['pages'], 
            cover_id=book_data['cover_id']
        )
        db.session.add(book)
    db.session.commit()

def assign_genres_to_books():
    genre_fiction = Genre.query.filter_by(name='Фантастика').first()
    genre_science = Genre.query.filter_by(name='Наука').first()
    genre_biography = Genre.query.filter_by(name='Биография').first()
    genre_fantasy = Genre.query.filter_by(name='Фэнтези').first()
    
    book_gatsby = Book.query.filter_by(title='Великий Гэтсби').first()
    book_mockingbird = Book.query.filter_by(title='Убить пересмешника').first()
    
    book_gatsby.genres.append(genre_fiction)
    book_mockingbird.genres.append(genre_fiction)
    book_mockingbird.genres.append(genre_biography)
    
    db.session.commit()

def main():
    db.drop_all()
    db.create_all()
    create_roles()
    create_users()
    create_genres()
    common_cover = create_cover()
    create_books(common_cover)
    assign_genres_to_books()

if __name__ == "__main__":
    main()
