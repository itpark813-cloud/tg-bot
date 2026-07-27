import telebot
from telebot import types
import time
import random

TOKEN = '8715699108:AAHShcE6CXS0oJDtS3pQT6LLtc2oIVN59Xg'
bot = telebot.TeleBot(TOKEN)

# Хранилище данных пользователей
user_notes = {}
user_state = {}

# ------------------- БАЗА КУРСА ПО FRONTEND (10 УРОКОВ) -------------------

FRONTEND_COURSE = {
    "1": {
        "title": "⬛ Урок 1: HTML5 & Семантика",
        "text": (
            "<b>⬛ УРОК 1: HTML5 & СЕМАНТИКА</b>\n\n"
            "HTML — это скелет веб-страницы. Семантика важна для SEO и доступности (A11y).\n\n"
            "<b>Забудьте про кучу <code>&lt;div&gt;</code>! Используйте смысловые теги:</b>\n"
            "• <code>&lt;header&gt;</code> — шапка сайта\n"
            "• <code>&lt;nav&gt;</code> — навигация и меню\n"
            "• <code>&lt;main&gt;</code> — главный уникальный контент\n"
            "• <code>&lt;section&gt;</code> — логический блок / секция\n"
            "• <code>&lt;article&gt;</code> — самостоятельный блок (статья, карточка)\n"
            "• <code>&lt;footer&gt;</code> — подвал сайта\n\n"
            "<b>💡 Пример правильной структуры:</b>\n"
            "<code>&lt;main&gt;\n"
            "  &lt;article class=\"card\"&gt;\n"
            "    &lt;h2&gt;Заголовок&lt;/h2&gt;\n"
            "    &lt;p&gt;Текст статьи...&lt;/p&gt;\n"
            "  &lt;/article&gt;\n"
            "&lt;/main&gt;</code>"
        )
    },
    "2": {
        "title": "⬜ Урок 2: CSS3 & Блочная модель (Box Model)",
        "text": (
            "<b>⬜ УРОК 2: CSS3 & BOX MODEL</b>\n\n"
            "Каждый элемент на странице — это прямоугольный бокс.\n\n"
            "<b>Состав Box Model:</b>\n"
            "1. <b>Content</b> — сам текст или картинка\n"
            "2. <b>Padding</b> — внутренний отступ (от контента до рамки)\n"
            "3. <b>Border</b> — рамка элемента\n"
            "4. <b>Margin</b> — внешний отступ (расстояние до соседних элементов)\n\n"
            "<b>🔥 Главное правило верстки:</b>\n"
            "Всегда добавляйте в начало CSS:\n"
            "<code>* {\n"
            "  box-sizing: border-box;\n"
            "}</code>\n"
            "Это делает так, чтобы <code>padding</code> и <code>border</code> не раздували ширину блока!"
        )
    },
    "3": {
        "title": "⬛ Урок 3: Flexbox — Магия выравнивания",
        "text": (
            "<b>⬛ УРОК 3: FLEXBOX</b>\n\n"
            "Flexbox решает 90% задач по раскладке элементов в одну линию или столбец.\n\n"
            "<b>Базовый шаблон:</b>\n"
            "<code>.container {\n"
            "  display: flex;\n"
            "  justify-content: space-between; /* Выравнивание по главной оси */\n"
            "  align-items: center; /* Выравнивание по поперечной оси */\n"
            "  gap: 20px; /* Отступы между дочерними элементами */\n"
            "}</code>\n\n"
            "💡 <i>Используйте Flexbox для шапки сайта, меню, карточек и центрирования!</i>"
        )
    },
    "4": {
        "title": "⬜ Урок 4: CSS Grid & Адаптивность",
        "text": (
            "<b>⬜ УРОК 4: CSS GRID & МЕДИАЗАПРОСЫ</b>\n\n"
            "Grid идеален для сложных двухмерных сеток (строки + столбцы).\n\n"
            "<b>Авто-адаптивная сетка карточек без медиазапросов:</b>\n"
            "<code>.grid-container {\n"
            "  display: grid;\n"
            "  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n"
            "  gap: 16px;\n"
            "}</code>\n\n"
            "<b>Адаптируем под телефоны через Media Queries:</b>\n"
            "<code>@media (max-width: 768px) {\n"
            "  .sidebar { display: none; }\n"
            "}</code>"
        )
    },
    "5": {
        "title": "⬛ Урок 5: Основы JavaScript (ES6+)",
        "text": (
            "<b>⬛ УРОК 5: ОСНОВЫ JAVASCRIPT</b>\n\n"
            "JavaScript оживляет ваш интерфейс.\n\n"
            "<b>Главные правила современного JS:</b>\n"
            "• Забудьте про <code>var</code>. Используйте <code>const</code> (по умолчанию) и <code>let</code> (если значение меняется).\n"
            "• Используйте стрелочные функции и методы массивов:\n\n"
            "<code>const users = ['Анна', 'Иван', 'Мария'];\n"
            "// Трансформация массива (map)\n"
            "const upperUsers = users.map(user => user.toUpperCase());\n"
            "console.log(upperUsers);</code>"
        )
    },
    "6": {
        "title": "⬜ Урок 6: DOM & События",
        "text": (
            "<b>⬜ УРОК 6: РАБОТА С DOM И СОБЫТИЯМИ</b>\n\n"
            "DOM (Document Object Model) — это представление HTML-страницы в виде дерева объектов в JS.\n\n"
            "<b>Пример клика по кнопке и смены класса:</b>\n"
            "<code>const btn = document.querySelector('.my-btn');\n"
            "const card = document.querySelector('.card');\n\n"
            "btn.addEventListener('click', () => {\n"
            "  card.classList.toggle('active');\n"
            "});</code>"
        )
    },
    "7": {
        "title": "⬛ Урок 7: Асинхронность & Fetch API",
        "text": (
            "<b>⬛ УРОК 7: ASYNC / AWAIT & FETCH</b>\n\n"
            "Фронтенд постоянно получает данные с сервера (API) в формате JSON.\n\n"
            "<b>Современный запрос к серверу:</b>\n"
            "<code>async function loadData() {\n"
            "  try {\n"
            "    const response = await fetch('https://api.example.com/data');\n"
            "    const data = await response.json();\n"
            "    console.log(data);\n"
            "  } catch (error) {\n"
            "    console.error('Ошибка загрузки:', error);\n"
            "  }\n"
            "}\n"
            "loadData();</code>"
        )
    },
    "8": {
        "title": "⬜ Урок 8: Git & GitHub для верстальщика",
        "text": (
            "<b>⬜ УРОК 8: GIT И КОМАНДНАЯ РАБОТА</b>\n\n"
            "Git — система контроля версий. Сохраняет историю вашего кода.\n\n"
            "<b>Базовый рабочий цикл в терминале:</b>\n"
            "1. <code>git init</code> — инициализация проекта\n"
            "2. <code>git add .</code> — подготовить все изменения к сохранению\n"
            "3. <code>git commit -m \"Добавил адаптивную шапку\"</code> — сохранить слепок кода\n"
            "4. <code>git push origin main</code> — отправить код на GitHub"
        )
    },
    "9": {
        "title": "⬛ Урок 9: Сборка проектов (Node.js, npm, Vite)",
        "text": (
            "<b>⬛ УРОК 9: ИНСТРУМЕНТЫ СБОРКИ & VITE</b>\n\n"
            "В современной разработке проекты собираются специальными сборщиками.\n\n"
            "<b>Быстрый старт проекта на Vite за 10 секунд:</b>\n"
            "1. Откройте терминал\n"
            "2. Выполните: <code>npm create vite@latest my-app</code>\n"
            "3. Перейдите в папку: <code>cd my-app</code>\n"
            "4. Установите зависимости: <code>npm install</code>\n"
            "5. Запустите сервер разработки: <code>npm run dev</code>"
        )
    },
    "10": {
        "title": "⬜ Урок 10: Старт в React.js & Деплой",
        "text": (
            "<b>⬜ УРОК 10: РЕАКТ И ДЕПЛОЙ</b>\n\n"
            "React — самый популярный UI-фреймворк в мире.\n\n"
            "<b>Базовый компонент React с состоянием (useState):</b>\n"
            "<code>import { useState } from 'react';\n\n"
            "function Counter() {\n"
            "  const [count, setCount] = useState(0);\n"
            "  return (\n"
            "    &lt;button onClick={() =&gt; setCount(count + 1)}&gt;\n"
            "      Кликов: {count}\n"
            "    &lt;/button&gt;\n"
            "  );\n"
            "}</code>\n\n"
            "🚀 <b>Где выложить готовый сайт бесплатно?</b>\n"
            "Vercel, Netlify или GitHub Pages."
        )
    }
}

# ------------------- КЛАВИАТУРЫ (ЧЕРНО-БЕЛЫЙ КОНТРАСТ) -------------------

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Кнопки со стильным контрастом черного и белого
    btn_course = types.KeyboardButton("🖤 💻 КУРС FRONTEND (10 УРОКОВ)")
    btn_focus = types.KeyboardButton("🤍 ⏱️ ФОКУС-ТАЙМЕР")
    btn_notes = types.KeyboardButton("🖤 📓 БЛОКНОТ")
    btn_style = types.KeyboardButton("🤍 ✒️ СТИЛИЗАТОР")
    btn_quotes = types.KeyboardButton("🖤 🎲 ЦИТАТА / ОРАКУЛ")
    
    markup.add(btn_course)
    markup.add(btn_focus, btn_notes)
    markup.add(btn_style, btn_quotes)
    return markup

def get_course_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Контрастные инлайн-кнопки (чередуются черные и белые индикаторы)
    for key, data in FRONTEND_COURSE.items():
        btn = types.InlineKeyboardButton(data["title"], callback_data=f"lesson_{key}")
        markup.add(btn)
        
    return markup

# ------------------- ОБРАБОТКА КОМАНД -------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "<b>┌───────────────────────────┐</b>\n"
        "<b>│   F R O N T E N D  D E V  │</b>\n"
        "<b>│     A C A D E M Y  v2.0   │</b>\n"
        "<b>└───────────────────────────┘</b>\n\n"
        "🖤 <b>Добро пожаловать в Академию Фронтенда!</b>\n\n"
        "Здесь ты пройдешь полный путь от HTML-тега до деплоя своего первого приложения на React.\n\n"
        "<b>Что внутри:</b>\n"
        "▪️ <b>10 полноценных практических уроков</b>\n"
        "▪️ <b>Инструменты продуктивности и фокуса</b>\n"
        "▪️ <b>Блокнот кода и стилизатор</b>\n\n"
        "Нажми кнопку ниже, чтобы начать обучение! ⤵️"
    )
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode="HTML", 
        reply_markup=get_main_keyboard()
    )

# ------------------- ОСНОВНОЕ МЕНЮ -------------------

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    chat_id = message.chat.id
    text = message.text

    # Обработка ожидаемого ввода
    if user_state.get(chat_id) == 'waiting_note':
        if chat_id not in user_notes:
            user_notes[chat_id] = []
        user_notes[chat_id].append(text)
        user_state[chat_id] = None
        bot.send_message(chat_id, f"🖤 <b>Заметка сохранена:</b>\n<code>{text}</code>", parse_mode="HTML")
        return

    if user_state.get(chat_id) == 'waiting_style':
        spaced_text = " ".join(list(text.upper()))
        formatted = (
            f"<b>▪️ Исходный текст:</b> <code>{text}</code>\n\n"
            f"<b>▪️ Стилизованный формат:</b>\n<code>{spaced_text}</code>\n\n"
            f"<b>▪️ В виде кода:</b>\n<code>{text}</code>"
        )
        user_state[chat_id] = None
        bot.send_message(chat_id, formatted, parse_mode="HTML")
        return

    # Навигация
    if text == "🖤 💻 КУРС FRONTEND (10 УРОКОВ)":
        msg = (
            "<b>░░░░░░░░░░░░░░░░░░░░░░░░░</b>\n"
            "  🎓 <b>ПОЛНЫЙ КУРС FRONTEND</b>\n"
            "<b>░░░░░░░░░░░░░░░░░░░░░░░░░</b>\n\n"
            "Выбери интересующий урок для изучения:"
        )
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=get_course_keyboard())

    elif text == "🤍 ⏱️ ФОКУС-ТАЙМЕР":
        markup = types.InlineKeyboardMarkup()
        btn_start = types.InlineKeyboardButton("▶️ Запустить 25 мин Помодоро", callback_data="start_pomodoro")
        markup.add(btn_start)
        msg = (
            "⏱️ <b>ФОКУС-ТАЙМЕР (25 МИНУТ)</b>\n\n"
            "Убери соцсети, завари чай/кофе и погрузись в код без отвлечений!"
        )
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)

    elif text == "🖤 📓 БЛОКНОТ":
        notes = user_notes.get(chat_id, [])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_add = types.InlineKeyboardButton("➕ Добавить", callback_data="add_note")
        btn_clear = types.InlineKeyboardButton("🗑 Очистить", callback_data="clear_notes")
        markup.add(btn_add, btn_clear)

        if not notes:
            notes_text = "<i>Ваш блокнот пуст.</i>"
        else:
            notes_text = "\n".join([f"▫️ <code>{i+1}.</code> {n}" for i, n in enumerate(notes)])

        msg = f"📓 <b>ВАШИ ЗАМЕТКИ КОДА:</b>\n\n{notes_text}"
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)

    elif text == "🤍 ✒️ СТИЛИЗАТОР":
        user_state[chat_id] = 'waiting_style'
        bot.send_message(
            chat_id, 
            "✒️ <b>Пришли любой текст</b>, и я преобразую его в моноширинный код-формат!", 
            parse_mode="HTML"
        )

    elif text == "🖤 🎲 ЦИТАТА / ОРАКУЛ":
        quotes = [
            "«Сначала сотрите проблему в умах, а затем пишите код.»",
            "«Хороший код — это лучший документ.»",
            "«Любой дурак может написать код, который поймет компьютер. Хорошие программисты пишут код, который понятен человеку.» — Мартин Фаулер",
            "«Ошибки в коде — это просто опыт, выраженный в строках.»",
            "«Простота — залог надежности.» — Эдсгер Дейкстра"
        ]
        q = random.choice(quotes)
        msg = f"🖤 <b>МУДРОСТЬ РАЗРАБОТЧИКА:</b>\n\n<code>{q}</code>"
        bot.send_message(chat_id, msg, parse_mode="HTML")

# ------------------- ИНТЕРАКТИВНЫЕ CALLBACKS -------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("lesson_"):
        lesson_id = data.split("_")[1]
        lesson = FRONTEND_COURSE.get(lesson_id)
        if lesson:
            markup = types.InlineKeyboardMarkup()
            btn_back = types.InlineKeyboardButton("⬅️ Назад к списку уроков", callback_data="back_to_course")
            markup.add(btn_back)
            
            bot.send_message(chat_id, lesson["text"], parse_mode="HTML", reply_markup=markup)

    elif data == "back_to_course":
        msg = "🎓 <b>Выберите следующий урок:</b>"
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=get_course_keyboard())

    elif data == "start_pomodoro":
        bot.answer_callback_query(call.id, "Таймер запущен!")
        bot.send_message(chat_id, "⏳ <b>25 минут фокуса начались!</b> Работаем над кодом.", parse_mode="HTML")
        time.sleep(10)  # Симуляция (в реале можно сделать 25*60)
        bot.send_message(chat_id, "🔔 <b>Время вышло!</b> Сделай перерыв 5 минут 🖤", parse_mode="HTML")

    elif data == "add_note":
        user_state[chat_id] = 'waiting_note'
        bot.send_message(chat_id, "📝 Напишите заметку следующим сообщением:", parse_mode="HTML")

    elif data == "clear_notes":
        user_notes[chat_id] = []
        bot.answer_callback_query(call.id, "Блокнот очищен")
        bot.send_message(chat_id, "🗑 Заметки удалены.", parse_mode="HTML")

if __name__ == '__main__':
    print("🖤 Бот курса Frontend запущен...")
    bot.infinity_polling()
