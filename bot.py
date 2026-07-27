import telebot
from telebot import types

# Вставь сюда свой токен
TOKEN = '8715699108:AAHShcE6CXS0oJDtS3pQT6LLtc2oIVN59Xg'
bot = telebot.TeleBot(TOKEN)

# База из 10 вопросов по C++
QUESTIONS = [
    {
        "question": "1. C++ tilida konsolga ma'lumot chiqarish uchun qaysi buyruq ishlatiladi?",
        "options": ["std::cout", "std::cin", "printf()", "print()"],
        "correct": 0
    },
    {
        "question": "2. C++ tilining asoschisi (yaratuvchisi) kim?",
        "options": ["Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie", "James Gosling"],
        "correct": 1
    },
    {
        "question": "3. C++ da o'zgaruvchini o'zgarmas (konstanta) qilish uchun qaysi kalit so'z ishlatiladi?",
        "options": ["static", "final", "const", "define"],
        "correct": 2
    },
    {
        "question": "4. Butun sonlarni saqlash uchun qaysi ma'lumot turi ishlatiladi?",
        "options": ["float", "double", "char", "int"],
        "correct": 3
    },
    {
        "question": "5. C++ da ko'rsatkich (pointer) e'lon qilish uchun qaysi belgi ishlatiladi?",
        "options": ["*", "&", "#", "@"],
        "correct": 0
    },
    {
        "question": "6. Massiv (array) indeksi qaysi sondan boshlanadi?",
        "options": ["1", "0", "-1", "Ixtiyoriy"],
        "correct": 1
    },
    {
        "question": "7. C++ da mantiqiy 'VA' (AND) operatori qaysi?",
        "options": ["||", "!", "&&", "&"],
        "correct": 2
    },
    {
        "question": "8. Tsiklni (loop) darhol to'xtatib undan chiqish uchun qaysi operator ishlatiladi?",
        "options": ["continue", "return", "exit", "break"],
        "correct": 3
    },
    {
        "question": "9. Klassning faqat shu klass ichida ko'rinadigan maxfiy a'zolari qaysi bo'limda e'lon qilinadi?",
        "options": ["private", "public", "protected", "friend"],
        "correct": 0
    },
    {
        "question": "10. 'new' operatori orqali ajratilgan dinamik xotirani bo'shatish uchun qaysi buyruq ishlatiladi?",
        "options": ["free", "delete", "remove", "clear"],
        "correct": 1
    }
]

# Хранилище прогресса пользователей
user_data = {}

def send_question(chat_id):
    state = user_data.get(chat_id)
    if not state:
        return

    q_idx = state["current_q"]
    q_data = QUESTIONS[q_idx]

    markup = types.InlineKeyboardMarkup()
    for idx, option in enumerate(q_data["options"]):
        btn = types.InlineKeyboardButton(text=option, callback_data=f"ans_{idx}")
        markup.add(btn)

    bot.send_message(
        chat_id,
        f"<b>Savol {q_idx + 1}/10:</b>\n\n{q_data['question']}",
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.message_handler(commands=['start', 'test'])
def start_quiz(message):
    chat_id = message.chat.id
    user_data[chat_id] = {
        "current_q": 0,
        "score": 0
    }
    
    bot.send_message(
        chat_id,
        "<b>C++ bo'yicha test sinoviga xush kelibsiz!</b>\n\n"
        "Sizga 10 ta savol beriladi. Boshladik!",
        parse_mode="HTML"
    )
    send_question(chat_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    chat_id = call.message.chat.id
    state = user_data.get(chat_id)

    if not state:
        bot.answer_callback_query(call.id, "Testni qayta boshlash uchun /start bosing.")
        return

    selected_option = int(call.data.split('_')[1])
    q_idx = state["current_q"]
    correct_option = QUESTIONS[q_idx]["correct"]

    if selected_option == correct_option:
        state["score"] += 1
        bot.answer_callback_query(call.id, "To'g'ri!")
    else:
        correct_text = QUESTIONS[q_idx]["options"][correct_option]
        bot.answer_callback_query(call.id, f"Noto'g'ri! To'g'ri javob: {correct_text}")

    bot.delete_message(chat_id, call.message.message_id)

    state["current_q"] += 1

    if state["current_q"] < len(QUESTIONS):
        send_question(chat_id)
    else:
        score = state["score"]
        total = len(QUESTIONS)
        percent = int((score / total) * 100)

        result_msg = (
            f"<b>Test yakunlandi!</b>\n\n"
            f"Natijangiz: <b>{score}/{total}</b> ({percent}%)\n\n"
        )

        if percent >= 80:
            result_msg += "A'lo natija! C++ asoslarini juda yaxshi bilasiz."
        elif percent >= 50:
            result_msg += "Yomon emas! Lekin yana biroz amaliyot qilish zarar qilmaydi."
        else:
            result_msg += "C++ mavzularini qaytadan takrorlashni maslahat beramiz."

        result_msg += "\n\nQayta topshirish uchun /start bosing."

        bot.send_message(chat_id, result_msg, parse_mode="HTML")
        del user_data[chat_id]

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
