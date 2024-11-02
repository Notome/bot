import telebot 

token = "7657238843:AAEN5uwZcFHutGT1p9pfQ8yeECFdRb3QYb8"
bot = telebot.TeleBot(token)
user_data = {'budget': 0, 'reach': 0, 'ca': [], 'theme': [], 'reels': None, 'stories': None}

# Данные о блогерах
db = [
    {'budget': 5000, 'reach': 6000, 'ca': ['35-44', '45-54', '25-34'], 
     'theme': ["Психология", "Паблик", "Мамочки"], 'reels': False, 'stories': True}
]

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Чтобы начать поиск блогеров.")
    show_main_menu(message)

def reset_search(message):
    bot.send_message(message.chat.id, 'Данные поиска удалены')
    global user_data
    user_data = {'budget': 0, 'reach': 0, 'ca': [], 'theme': [], 'reels': None, 'stories': None}  # Обнуляем данные
    show_main_menu(message)

@bot.message_handler(func=lambda message: message.text == 'Начать поиск')
def start_search(message):
    bot.send_message(message.chat.id, "Начинаем поиск! Введите максимальный бюджет:")
    bot.register_next_step_handler(message, get_budget)

def show_main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = telebot.types.KeyboardButton('Начать поиск')
    reset_button = telebot.types.KeyboardButton('Начать заново')
    markup.add(start_button, reset_button)
    bot.send_message(message.chat.id, "Нажмите на кнопку:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text not in ['Начать поиск', 'Начать заново'])
def handle_invalid_input(message):
    bot.send_message(message.chat.id, 'Неверное значение.')
    show_main_menu(message)

def get_budget(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    try:
        budget = int(message.text)
        user_data['budget'] = budget 
        bot.send_message(message.chat.id, 'Записали! Внесите теперь минимальный охват:')
        bot.register_next_step_handler(message, get_reach)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели не число. Попробуйте снова:')
        bot.register_next_step_handler(message, get_budget)

def get_reach(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return
            
    try:
        reach = int(message.text)
        user_data['reach'] = reach 
        bot.send_message(message.chat.id, 'Записали!')
        get_ca(message)
    except ValueError:
        bot.send_message(message.chat.id, 'Вы ввели не число. Попробуйте снова:')
        bot.register_next_step_handler(message, get_reach)

def get_ca(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    age_ranges = ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    for age in age_ranges:
        markup.add(telebot.types.KeyboardButton(age))
    bot.send_message(message.chat.id, "Выберите ЦА, которая вам нужна:", reply_markup=markup)
    bot.register_next_step_handler(message, process_ca)

def process_ca(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    if message.text not in ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']:
        bot.send_message(message.chat.id, "Выберите из предложенных значений")
        get_ca(message)
        return

    if message.text not in user_data['ca']:
        user_data['ca'].append(message.text)
    else: 
        bot.send_message(message.chat.id, "Данные уже были внесены.")

    bot.send_message(message.chat.id, "Вы хотите добавить ещё ЦА?")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = telebot.types.KeyboardButton('Да')
    item2 = telebot.types.KeyboardButton('Нет')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите:", reply_markup=markup)
    
    bot.register_next_step_handler(message, handle_ca_choice)

def handle_ca_choice(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    if message.text == 'Да': 
        get_ca(message)
    elif message.text == 'Нет': 
        get_theme(message)
    else: 
        bot.send_message(message.chat.id, "Вы не выбрали вариант")
        get_ca(message)

def get_theme(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    theme_ranges = ["Психология", "Паблик", "Лайф", "Жизнь за границей", "Семья", "Фудблог", "Мамочки", "Огород/Сад", "Мода", "Врач", "Распаковки", "Похудение"]
    for theme in theme_ranges:
        markup.add(telebot.types.KeyboardButton(theme))
    bot.send_message(message.chat.id, "Выберите тему, которая вам нужна:", reply_markup=markup)
    bot.register_next_step_handler(message, process_theme)

def process_theme(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    if message.text not in ["Психология", "Паблик", "Лайф", "Жизнь за границей", "Семья", "Фудблог", "Мамочки", "Огород/Сад", "Мода", "Врач", "Распаковки"]:
        bot.send_message(message.chat.id, 'Выберите из предложенных значений.')
        get_theme(message)
        return
    
    if message.text not in user_data['theme']:
        user_data['theme'].append(message.text)
        ask_additional_theme(message)
    else:
        bot.send_message(message.chat.id, "Данные уже были внесены.")
        ask_additional_theme(message)

def ask_additional_theme(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = telebot.types.KeyboardButton('Да')
    item2 = telebot.types.KeyboardButton('Нет')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Вы хотите добавить ещё тему?", reply_markup=markup)
    bot.register_next_step_handler(message, handle_theme_choice)

def handle_theme_choice(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    if message.text == 'Да': 
        get_theme(message)
    elif message.text == 'Нет': 
        get_format(message)
    else: 
        bot.send_message(message.chat.id, "Вы не выбрали вариант. Пожалуйста, выберите 'Да' или 'Нет'.")
        ask_additional_theme(message)

def get_format(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = telebot.types.KeyboardButton('Сторис')
    item2 = telebot.types.KeyboardButton('Рилс')
    item3 = telebot.types.KeyboardButton('Любой')
    markup.add(item1, item2, item3)  # Добавляем кнопки в разметку
    bot.send_message(message.chat.id, 'Какой формат вас интересует?', reply_markup=markup)
    bot.register_next_step_handler(message, process_format)

def process_format(message):
    if message.text == 'Начать заново':
        reset_search(message)
        return

    if message.text not in ['Рилс', 'Сторис', 'Любой']:
        bot.send_message(message.chat.id, 'Выберите из предложенных значений.')
        get_format(message)  
        return
    
    # Установка значений в user_data
    user_data['reels'] = message.text == 'Рилс' or message.text == 'Любой'
    user_data['stories'] = message.text == 'Сторис' or message.text == 'Любой'
    
    check_conditions(message)

def check_conditions(message):
    indexes = [] 
    for idx, blogger in enumerate(db):
        if blogger.get('budget', 0) > user_data['budget']:
            continue  

        if blogger.get('reach', 0) < user_data['reach']:
            continue 

        if not any(c in blogger['ca'] for c in user_data['ca']):
            continue  

        if not any(theme in blogger['theme'] for theme in user_data['theme']):
            continue  

        if user_data['reels'] and not blogger['reels']:
            continue  

        if user_data['stories'] and not blogger['stories']:
            continue  

        indexes.append(idx)

    if indexes: 
        response_message = "Найдены следующие блогеры, соответствующие вашим критериям:\n" + "\n".join(f"Блогер {i+1}" for i in indexes)
    else: 
        response_message = "К сожалению, не найдено блогеров, соответствующих вашим критериям."

    bot.send_message(message.chat.id, response_message)

bot.infinity_polling()
