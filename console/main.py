import psycopg2

from console.isert_values import run_insert


# Функция для удобного выбора опций
def get_option(question='Что хотите сделать?', answers=None, interval=False):
    if interval:
        while True:
            try:
                number_of_days = int(input('Введите интервал (в днях)\n'))
            except ValueError:
                print('Нужно ввести число')
                continue
            return number_of_days
    if answers is None:
        answers = ['Добавить Факт взятия/возврата книги', 'Просмотр отчетов', 'Закончить работу']
    s = '\n'.join([f'{i + 1}) {answers[i]}' for i in range(len(answers))])
    while True:
        option = 0
        while option < 1 or option > len(answers):
            try:
                option = int(
                    input(f'{question}\n{s}\n')
                )
            except ValueError:
                print('Выберите существующую опцию')
                continue
            if option < 1 or option > len(answers):
                print('Выберите существующую опцию')
                continue
        return option


def main():
    conn = psycopg2.connect(
        host="localhost",
        database="library",
        user="library_user",
        password="library_password",
        port="5433"
    )

    cur = conn.cursor()

    while True:
        option = get_option()
        if option == 1:
            cur.execute("select * from public.user")
            users = cur.fetchall()
            cur.execute("select * from public.book where count_in_library > 0")
            books = cur.fetchall()

            user = users[get_option('Выберите пользователя', [i[1] for i in users]) - 1]
            book = books[get_option('Выберите книгу', [i[1] for i in books]) - 1]

            action = get_option('Взял или вернул', ['Взял', 'Вернул'])
            if action == 1:
                # Тут надо проверить не брал ли пользователь такую же книгу ранее
                cur.execute(f"select * from user_has_book where (book_id = {book[0]} and user_id = {user[0]} and returned = False)")
                data = cur.fetchall()
                if len(data) > 0:
                    print('Этот пользователь ещё не вернул старую книгу\n')
                    continue

                interval = get_option('На сколько хотите дать книгу(в днях)?', interval=True)
                cur.execute(
                    f"insert into public.user_has_book (user_id, book_id, rental_duration) values ({user[0]}, {book[0]}, '{interval} days')"
                )
                cur.execute(f"update public.book set count_in_library = {book[2] - 1} where id = {book[0]}")
            elif action == 2:
                # Проверка, что пользователь вообще брал книгу перед тем как вернуть
                cur.execute(f"select * from user_has_book where (book_id = {book[0]} and user_id = {user[0]})")
                data = cur.fetchall()

                book_id = book[0]
                user_id = user[0]
                if len(data) < 1:
                    print('Этот пользователь не брал данную книгу!!!\n')
                    continue
                elif len(data) == 1:
                    if data[0][5]:
                        print('Этот пользователь уже вернул книгу!!!\n')
                        continue
                elif len(data) > 1:
                    data = sorted(data, key=lambda x: x[5])[0]
                    user_id = data[1]
                    book_id = data[2]
                else:
                    print('Что-то пошло не по плану')
                    break

                cur.execute(f"update public.book set count_in_library = {book[2] + 1} where id = {book_id}")
                cur.execute(f"update public.user_has_book set returned = True where (book_id = {book_id} and user_id = {user_id})")

            conn.commit()
        elif option == 2:
            option = get_option('Выберите отчёт', [
                'Cколько свободных книг есть в библиотеке на текущий момент',
                'Сколько книг брал каждый читатель за все время',
                'Сколько книг сейчас находится на руках у каждого читателя',
                'Дата последнего посещения читателем библиотеки',
                'Наиболее предпочитаемые читателями жанры по убыванию',
                'Читатели и книги которые они не вернули вовремя'
            ])

            queries = {
                1: {
                    'query': "select sum(count_in_library) from book where count_in_library > 0",
                    'answer': lambda x: f"Свободных книг в библиотеке: {x[0][0]}"
                },
                2: {
                    'query': "select name, count(*) from public.user join public.user_has_book on user_has_book.user_id = public.user.id group by name",
                    'answer': lambda x: f"Столько книг брал каждый читатель за всё время:\n{'\n'.join([f'{i[0]}: {i[1]}' for i in x])}"
                },
                3: {
                    'query': "select name, count(*) from public.user join public.user_has_book on (user_has_book.user_id = public.user.id and returned = False) group by name",
                    'answer': lambda x: f"Сейчас на руках у каждого читателя находится столько книг:\n{'\n'.join([f'{i[0]}: {i[1]}' for i in x])}"
                },
                4: {
                    'query': "select max(date_of_taken) from user_has_book",
                    'answer': lambda x: f"Дата последнего посещения библиотеки: {x[0][0]}"
                },
                5: {
                    'query': "select genre.name, count(genre.name) from user_has_book "
                             "join book on book.id = user_has_book.book_id "
                             "join book_genre on book.id = book_genre.book_id "
                             "join genre on genre.id = genre_id group by genre.name order by count desc",
                    'answer': lambda x: f"Наиболее предпочитаемые читателями жанры (по убыванию):\n{'\n'.join([i[0] for i in x])}"
                },
                6: {
                    'query': "select public.user.id, public.user.name, book.id, book.name from user_has_book "
                             "join public.user on public.user.id = user_id "
                             "join public.book on public.book.id = book_id "
                             "where (date (date_of_taken + rental_duration) < now() and returned = False)",
                    'answer': lambda x: f"Читатели не вернувшие книги вовремя и"
                                        f" книги которые они не вернули:\n{'\n'.join([f'{i[1]} - {i[3]}' for i in x])}"
                },
            }

            cur.execute(queries[option]['query'])
            data = cur.fetchall()
            print(queries[option]['answer'](data))
        elif option == 3:
            print('Завершение работы')
            break
        else:
            print('Выберите опцию 1, 2 или 3')
        print()

    cur.close()
    conn.close()

if  __name__ == '__main__':
    test_conn = psycopg2.connect(
        host="localhost",
        database="library",
        user="library_user",
        password="library_password",
        port="5433"
    )

    cur = test_conn.cursor()

    try:
        cur.execute('select * from author')
    except psycopg2.errors.UndefinedTable:
        run_insert()

    cur.close()
    test_conn.close()

    main()