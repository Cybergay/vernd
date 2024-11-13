import telebot
import sqlite3

# токен бота
bot = telebot.TeleBot('7852742995:AAHLnc9bi2jUwUPI_rARhbAK3vlxHWLllaA')


# Пароль для режима редактирования йоу
admin_password = "Tagir123Abiy"

# Флаг для режима редактирования
edit_mode = False

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kozyaki (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        date TEXT,
                        reason TEXT
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS roles (
                        name TEXT PRIMARY KEY,
                        role TEXT
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS duties (
                        day TEXT PRIMARY KEY,
                        person TEXT
                      )''')
    conn.commit()
    conn.close()

# Добавление косяка в базу данных
def add_kozyak_to_db(name, date, reason):
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kozyaki (name, date, reason) VALUES (?, ?, ?)", (name, date, reason))
    conn.commit()
    conn.close()

# Удаление косяка из базы данных по имени и порядковому номеру
def remove_kozyak_from_db(name, index):
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM kozyaki WHERE name = ? ORDER BY id LIMIT 1 OFFSET ?", (name, index - 1))
    result = cursor.fetchone()
    if result:
        kozyak_id = result[0]
        cursor.execute("DELETE FROM kozyaki WHERE id = ?", (kozyak_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

# Редактирование роли в базе данных
def update_role(name, role):
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO roles (name, role) VALUES (?, ?)", (name, role))
    conn.commit()
    conn.close()

# Редактирование дежурства на день
def update_duty(day, person):
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO duties (day, person) VALUES (?, ?)", (day, person))
    conn.commit()
    conn.close()

# Получение сводной информации из базы данных
def get_kozyaki_summary():
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, COUNT(*) as count FROM kozyaki GROUP BY name")
    summary = "Статистика косяков хаты:\n"
    for row in cursor.fetchall():
        summary += f"{row[0]}: {row[1]} косяков\n"
    conn.close()
    return summary

# Получение всех ролей
def get_roles_summary():
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, role FROM roles")
    summary = "Роли по хате:\n"
    for row in cursor.fetchall():
        summary += f"{row[0]}: {row[1]}\n"
    conn.close()
    return summary

# Получение всех дежурств
def get_duties_summary():
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT day, person FROM duties")
    summary = "Дежурство на кухне:\n"
    for row in cursor.fetchall():
        summary += f"{row[0]}: {row[1]}\n"
    conn.close()
    return summary

# Получение подробной информации о косяках для конкретного человека
def get_kozyaki_details(name):
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, reason FROM kozyaki WHERE name = ?", (name,))
    details = cursor.fetchall()
    conn.close()
    return details

# Инициализация базы данных при старте
init_db()

# Вход в режим редактирования
@bot.message_handler(commands=['edit'])
def enter_edit_mode(message):
    global edit_mode
    msg = bot.send_message(message.chat.id, "Введите пароль для входа в режим редактирования:")
    bot.register_next_step_handler(msg, check_password)

# Проверка пароля
def check_password(message):
    global edit_mode
    if message.text == admin_password:
        edit_mode = True
        bot.send_message(message.chat.id, "Пароль верный! Вход в режим редактирования.")
    else:
        bot.send_message(message.chat.id, "Неправильный пароль!")

# Добавление косяка через команду /add
@bot.message_handler(func=lambda message: edit_mode and message.text.startswith('/add'))
def add_kozyak(message):
    try:
        parts = message.text.split(" ", 3)  # Сплитим до 4 частей, чтобы ЧТо? хз мне лень
        name = parts[1]
        date = parts[2]
        reason = parts[3] if len(parts) > 3 else "Не указана причина"  # Все оставшееся – причина
        add_kozyak_to_db(name, date, reason)
        bot.send_message(message.chat.id, f"Косяк для {name} добавлен!")
    except IndexError:
        bot.send_message(message.chat.id, "Неверный формат! Используйте: /add <имя> <дата> <причина>")

# Удаление косяка через команду /remove
@bot.message_handler(func=lambda message: edit_mode and message.text.startswith('/remove'))
def remove_kozyak(message):
    try:
        _, name, index = message.text.split(" ", 2)
        index = int(index)
        if remove_kozyak_from_db(name, index):
            bot.send_message(message.chat.id, f"Косяк номер {index} для {name} удален!")
        else:
            bot.send_message(message.chat.id, f"Косяк номер {index} для {name} не найден.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат! Используйте: /remove <имя> <номер косяка>")

# Редактирование роли через команду /role
@bot.message_handler(func=lambda message: edit_mode and message.text.startswith('/role'))
def edit_role(message):
    try:
        _, name, role = message.text.split(" ", 2)
        name = name.title()  # Приводим имя к формату с заглавной буквы а то два имени будут
        update_role(name, role)
        bot.send_message(message.chat.id, f"Роль для {name} обновлена на '{role}'!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат! Используйте: /role <имя> <роль>")

# Редактирование дежурства через команду /duty
@bot.message_handler(func=lambda message: edit_mode and message.text.startswith('/duty'))
def edit_duty(message):
    try:
        _, day, person = message.text.split(" ", 2)
        day = day.capitalize()  # Приводим день к формату с заглавной буквы
        person = person.title()  # Приводим имя к формату с заглавной буквы
        update_duty(day, person)
        bot.send_message(message.chat.id, f"Дежурный на {day} обновлен на '{person}'!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат! Используйте: /duty <день> <имя>")

# Выход из режима редактирования
@bot.message_handler(commands=['done'])
def exit_edit_mode(message):
    global edit_mode
    if edit_mode:
        edit_mode = False
        bot.send_message(message.chat.id, "Вы вышли из режима редактирования.")
    else:
        bot.send_message(message.chat.id, "Вы не в режиме редактирования.")

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_stats = telebot.types.KeyboardButton('Статистика косяков хаты')
    btn_roles = telebot.types.KeyboardButton('Роли')
    btn_duties = telebot.types.KeyboardButton('Дежурство на кухне')
    btn_king = telebot.types.KeyboardButton('посмотреть в глазок')  # Добавляем кнопку обратно
    markup.row(btn_stats, btn_roles, btn_duties)
    markup.row(btn_king)
    bot.send_message(message.chat.id, "Selam alaikum! Выбери то, что тебя интересует.", reply_markup=markup)


# Команда /help
@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id, "Абый! есть команды такие, как: /edit, чтобы перейти в режим редактирования. /role , /remove, /duty, думаю что за что и так понятно, если что там можно посмотреть. И ПОСЛЕ ВСЕХ ИЗМЕНЕНИЙ ПИШИ /done, чтобы выйти из режима редактирования, а то бот афигеет. ")

# Обработка кнопок
@bot.message_handler(func=lambda message: message.text == "Статистика косяков хаты")
def send_stats(message):
    summary = get_kozyaki_summary()
    markup = telebot.types.InlineKeyboardMarkup()

    # Добавляем кнопки для каждого человека из таблицы косяков
    conn = sqlite3.connect("kozyaki.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM kozyaki")
    for row in cursor.fetchall():
        markup.add(telebot.types.InlineKeyboardButton(row[0], callback_data=f"detail_{row[0]}"))
    conn.close()

    bot.send_message(message.chat.id, summary, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("detail_"))
def send_detailed_info(call):
    name = call.data[len("detail_"):]
    details = get_kozyaki_details(name)
    if details:
        detail_message = f"Подробная информация о косяках {name}:\n\n"
        for idx, detail in enumerate(details, 1):
            detail_message += f"{idx}. Дата: {detail[0]}, Причина: {detail[1]}\n"
    else:
        detail_message = f"Нет информации о косяках для {name}."
    bot.send_message(call.message.chat.id, detail_message)


@bot.message_handler(func=lambda message: message.text == "Роли")
def send_roles(message):
    summary = get_roles_summary()
    bot.send_message(message.chat.id, summary)


@bot.message_handler(func=lambda message: message.text == "Дежурство на кухне")
def send_duties(message):
    summary = get_duties_summary()
    bot.send_message(message.chat.id, summary)


# Обработка команды "посмотреть в глазок"
@bot.message_handler(func=lambda message: message.text == "посмотреть в глазок")
def send_photo_of_king(message):
    try:
        with open(r'2 булат.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Фотография не найдена. Проверь путь к файлу.")


# Запуск бота
bot.polling(none_stop=True)
