import telebot
from telebot import types
import time
import random

# Ваш токен уже вставлен в код
TOKEN = '8715699108:AAHShcE6CXS0oJDtS3pQT6LLtc2oIVN59Xg'
bot = telebot.TeleBot(TOKEN)

# Временное хранилище заметок пользователем в памяти
user_notes = {}
user_state = {}

# ------------------- КЛАВИАТУРЫ -------------------

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_lessons = types.KeyboardButton("🎓 МИНИ-УРОКИ")
    btn_focus = types.KeyboardButton("⏱️ ФОКУС-ТАЙМЕР")
    btn_notes = types.KeyboardButton("📓 БЛОКНОТ")
    btn_style = types.KeyboardButton("✒️ ЧБ СТИЛИЗАТОР")
    btn_oracle = types.KeyboardButton("🎲 ЦИТАТА / ОРАКУЛ")
    markup.add(btn_lessons, btn_focus, btn_notes, btn_style, btn_oracle)
    return markup

def get_lessons_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    b1 = types.InlineKeyboardButton("🐍 Python & Кодинг", callback_data="lesson_code")
    b2 = types.InlineKeyboardButton("🧠 Продуктивность & Тайм-менеджмент", callback_data="lesson_prod")
    b3 = types.InlineKeyboardButton("📐 Критическое мышление", callback_data="lesson_think")
    markup.add(b1, b2, b3)
    return markup

# ------------------- ХЭНДЛЕРЫ КОМАНД -------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "```\n"
        "┌───────────────────────────┐\n"
        "│    M O N O C H R O M E    │\n"
        "│       B O T  v 1 . 0      │\n"
        "└───────────────────────────┘\n"
        "```\n"
        "🖤 **Добро пожаловать в минималистичный хаб.**\n\n"
        "Здесь нет ничего лишнего — только польза, фокусировка и эстетика.\n\n"
        "▪️ **Уроки** — прокачка навыков\n"
        "▪️ **Фокус-таймер** — работа без отвлечений\n"
        "▪️ **Блокнот** — быстрая записная книжка\n"
        "▪️ **Стилизатор** — красивый ЧБ текст\n\n"
        "Выбери нужный раздел на клавиатуре ниже ⤵️"
    )
    bot.send_message(
        message.chat.id, 
        welcome_text, 
        parse_mode="Markdown", 
        reply_markup=get_main_keyboard()
    )

# ------------------- ОСНОВНОЕ МЕНЮ -------------------

@bot.message_handler(content_types=['text'])
def handle_menu(message):
    chat_id = message.chat.id
    text = message.text

    # Проверяем, ожидает ли бот ввод текста для конвертера или блокнота
    if user_state.get(chat_id) == 'waiting_note':
        if chat_id not in user_notes:
            user_notes[chat_id] = []
        user_notes[chat_id].append(text)
        user_state[chat_id] = None
        bot.send_message(chat_id, f"🖤 `Заметка сохранена:`\n> {text}", parse_mode="Markdown")
        return

    if user_state.get(chat_id) == 'waiting_style':
        spaced_text = " ".join(list(text.upper()))
        formatted = (
            f"▪️ **Исходник:** `{text}`\n\n"
            f"▪️ **Моно-пробел:**\n`{spaced_text}`\n\n"
            f"▪️ **Код-блок:**\n```\n{text}\n```"
        )
        user_state[chat_id] = None
        bot.send_message(chat_id, formatted, parse_mode="Markdown")
        return

    # Разделы меню
    if text == "🎓 МИНИ-УРОКИ":
        msg = (
            "░░░░░░░░░░░░░░░░░░░░░░░░░\n"
            "   🎓 **БАЗА ЗНАНИЙ & УРОКИ**\n"
            "░░░░░░░░░░░░░░░░░░░░░░░░░\n\n"
            "Выбери категорию для изучения короткого, но полезного материала:"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=get_lessons_keyboard())

    elif text == "⏱️ ФОКУС-ТАЙМЕР":
        markup = types.InlineKeyboardMarkup()
        btn_start = types.InlineKeyboardButton("▶️ Запустить 25 мин (Помодоро)", callback_data="start_pomodoro")
        markup.add(btn_start)
        msg = (
            "🔳 **ЧБ ФОКУС-ТАЙМЕР**\n\n"
            "Метод Pomodoro: 25 минут глубокой работы без соцсетей и телефона.\n"
            "Готов сконцентрироваться?"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

    elif text == "📓 БЛОКНОТ":
        notes = user_notes.get(chat_id, [])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_add = types.InlineKeyboardButton("➕ Добавить", callback_data="add_note")
        btn_clear = types.InlineKeyboardButton("🗑 Очистить", callback_data="clear_notes")
        markup.add(btn_add, btn_clear)

        if not notes:
            notes_text = "_Ваш блокнот пуст._"
        else:
            notes_text = "\n".join([f"▫️ `{i+1}.` {n}" for i, n in enumerate(notes)])

        msg = f"📓 **ВАШИ ЗАМЕТКИ:**\n\n{notes_text}"
        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

    elif text == "✒️ ЧБ СТИЛИЗАТОР":
        user_state[chat_id] = 'waiting_style'
        bot.send_message(
            chat_id, 
            "✒️ **Пришли любой текст или фразу**, и я преобразую её в эстетичный монохромный формат!", 
            parse_mode="Markdown"
        )

    elif text == "🎲 ЦИТАТА / ОРАКУЛ":
        quotes = [
            "«Симплисити — это крайняя степень утонченности.» — Леонардо да Винчи",
            "«Хаос — это просто нерасшифрованный порядок.»",
            "«Делай меньше, но делай это безупречно.»",
            "«Черный и белый — это цвета фотографии. Для меня они символизируют надежду и отчаяние.»",
            "«Фокус — это умение говорить «нет» сотне других хороших идей.» — Стив Джобс"
        ]
        q = random.choice(quotes)
        msg = (
            "─── 🖤 **MONOCHROME WISDOM** ───\n\n"
            f"`{q}`\n\n"
            "─────────────────────────"
        )
        bot.send_message(chat_id, msg, parse_mode="Markdown")

# ------------------- ИНТЕРАКТИВНЫЕ CALLBACKS -------------------

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id

    if call.data == "lesson_code":
        text = (
            "🐍 **УРОК: Правило DRY в кодинге**\n\n"
            "**DRY = Don't Repeat Yourself** (Не повторяйся).\n\n"
            "❌ **Плохо:**\n"
            "```python\n"
            "print('Привет, Али!')\n"
            "print('Привет, Иван!')\n"
            "```\n\n"
            "✅ **Хорошо:**\n"
            "```python\n"
            "def greet(name):\n"
            "    print(f'Привет, {name}!')\n"
            "```\n"
            "💡 _Пиши функции, если код повторяется больше 2 раз._"
        )
        bot.send_message(chat_id, text, parse_mode="Markdown")

    elif call.data == "lesson_prod":
        text = (
            "🧠 **УРОК: Правило 2-х минут**\n\n"
            "Если задача занимает **меньше 2 минут** (ответить на письмо, вынести мусор, сделать отжимания) — **сделай её прямо сейчас**.\n\n"
            "не записывай её в планёр, не откладывай. Это освобождает до 30% ресурса мозга ежедневно."
        )
        bot.send_message(chat_id, text, parse_mode="Markdown")

    elif call.data == "lesson_think":
        text = (
            "📐 **УРОК: Бритва Оккама**\n\n"
            "«Не следует множить сущности без необходимости».\n\n"
            "💡 **Суть:** Если есть несколько объяснений ситуации, самое простое из них, как правило, является правильным.\nНе усложняй вещи там, где всё очевидно."
        )
        bot.send_message(chat_id, text, parse_mode="Markdown")

    elif call.data == "start_pomodoro":
        bot.answer_callback_query(call.id, "Фокус-таймер запущен!")
        bot.send_message(chat_id, "⏳ **Сессия 25 минут началась.** Убери телефон и займись делом!\nЯ пришлю уведомление, когда время выйдет.", parse_mode="Markdown")
        
        # Симуляция таймера (для теста 10 секунд, можно заменить на 25*60)
        time.sleep(10) 
        bot.send_message(chat_id, "🔔 **ВРЕМЯ ВЫШЛО!** Отдохни 5 минут (сделай разминку, выпей воды) и возвращайся! 🖤", parse_mode="Markdown")

    elif call.data == "add_note":
        user_state[chat_id] = 'waiting_note'
        bot.send_message(chat_id, "📝 Напиши текст заметки следующим сообщением:", parse_mode="Markdown")

    elif call.data == "clear_notes":
        user_notes[chat_id] = []
        bot.answer_callback_query(call.id, "Заметки очищены")
        bot.send_message(chat_id, "🗑 Ваши заметки успешно удалены.", parse_mode="Markdown")

# ------------------- ЗАПУСК -------------------
if __name__ == '__main__':
    print("⬛ Бот успешно запущен и готов к работе...")
    bot.infinity_polling()
