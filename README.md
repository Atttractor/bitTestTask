##Старт
Есть два режима работы программы:
    - В консоли
    - В браузере
Для запуска в консоли нужно:
Создать виртуальное окружение
```
python3 -m venv myenv
```
Активировать виртуальное окружение
Windows:
```
myenv\Scripts\activate
```
MacOS и Linux:
```
source myenv/bin/activate
```
Установить зависимости
```
pip install --upgrade -r requirements.txt
```
Затем просто запустить console/main.py

Для запуска в браузере:
```
docker compose up --build -d
```
Перейти на localhost:8000


База находится на localhost:5433
App находится на localhost:8000
Методы API можно псмотреть на localhost::8000/docs
