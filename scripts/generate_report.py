#!/usr/bin/env python3
"""Generate OTCHET_PRACTIKA.docx from markdown content."""

try:
    from docx import Document
    from docx.shared import Pt, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    print("Install: pip install python-docx")
    raise

doc = Document()

style = doc.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(12)

def heading(text, level=1):
    doc.add_heading(text, level=level)

def para(text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p

def table(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = "Table Grid"
    for i, h in enumerate(headers):
        t.rows[0].cells[i].text = h
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            t.rows[ri + 1].cells[ci].text = str(cell)
    doc.add_paragraph()

# Title
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("ОТЧЁТ ПО ПРАКТИКЕ\nВеб-разработка — Simple Weather App")
r.bold = True
r.font.size = Pt(14)

doc.add_paragraph()
para("Студент: _________________________________")
para("Группа: _________________________________")
para("Дата сдачи: _________________________________")
doc.add_paragraph()

heading("5.1 Выбранный проект", 1)
heading("Название проекта", 2)
para("Simple Weather App — приложение погоды на Vanilla JavaScript")

heading("Ссылка на проект из каталога", 2)
para("https://webdesign.tutsplus.com/build-a-simple-weather-app-with-vanilla-javascript--cms-33893t")

heading("Краткое описание", 2)
para(
    "Одностраничное веб-приложение для поиска текущей погоды в городах мира. "
    "Пользователь вводит название города, приложение запрашивает OpenWeatherMap API "
    "и отображает карточку с температурой, иконкой и описанием."
)

heading("Что реализовано / доработано", 2)
para("По туториалу: HTML-разметка, CSS Grid, Fetch API, кастомные иконки, защита от дубликатов.")
para("Доработки: localStorage, удаление карточек, Express-сервер для Railway, Code Climate.")

heading("5.2 Технический паспорт проекта", 1)
table(
    ["Параметр", "Значение"],
    [
        ["GitHub", "https://github.com/YOUR_USERNAME/simple-weather-app"],
        ["Деплой (Railway)", "https://YOUR-APP.up.railway.app"],
        ["Каталог", "https://webdesign.tutsplus.com/build-a-simple-weather-app-with-vanilla-javascript--cms-33893t"],
        ["Frontend", "HTML5, CSS3, Vanilla JavaScript"],
        ["Backend", "Node.js 18+, Express 4"],
        ["БД", "localStorage (клиент)"],
        ["API", "OpenWeatherMap Current Weather v2.5"],
        ["Авторизация", "Отсутствует"],
    ],
)

heading("5.3 Архитектура", 1)
heading("Схема", 2)
para(
    "Браузер (HTML/CSS/JS + localStorage) → Railway (Express server.js) → OpenWeatherMap API. "
    "API-ключ передаётся через endpoint /config.js из переменной OPENWEATHER_API_KEY."
)

heading("ERD", 2)
para("localStorage.weatherAppCities: массив объектов { key: string, data: WeatherResponse }.")
para("WeatherResponse: name, sys.country, main.temp, weather[0].icon/main/description.")

heading("Use Case", 2)
table(
    ["UC", "Сценарий", "Результат"],
    [
        ["UC-1", "Поиск погоды по городу", "Карточка добавлена в список"],
        ["UC-2", "Повторный поиск того же города", "Сообщение о дубликате, без API-запроса"],
        ["UC-3", "Удаление карточки", "Город удалён из DOM и localStorage"],
        ["UC-4", "Перезагрузка страницы", "Список восстановлен из localStorage"],
    ],
)

heading("API", 2)
para("GET https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric")
para("Документация: https://openweathermap.org/current")

heading("5.4 Таблица соответствия", 1)
table(
    ["Функция", "GitHub", "Деплой"],
    [
        ["Форма поиска", "index.html", "Главная — форма"],
        ["Стили и Grid", "css/styles.css", "Главная — карточки"],
        ["Fetch API", "js/app.js", "Поиск города → SUBMIT"],
        ["Карточка города", "js/app.js", "Карточка после поиска"],
        ["Дубликаты", "js/app.js", "Повторный London"],
        ["localStorage", "js/app.js", "F5 после добавления"],
        ["Удаление", "js/app.js", "Кнопка Удалить"],
        ["Сервер", "server.js", "/config.js"],
    ],
)

heading("5.5 Демонстрация работы", 1)
para("Формат: GIF / видео / asciinema (до 2 мин).")
para("Сценарий: London → Paris → дубликат London → удалить Paris → F5.")
para("Ссылка на демо: _______________________________________________")

heading("5.6 Качество кода", 1)
para("Code Climate: подключить репозиторий, оценка A или B. Бейдж в README.md.")
para("Конфигурация: .codeclimate.yml, .eslintrc.json")

heading("5.7 Вывод по практике", 1)
para(
    "Реализовано SPA-приложение погоды по туториалу Envato Tuts+ с доработками: "
    "localStorage, удаление карточек, деплой на Railway. "
    "Освоены Fetch API, CSS Grid, работа с внешним REST API, деплой Node.js-приложения."
)
para(
    "Сложности: адаптация устаревшего API, безопасное хранение ключа через env. "
    "Дальнейшие улучшения: геолокация, прогноз на 5 дней, backend-прокси для API."
)

out = "docs/OTCHET_PRACTIKA.docx"
doc.save(out)
print(f"Saved: {out}")
