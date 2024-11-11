import psycopg2
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.db.isert_values import run_insert

BASE_DIR = Path(__file__).resolve().parent

from app.models import *

app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'views')))
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, 'views/static'))), name="static")

test_conn = psycopg2.connect(
        host="pg_db",
        database="library",
        user="library_user",
        password="library_password",
        port="5432"
    )

cur = test_conn.cursor()

try:
    cur.execute('select * from author')
except psycopg2.errors.UndefinedTable:
    run_insert()


test_conn.close()


CONN = psycopg2.connect(
        host="pg_db", # название контейнера с бд
        database="library",
        user="library_user",
        password="library_password",
        port="5432" # порт внутри контейнера с бд
    )

cur = CONN.cursor()

# Роут с фронтендом
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    cur = CONN.cursor()
    cur.execute("select * from book")
    books = cur.fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

# Далее идут 6 роутов с отчётами
@app.get("/count_of_books", summary='Cколько свободных книг есть в библиотеке на текущий момент', tags=["Отчёты"])
def count_of_books():
    cur = CONN.cursor()
    cur.execute("select sum(count_in_library) from book where count_in_library > 0")
    return {"data": cur.fetchall()[0][0]}

@app.get("/users_takes_books_all_time", summary='Сколько книг брал каждый читатель за все время', tags=["Отчёты"])
def users_takes_books_all_time():
    cur = CONN.cursor()
    cur.execute("select name, count(*) from public.user join public.user_has_book on user_has_book.user_id = public.user.id group by name")
    return {"data": cur.fetchall()}

@app.get("/users_have_books", summary='Сколько книг сейчас находится на руках у каждого читателя', tags=["Отчёты"])
def users_have_books():
    cur = CONN.cursor()
    cur.execute("select name, count(*) from public.user join public.user_has_book on (user_has_book.user_id = public.user.id and returned = False) group by name")
    return {"data": cur.fetchall()}

@app.get("/last_visit_date", summary='Дата последнего посещения читателем библиотеки', tags=["Отчёты"])
def last_visit_date():
    cur = CONN.cursor()
    cur.execute("select max(date_of_taken) from user_has_book")
    return {"data": cur.fetchall()}

@app.get("/best_genres_by_desc", summary='Наиболее предпочитаемые читателями жанры по убыванию', tags=["Отчёты"])
def best_genres_by_desc():
    cur = CONN.cursor()
    cur.execute("select genre.name, count(genre.name) from user_has_book "
                "join book on book.id = user_has_book.book_id "
                "join book_genre on book.id = book_genre.book_id "
                "join genre on genre.id = genre_id group by genre.name order by count desc")
    return {"data": cur.fetchall()}

@app.get("/overdue_books", summary='Наиболее предпочитаемые читателями жанры по убыванию', tags=["Отчёты"])
def overdue_books():
    cur = CONN.cursor()
    cur.execute("select public.user.id, public.user.name, book.id, book.name from user_has_book "
                "join public.user on public.user.id = user_id "             
                "join public.book on public.book.id = book_id "
                "where (date (date_of_taken + rental_duration) < now() and returned = False)")
    return {"data": cur.fetchall()}

# Роут для создания книги (НЕ СОВСЕМ ДОДЕЛАН)
@app.post("/create_book", summary='Создать книгу', tags=["Книги"])
def create_book(data: CreateBookModel):
    cur = CONN.cursor()

    name = data.name
    count_in_library = data.count_in_library

    # Времени оставалось мало, когда я понял, что это узкое место
    genres = data.genres
    authors = data.authors

    cur.execute(f"insert into public.book (name, count_in_library) values ('{name}', {count_in_library});")
    CONN.commit()
    return "Книга создана"

# Роут для изменения книги
@app.put("/edit_book", summary='Изменить книгу', tags=["Книги"])
def edit_book(data: EditBookModel):
    cur = CONN.cursor()

    book_id = data.id
    name = data.name
    count_in_library = data.count_in_library

    cur.execute(f"select * from public.book where id = {book_id}")
    if not cur.fetchall():
        return "Книга не найдена"

    cur.execute(f"update public.book set name = '{name}', count_in_library = {count_in_library} where id = {book_id}")
    CONN.commit()
    return "Книга изменена"

# Роут для удаления книги
@app.delete("/delete_book", summary='Удалить книгу', tags=["Книги"])
def delete_book(data: DeleteModel):
    cur = CONN.cursor()

    book_id = data.id

    cur.execute(f"delete from public.book where id = {book_id};")
    CONN.commit()
    return "Книга удалена"

# Роут для создания юзера
@app.post("/create_user", summary='Создать пользователя', tags=["Пользователи"])
def create_user(data: CreateUserModel):
    cur = CONN.cursor()

    name = data.name
    address = data.address
    phone_number = data.phone_number
    email = data.email

    cur.execute(f"insert into public.user (name, address, phone_number, email) values "
                f"('{name}', '{address}', '{phone_number}', '{email}');")
    CONN.commit()
    return "Пользователь сохранён"

# Роут для изменения юзера
@app.put("/edit_user", summary='Изменить пользователя', tags=["Пользователи"])
def edit_user(data: EditUserModel):
    cur = CONN.cursor()

    user_id = data.id
    name = data.name
    address = data.address
    phone_number = data.phone_number
    email = data.email

    cur.execute(f"select * from public.user where id = {user_id}")
    if not cur.fetchall():
        return "Пользователь не найден"

    cur.execute(f"update public.user set name = '{name}', address = '{address}', phone_number = '{phone_number}', email = '{email}' where id = {user_id}")
    CONN.commit()
    return "Пользователь изменён"

# Роут для удаления юзера
@app.delete("/delete_user", summary='Удалить пользователя', tags=["Пользователи"])
def delete_user(data: DeleteModel):
    cur = CONN.cursor()

    user_id = data.id

    cur.execute(f"delete from public.user where public.user.id = {user_id};")
    CONN.commit()
    return "Пользователь удалён"

# Роут для аренды книги
@app.post("/get_book", summary='Дать книгу', tags=["Взять или вернуть книгу"])
def get_book(data: GetBook):
    cur = CONN.cursor()

    user_id = data.user_id
    book_id = data.book_id
    interval = data.interval

    cur.execute(f"select * from user_has_book where (book_id = {book_id} and user_id = {user_id} and returned = False)")
    data = cur.fetchall()
    if len(data) > 0:
        print('Этот пользователь ещё не вернул старую книгу')
        return "Этот пользователь ещё не вернул старую книгу"

    cur.execute(
        f"insert into public.user_has_book (user_id, book_id, rental_duration) values ({user_id}, {book_id}, '{interval} days')"
    )
    cur.execute(f"select count_in_library from book where book.id = {book_id}")
    count_in_library = cur.fetchall()[0][0]
    cur.execute(f"update public.book set count_in_library = {count_in_library - 1} where id = {book_id}")
    CONN.commit()
    return "OK"

# Роут для возвращения книги
@app.post("/return_book", summary='Забрать книгу', tags=["Взять или вернуть книгу"])
def return_book(data: ReturnBook):
    cur = CONN.cursor()

    user_id = data.user_id
    book_id = data.book_id

    # Проверка, что пользователь вообще брал книгу перед тем как вернуть
    cur.execute(f"select * from user_has_book where (book_id = {book_id} and user_id = {user_id})")
    data = cur.fetchall()

    if len(data) < 1:
        print('Этот пользователь не брал данную книгу!!!')
        return "Этот пользователь не брал данную книгу!!!"
    elif len(data) == 1:
        if data[0][5]:
            print('Этот пользователь уже вернул книгу!!!')
            return "Этот пользователь уже вернул книгу!!!"
    elif len(data) > 1:
        data = sorted(data, key=lambda x: x[5])[0]
        user_id = data[1]
        book_id = data[2]
    else:
        print('Что-то пошло не по плану')
        return "Что-то пошло не по плану"

    cur.execute(f"select count_in_library from book where book.id = {book_id}")
    count_in_library = cur.fetchall()[0][0]

    cur.execute(f"update public.book set count_in_library = {count_in_library + 1} where id = {book_id}")
    cur.execute(f"update public.user_has_book set returned = True where (book_id = {book_id} and user_id = {user_id})")
    CONN.commit()
    return "OK"