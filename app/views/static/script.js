function toggleDivVisibility(id) {
    var el = document.getElementById(id);
    if (el.style.display === 'none') {
        el.style.display = 'block'
    } else {
        el.style.display = 'none'
    }
}

BACK_BUF = ''

document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#btn-reports').addEventListener('click', () => {
        toggleDivVisibility('start-btns')
        toggleDivVisibility('back')
        reports = document.getElementById('reports')
        if (reports.style.display === 'none') {
            reports.style.display = 'flex'
        } else {
            reports.style.display = 'none'
        }
        BACK_BUF = 'start'
    })

    document.querySelector('#btn-fact').addEventListener('click', () => {
        BACK_BUF = 'start'
        document.getElementById('get-return-btns').style.display = 'block'
        toggleDivVisibility('back')
        toggleDivVisibility('start-btns')
    })

    document.querySelector('#btn-crud').addEventListener('click', () => {
        BACK_BUF = 'start'
        document.getElementById('crud-btns').style.display = 'grid'
        toggleDivVisibility('back')
        toggleDivVisibility('start-btns')
    })
    // Кнопка 'Назад'
    document.querySelector('#back').addEventListener('click', () => {
        if (BACK_BUF === 'start') {
            document.getElementById('start-btns').style.display = 'block'
            toggleDivVisibility('back')

            divs = document.querySelector('body').querySelectorAll('div')
            for (let i = 0; i < divs.length; i += 1) {
                if (divs[i].id !== 'start-btns') {
                    divs[i].style.display = 'none'
                }
            }
        } else if (BACK_BUF == 'reports') {
            BACK_BUF = 'start'
            document.getElementById('reports').style.display = 'flex'
            divs = document.querySelector('body').querySelectorAll('div')
            for (let i = 0; i < divs.length; i += 1) {
                if (divs[i].id !== 'reports') {
                    divs[i].style.display = 'none'
                }
            }
        } else if (BACK_BUF == 'crud') {
            BACK_BUF = 'start'
            document.getElementById('crud-btns').style.display = 'grid'
            divs = document.querySelector('body').querySelectorAll('div')
            for (let i = 0; i < divs.length; i += 1) {
                if (divs[i].id !== 'crud-btns') {
                    divs[i].style.display = 'none'
                }
            }
        }
        else if (BACK_BUF == 'get-return') {
            BACK_BUF = 'start'
            document.getElementById('get-return-btns').style.display = 'block'
            divs = document.querySelector('body').querySelectorAll('div')
            for (let i = 0; i < divs.length; i += 1) {
                if (divs[i].id !== 'get-return-btns') {
                    divs[i].style.display = 'none'
                }
            }
        }
    })

    // Запросы к API отчётов
    document.querySelector('#report-1').addEventListener('click', async () => {
        const response = await fetch('/count_of_books', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }

        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'
        
        one_item = document.querySelector('#one-item')
        one_item.querySelector('#name-of-item').innerText = 'Количество свободных книг в библиотеке:'
        one_item.querySelector('#value-of-item').innerText = data

        one_item.style.display = 'block'
    })
    document.querySelector('#report-2').addEventListener('click', async () => {
        const response = await fetch('/users_takes_books_all_time', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }

        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'

        many_items = document.querySelector('#many-items')
        many_items.innerHTML = 'Каждый читатель брал столько книг за всё время:</h1>'
        for (let i = 0; i < data.length; i++) {
            many_items.innerHTML += '<h3>' + data[i][0] + ' : ' + data[i][1] + '</h3>'
        }

        many_items.style.display = 'block'
    })
    document.querySelector('#report-3').addEventListener('click', async () => {
        const response = await fetch('/users_have_books', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }

        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'

        many_items = document.querySelector('#many-items')
        many_items.innerHTML = 'У каждого читателя сейчас столько книг:</h1>'
        for (let i = 0; i < data.length; i++) {
            many_items.innerHTML += '<h3>' + data[i][0] + ' : ' + data[i][1] + '</h3>'
        }

        many_items.style.display = 'block'
    })
    document.querySelector('#report-4').addEventListener('click', async () => {
        const response = await fetch('/last_visit_date', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }

        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'
        
        one_item = document.querySelector('#one-item')
        one_item.querySelector('#name-of-item').innerText = 'Дата последнего посещения библиотеки:'
        one_item.querySelector('#value-of-item').innerText = data

        one_item.style.display = 'block'
    })
    document.querySelector('#report-5').addEventListener('click', async () => {
        const response = await fetch('/best_genres_by_desc', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }
        console.log(data)
        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'

        many_items = document.querySelector('#many-items')
        many_items.innerHTML = '<h1>Наиболее популярные жанры (по убыванию):</h1>'
        for (let i = 0; i < data.length; i++) {
            many_items.innerHTML += '<h3>' + data[i][0] + '</h3>'
        }

        many_items.style.display = 'block'
    })
    document.querySelector('#report-6').addEventListener('click', async () => {
        const response = await fetch('/overdue_books', {
            method: "GET", 
            cache: "no-cache",
        });
        if (response.ok) {
            data = await response.json();
            data = data['data']
        } else {
            alert("Ошибка HTTP: " + response.status);
        }
        console.log(data)
        document.getElementById('reports').style.display = 'none'
        BACK_BUF = 'reports'

        many_items = document.querySelector('#many-items')
        many_items.innerHTML = '<h1>Читатели не вернувшие книги вовремя и книги которые они не вернули:</h1>'
        for (let i = 0; i < data.length; i++) {
            many_items.innerHTML += '<h3>' + data[i][1] + ' : ' + data[i][3] + '</h3>'
        }

        many_items.style.display = 'block'
    })

    // Запросы к API CRUD книг и пользователей
    // Создать юзера
    document.querySelector('#c-user').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Имя</p><input type="text" name="name" maxlength="64" required>
                        <p>Адрес</p><input type="text" name="address" maxlength="128" required>
                        <p>Номер телефона в формате (89000000000)</p><input type="text" name="phone_number" maxlength="11" required>
                        <p>email</p><input type="email" name="email" maxlength="64" required>
                        <input type="submit" value="Создать">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            const response = await fetch('/create_user', {
                method: 'POST',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    // Удалить юзера
    document.querySelector('#d-user').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Id пользователя</p><input type="number" min="0" name="id" required>
                        <input type="submit" value="Удалить">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.id = +jsonData.id
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/delete_user', {
                method: 'DELETE',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    // Изменить юзера
    document.querySelector('#u-user').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Id пользователя</p><input type="number" min="0" name="id" required>
                        <p>Имя</p><input type="text" name="name" maxlength="64" required>
                        <p>Адрес</p><input type="text" name="address" maxlength="128" required>
                        <p>Номер телефона в формате (89000000000)</p><input type="text" name="phone_number" maxlength="11" required>
                        <p>email</p><input type="email" name="email" maxlength="64" required>
                        <input type="submit" value="Изменить">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.id = +jsonData.id
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/edit_user', {
                method: 'PUT',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    // Создать книгу
    document.querySelector('#c-book').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Название</p><input type="text" name="name" maxlength="64" required>
                        <p>Количество</p><input type="number" name="count_in_library" min="1" required>
                        <input type="submit" value="Создать">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.id = +jsonData.count_in_library
            jsonData.authors = []
            jsonData.genres = []
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/create_book', {
                method: 'POST',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    // Изменить книгу
    document.querySelector('#u-book').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Id книги</p><input type="number" name="id" min="0" required>
                        <p>Название</p><input type="text" name="name" maxlength="64" required>
                        <p>Количество</p><input type="number" name="count_in_library" min="1" required>
                        <input type="submit" value="Изменить">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.id = +jsonData.id
            jsonData.count_in_library = +jsonData.count_in_library
            jsonData.authors = []
            jsonData.genres = []
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/edit_book', {
                method: 'PUT',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    // Изменить книгу
    document.querySelector('#d-book').addEventListener('click', async () => {
        BACK_BUF = 'crud'
        document.getElementById('crud-btns').style.display = 'none'
        let form = `<form id="form1" method="POST">
                        <p>Id книги</p><input type="number" name="id" min="0" required>
                        <input type="submit" value="Удалить">
                    </form>`
        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.id = +jsonData.id
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/delete_book', {
                method: 'DELETE',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        });
    })
    

    // Запросы к на взятие/возвращение книги
    // взять книгу
    document.querySelector('#get-btn').addEventListener('click', () => {
        BACK_BUF = 'get-return'
        document.getElementById('get-return-btns').style.display = 'none'

        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'

        let form = `<form id="form1" method="POST">
                        <p>Id юзера</p><input type="number" min="0" name="user_id" required>
                        <p>Id книги</p><input type="number" min="0" name="book_id" required>
                        <p>На сколько дать (в днях)</p><input type="number" min="0" name="interval" required>
                        <input type="submit" value="Дать книгу">
                    </form>`
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));

            jsonData = JSON.parse(jsonData)
            jsonData.user_id = +jsonData.user_id
            jsonData.book_id = +jsonData.book_id
            jsonData.interval = +jsonData.interval
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/get_book', {
                method: 'POST',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        })
    })
    // вернуть книгу
    document.querySelector('#return-btn').addEventListener('click', () => {
        BACK_BUF = 'get-return'
        document.getElementById('get-return-btns').style.display = 'none'

        let fd = document.querySelector('#form-div')
        fd.style.display = 'flex'

        let form = `<form id="form1" method="POST">
                        <p>Id юзера</p><input type="number" min="0" name="user_id" required>
                        <p>Id книги</p><input type="number" min="0" name="book_id" required>
                        <input type="submit" value="Забрать книгу">
                    </form>`
        fd.innerHTML = form

        form = document.getElementById('form1')
        form.addEventListener('submit', async (e) => {
            e.preventDefault()

            const formDataToJson = (formData) => JSON.stringify(Object.fromEntries(formData));
            let jsonData = formDataToJson(new FormData(form));
            
            jsonData = JSON.parse(jsonData)
            jsonData.user_id = +jsonData.user_id
            jsonData.book_id = +jsonData.book_id
            jsonData = JSON.stringify(jsonData)

            const response = await fetch('/return_book', {
                method: 'POST',
                body: jsonData,
                headers: {'content-type': 'application/json'}
            })
            .then((response) => {
                if (response.ok) {
                    response.text().then((text) => alert(text))
                }
            })
            .catch((error) => {
                alert("Ошибка сервера: " + error);
            });
        })
    })
})