#крч, за 21.10.2024 косяки + 1 всем, кроме артура, тагира, шамиля и гиндули
# косяк щамилю, абсу, шайд и шамсу +1 за 22.10
# косяк шамилю, абсу, шайд и шамсу +1 за 23.10
import telebot

# Вставь сюда свой токен бота
bot = telebot.TeleBot('7852742995:AAHLnc9bi2jUwUPI_rARhbAK3vlxHWLllaA')

# Сводная информация о косяках (удобно редактировать)
kozyaki_summary = """
Статистика косяков хаты:
Король кринжа(Шомка): 2 косяка
Тимур Гиндулла: 2 косяка
Тимур Шамс: 3 косяков, 500 не отдал
Тимур абс: 4 косяка, 500руб не отдал
Артур: 0 косяков
Шайдуллин: 6 косяка, 1000 рублей не отдал
Тагири: -1(минус один) косяков, 500 руб отдал
"""

# Информация о косяках с подробностями
kozyaki_details = {
    "Король кринжа(Шомка)": [
        {"дата": "-", "причина": "чашки с плесенью и чаем(не помыл, вроде 2 раза)"},
        {"дата": "-", "причина": "посуда с супом"},
        {"дата": "-", "причина": "остальные не знаю\не помню"},
        {"дата": "23.10.2024", "причина": "генка"},
    ],
    "Тимур Гиндулла": [
        {"дата": "15.09.2024", "причина": "генка"},

    ],
    "Тимур Шамс": [
        {"дата": "22.09.2024", "причина": "один косяк за генку (решение общепринятое)"},
        {"дата": "28.09.2024", "причина": "не помыл посуду"},
        {"дата": "-", "причина": "остальные не знаю\не помню"},
        {"дата": "10.10.2024", "причина": "на кухне оставил, по вложениям в группе пруфы"},
        {"дата": "21.10.2024", "причина": "генка"},
        {"дата": "22.10.2024", "причина": "генка"},
        {"дата": "23.10.2024", "причина": "генка"},
    ],
    "Тимур абс": [
        {"дата": "-", "причина": "Балкон(вроде)"},
        {"дата": "04.10.2024", "причина": "Балкон, за форму"},
        {"дата": "21.10.2024", "причина": "генка"},
        {"дата": "22.10.2024", "причина": "генка"},
        {"дата": "23.10.2024", "причина": "генка"},
    ],
    "Артур": [
        {"дата": "13.10.2024", "причина": "генка"},
    ],
    "Шайдуллин": [
        {"дата": "15.09.2024", "причина": "генка"},
        {"дата": "03.10.2024", "причина": "посуда не помыта"},
        {"дата": "21.10.2024", "причина": "генка"},
        {"дата": "22.10.2024", "причина": "генка"},
        {"дата": "23.10.2024", "причина": "генка"},
    ],
    "Тагири": [
        {"дата": "15.09.2024", "причина": "генка"},
        {"дата": "16.09.2024", "причина": "тоже генка, только один косяк"}
    ],
}

# Краткая статистика косяков
kozyaki_stats = {name: f"{len(details)} косяков" for name, details in kozyaki_details.items()}

# Информация о генке
genka_info = """
Артур - Кухня
Тагири - Туалет
Тимур Шамс - Комната своя
Тимур Абс - Комната своя
Тимур Гиндули - Комната своя
Шамиль - Коридор
Шайдуллин - Ванна
"""

# Роли по хате
house_roles = {
    "Шайбоба": "Хозтовары",
    "Артур": "Шериф",
    "Шамиль": "Санитар",
    "Тимур Шамс": "Сантехник",
    "Тагири": "Вайфай и вода",
}

# Дежурство на кухне
kitchen_duties_daily = {
    "Понедельник": "Амир",
    "Вторник": "Гиндула",
    "Среда": "Шамиль",
    "Четверг": "Абс",
    "Пятница": "Шамс",
    "Суббота": "Тагири",
    "Воскресенье": "Артур"
}

# Команда старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Создаем кнопки
    btn_stats = telebot.types.KeyboardButton('Статистика косяков хаты')
    btn_king = telebot.types.KeyboardButton('посмотреть в глазок')
    btn_duties = telebot.types.KeyboardButton('Информация о генке')
    btn_kitchen = telebot.types.KeyboardButton('Роль + дежурный кухни')

    # Размещаем кнопки в два ряда
    markup.row(btn_stats, btn_king)
    markup.row(btn_duties, btn_kitchen)

    bot.send_message(message.chat.id, "Selam alaikum! Выбери то, что тебя интересует.", reply_markup=markup)

# Обработка кнопки для статистики косяков
@bot.message_handler(func=lambda message: message.text == "Статистика косяков хаты")
def send_stats(message):
    markup = telebot.types.InlineKeyboardMarkup()

    # Создаем кнопки для каждого человека
    for name in kozyaki_stats:
        markup.add(telebot.types.InlineKeyboardButton(name, callback_data=f"detail_{name}"))

    bot.send_message(message.chat.id, kozyaki_summary, reply_markup=markup)

# Обработка нажатия на кнопку для детальной информации
@bot.callback_query_handler(func=lambda call: call.data.startswith("detail_"))
def send_detailed_info(call):
    # Извлекаем имя из callback_data
    name = call.data[len("detail_"):]

    # Получаем детальную информацию о косяках
    details = kozyaki_details.get(name, [])
    if details:
        detail_message = f"Подробная информация о косяках {name}:\n\n"
        for idx, detail in enumerate(details, 1):
            detail_message += f"{idx}. Дата: {detail['дата']}, Причина: {detail['причина']}\n"
    else:
        detail_message = f"Нет информации о косяках для {name}."

    bot.send_message(call.message.chat.id, detail_message)

# Обработка кнопки "кто же такой этот король кринжа?"
@bot.message_handler(func=lambda message: message.text == "посмотреть в глазок")
def send_photo_of_king(message):
    try:
        with open(r'2 булат.jpg', 'rb') as photo:  # Убедись, что путь к фото корректный
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Фотография не найдена. Проверь путь к файлу.")

# Обработка кнопки "Информация о генке"
@bot.message_handler(func=lambda message: message.text == "Информация о генке")
def send_genka_info(message):
    bot.send_message(message.chat.id, f"------------Генка------------\n{genka_info}")

# Обработка кнопки "Роль + дежурный кухни"
@bot.message_handler(func=lambda message: message.text == "Роль + дежурный кухни")
def send_kitchen_duties(message):
    roles_message = "\n".join([f"*{role}*: {person}" for role, person in house_roles.items()])
    kitchen_message = "\n".join([f"*{day}*: {person}" for day, person in kitchen_duties_daily.items()])
    full_message = f"------------Роли------------\n{roles_message}\n\n" \
                   f"------------Дежурные на кухне------------\n{kitchen_message}"
    bot.send_message(message.chat.id, full_message, parse_mode='Markdown')

# Запуск бота
bot.polling(none_stop=True)