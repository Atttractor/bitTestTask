import random
import psycopg2
from pathlib import Path

CONN = psycopg2.connect(
        host="pg_db",
        database="library",
        user="library_user",
        password="library_password",
        port="5432"
)

GENRES_LIST = [f'Genre {i}' for i in range(1, 10)]
AUTHORS_LIST = [f'Author {i}' for i in range(1, 15)]
BOOKS_LIST = [(f'Book {i}',
                  {
                      'Authors': [random.choice(AUTHORS_LIST) for _ in range(2)],
                      'Genres': [random.choice(GENRES_LIST) for _ in range(3)]
                  }) for i in range(1, 25)]
USERS = [
    {
        'Name': f'User {i}',
        'Address': 'Address',
        'phone_number': f'{random.randint(89000000000, 89999999999)}',
        # ord('a') - 97, ord('z') - 122
        'email': f'{''.join([chr(random.randint(97, 122)) for _ in range(10)])}@{random.choice(['ya', 'yandex', 'gmail'])}.ru',
        'books': [random.choice(BOOKS_LIST)[0] for _ in range(random.randint(1, 4))]
    } for i in range(1, 20)]

def insert_books_genres_authors_users():
    cur = CONN.cursor()

    s = ''
    for genre in GENRES_LIST:
        s +=  f"('{genre}'), "
    s = s[:-2] + ';'
    cur.execute(f"insert into public.genre (name) values {s}")

    s = ''
    for author in AUTHORS_LIST:
        s += f"('{author}'), "
    s = s[:-2] + ';'
    cur.execute(f"insert into public.author (name) values {s}")

    s = ''
    for book in BOOKS_LIST:
        s += f"('{book[0]}', {random.randint(5, 15)}), "
    s = s[:-2] + ';'
    cur.execute(f"insert into public.book (name, count_in_library) values {s}")

    s = ''
    for user in USERS:
        s += f"('{user['Name']}', '{user['Address']}', '{user['phone_number']}', '{user['email']}'), "
    s = s[:-2] + ';'
    cur.execute(f"insert into public.user (name, address, phone_number, email) values {s}")

    CONN.commit()
    cur.close()


def make_relations():
    cur = CONN.cursor()

    cur.execute("select id, name from public.genre;")
    genres = cur.fetchall()
    genres = {genre[1]: genre[0] for genre in genres}

    cur.execute("select id, name from public.author;")
    authors = cur.fetchall()
    authors = {author[1]: author[0] for author in authors}

    cur.execute("select id, name from public.user;")
    users = cur.fetchall()
    users = {user[1]: user[0] for user in users}

    cur.execute("select * from public.book;")
    books = cur.fetchall()
    books = {book[1]: (book[0], book[1]) for book in books}

    s_book_author = ''
    s_book_genre = ''
    for book in BOOKS_LIST:
        book_id = books[book[0]][0]
        for author in book[1]['Authors']:
            s_book_author += f"({book_id}, {authors[author]}), "
        for genre in book[1]['Genres']:
            s_book_genre += f"({book_id}, {genres[genre]}), "
    s_book_genre = s_book_genre[:-2] + ';'
    s_book_author = s_book_author[:-2] + ';'

    cur.execute(f"insert into public.book_genre (book_id, genre_id) values {s_book_genre}\n"
                f"insert into public.book_author (book_id, author_id) values {s_book_author}")

    s = ''
    for user in USERS:
        user_id = users[user['Name']]
        for book in user['books']:
            s += f"({user_id}, {books[book][0]}), "
    s = s[:-2] + ';'

    cur.execute(f"insert into public.user_has_book (user_id, book_id) values {s}")

    CONN.commit()
    cur.close()


def create_db(url):
    cur = CONN.cursor()

    bas_dir = Path(__file__).resolve().parent
    print(bas_dir)

    with open(str(Path(bas_dir, url)), 'r') as f:
        cur.execute(f.read())
        f.close()

    CONN.commit()
    cur.close()

def run_insert():
    create_db('schema.sql')
    insert_books_genres_authors_users()
    make_relations()

    CONN.close()