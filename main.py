# --------------------------- #
#      Written by KIRYA       #
#   Created on: 14.03.2025    #
# Last updated on: 15.03.2025 #
# --------------------------- #

# --------------------------------------------------------------------------- #
# STANDARD LIBRARIES                                                          #
# --------------------------------------------------------------------------- #

import random

# --------------------------------------------------------------------------- #
# EXTERNAL LIBRARIES                                                          #
# --------------------------------------------------------------------------- #

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# --------------------------------------------------------------------------- #
# GLOBALS                                                                     #
# --------------------------------------------------------------------------- #

# --- #
# BOT #
# --- #

BOT_TOKEN = '<place-your-bot-token-here>'
BOT = TeleBot(BOT_TOKEN)
BOT_DEVELOPER = False

# ------ #
# STATES #
# ------ #

current_state = None
STATES = ['start', 'profile_maker_age', 'profile_maker_sex',
          'profile_maker_preffered_sex', 'profile_maker_city', 'profile_maker_name',
          'profile_maker_description', 'profile_maker_photo_video', 'profile_maker_show_result',
          'search_loop', 'write_to_user', 'sleep_mode',
          'my_profile', 'delete_profile_ask', 'delete_profile']

# --------------- #
# ALLOWED ANSWERS #
# --------------- #

STATE_START_ALLOWED_ANSWERS = ['👍']
STATE_SEX_ALLOWED_ANSWERS = ['Я — парень', 'Я — девушка']
STATE_PREFFERED_SEX_ALLOWED_ANSWERS = ['Девушки', 'Парни', 'Все равно']
STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS = ['Да', 'Изменить анкету']
STATE_SEARCH_LOOP_ALLOWED_ANSWERS = ['❤️', '💌', '👎', '💤']
STATE_WRITE_TO_USER_ALLOWED_ANSWERS = ['Вернуться назад']
STATE_SLEEP_MODE_ALLOWED_ANSWERS = ['1', '2', '3']
STATE_MY_PROFILE_ALLOWED_ANSWERS = ['1 🚀', '2']
STATE_DELETE_PROFILE_ALLOWED_ANSWERS = ['😴 Удалить анкету', '[DEV] Удалить анкету и отключить бота [DEV]', '← Назад']
STATE_POST_DELETION_ALLOWED_ANSWERS = ['Старт']

# -------------------- #
# USER'S PROFILE CLASS #
# -------------------- #

class BotUser:
    def __init__(self, age, sex,
                 preffered_sex, city, name,
                 description, photo_video):
        self.age = age
        self.sex = sex
        self.preffered_sex = preffered_sex
        self.city = city
        self.name = name
        self.description = description
        self.photo_video = photo_video

# ------ #
# SEARCH #
# ------ #

profile = None
temp_profile = None

# --------------------------------------------------------------------------- #
# SYSTEM FUNCTIONS                                                            #
# --------------------------------------------------------------------------- #

def bot_create_reply_keyboard(options_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in options_list:
        if (options_list == STATE_DELETE_PROFILE_ALLOWED_ANSWERS) and
           (option == STATE_DELETE_PROFILE_ALLOWED_ANSWERS[1]) and
           (BOT_DEVELOPER):
            pass
        else:
            continue
        keyboard.add(KeyboardButton(option))
    return keyboard
    
def bot_wrong_answer(msg):
    BOT.send_message(msg.chat.id, 'Нет такого варианта ответа.')

# --------------------------------------------------------------------------- #
# COMMANDS                                                                    #
# --------------------------------------------------------------------------- #

# --------------- #
# "START" COMMAND #
# --------------- #

@BOT.message_handler(commands=['start'])
def cmd_start(msg):
    global current_state
    
    current_state = STATES[0]
    
    BOT.send_message(msg.chat.id,
                     'Я помогу найти тебе пару или просто друзей. Можно я задам тебе пару вопросов?',
                     reply_markup=bot_create_reply_keyboard(STATE_START_ALLOWED_ANSWERS))

# --------------------------------------------------------------------------- #
# HANDLERS                                                                    #
# --------------------------------------------------------------------------- #

# ---------------- #
# MESSAGES HANDLER #
# ---------------- #

# ------------------------------------------------ #
#                !!! WARNING !!!                   #
# THIS CUSTOM HANDLER IS FULL OF POOR-QUALITY CODE #
#              YOU'VE BEEN WARNED                  #
# ------------------------------------------------ #

@BOT.message_handler(func = lambda msg: True, content_types=['text', 'photo'])
def messages_handler(msg):
    global current_state
    
    match current_state:
        
        case 'start':
            if (msg.text in STATE_START_ALLOWED_ANSWERS):
                match msg.text:
                    case '👍':
                        current_state = STATES[1]
                        profile_maker_age(msg)
            else:
                bot_wrong_answer(msg)
                        
        case 'profile_maker_age':
            if (not msg.text.isdigit()):
                BOT.send_message(msg.chat.id, 'Укажи правильный возраст. Только цифры.')
            else:
                main_user.age = msg.text
                current_state = STATES[2]
                profile_maker_sex(msg)
            
        case 'profile_maker_sex':
            if (msg.text in STATE_SEX_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Я — парень':
                        main_user.sex = 'male'
                    case 'Я — девушка':
                        main_user.sex = 'female'
                current_state = STATES[3]
                profile_maker_preffered_sex(msg)
            else:
                bot_wrong_answer(msg)
            
        case 'profile_maker_preffered_sex':
            if (msg.text in STATE_PREFFERED_SEX_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Девушки':
                        main_user.preffered_sex = 'females'
                    case 'Парни':
                        main_user.preffered_sex = 'males'
                    case 'Все равно':
                        main_user.preffered_sex = 'everyone'
                current_state = STATES[4]
                profile_maker_city(msg)
            else:
                bot_wrong_answer(msg)
            
        case 'profile_maker_city':
            if (not msg.text.isalpha()):
                BOT.send_message(msg.chat.id, 'Укажи правильное название города. Только буквы.')
            else:
                main_user.city = msg.text
                current_state = STATES[5]
                profile_maker_name(msg)
            
        case 'profile_maker_name':
            if (not msg.text.isalpha()):
                BOT.send_message(msg.chat.id, 'Укажи правильное имя. Только буквы.')
            else:
                main_user.name = msg.text
                current_state = STATES[6]
                profile_maker_description(msg)
            
        case 'profile_maker_description':
            if (len(msg.text) > 900):
                BOT.send_message(msg.chat.id, 'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
            else:
                main_user.description = msg.text
                current_state = STATES[7]
                profile_maker_photo_video(msg)
            
        case 'profile_maker_photo_video':
            if (not msg.content_type == 'photo'):
                BOT.send_message(msg.chat.id, 'Не удалось загрузить фото либо оно не было добавлено. Попробуй еще раз.')
            else:
                main_user.photo_video = msg
                current_state = STATES[8]
                profile_maker_show_result(msg)
            
        case 'profile_maker_show_result':
            if (msg.text in STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Да':
                        current_state = STATES[9]
                        search_loop(msg)
                    case 'Изменить анкету':
                        current_state = STATES[1]
                        profile_maker_age(msg)
            else:
                bot_wrong_answer(msg)
                        
        case 'search_loop':
            if (msg.text in STATE_SEARCH_LOOP_ALLOWED_ANSWERS):
                match msg.text:
                    case '❤️':
                        search_loop(msg)
                    case '💌':
                        current_state = STATES[10]
                        write_to_user(msg)
                    case '👎':
                        search_loop(msg)
                    case '💤':
                        current_state = STATES[11]
                        sleep_mode(msg)
            else:
                bot_wrong_answer(msg)
                        
        case 'write_to_user':
            if (msg.text in STATE_WRITE_TO_USER_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Вернуться назад':
                        current_state = STATES[9]
                        search_loop(msg)
            else:
                if (len(msg.text) > 900):
                    BOT.send_message(msg.chat.id, 'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
                elif (len(msg.text) == 0):
                    BOT.send_message(msg.chat.id, 'Сообщение не может быть пустым.')
                else:
                    BOT.send_message(msg.chat.id, 'Лайк отправлен, ждем ответа.')
                    current_state = STATES[9]
                    search_loop(msg)
            
        case 'sleep_mode':
            if (msg.text in STATE_SLEEP_MODE_ALLOWED_ANSWERS):
                match msg.text:
                    case '1':
                        current_state = STATES[9]
                        search_loop(msg)
                    case '2':
                        current_state = STATES[12]
                        my_profile(msg)
                    case '3':
                        current_state = STATES[13]
                        delete_profile_ask(msg)
            else:
                bot_wrong_answer(msg)
                        
        case 'my_profile':
            if (msg.text in STATE_MY_PROFILE_ALLOWED_ANSWERS):
                match msg.text:
                    case '1 🚀':
                        current_state = STATES[9]
                        search_loop(msg)
                    case '2':
                        current_state = STATES[1]
                        profile_maker_age(msg)
            else:
                bot_wrong_answer(msg)
            
        case 'delete_profile_ask':
            if (msg.text in STATE_DELETE_PROFILE_ALLOWED_ANSWERS):
                match msg.text:
                    case '😴 Удалить анкету':
                        current_state = STATES[14]
                        delete_profile(msg)
                    case '[DEV] Удалить анкету и отключить бота [DEV]' if BOT_DEVELOPER:
                        delete_profile_and_disable_bot(msg)
                    case '← Назад':
                        current_state = STATES[12]
                        my_profile(msg)
            else:
                bot_wrong_answer(msg)
                
        case 'delete_profile':
            if (msg.text in STATE_POST_DELETION_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Старт':
                        cmd_start(msg)
            else:
                bot_wrong_answer(msg)

# --------------------------------------------------------------------------- #
# FUNCTIONS                                                                   #
# --------------------------------------------------------------------------- #

# ------------- #
# PROFILE MAKER #
# ------------- #

def profile_maker_age(msg):
    BOT.send_message(msg.chat.id, 'Сколько тебе лет?')
    
def profile_maker_sex(msg):
    BOT.send_message(msg.chat.id, 'Теперь определимся с полом.',
                     reply_markup=bot_create_reply_keyboard(STATE_SEX_ALLOWED_ANSWERS))
    
def profile_maker_preffered_sex(msg):
    BOT.send_message(msg.chat.id, 'Кто тебе интересен?',
                     reply_markup=bot_create_reply_keyboard(STATE_PREFFERED_SEX_ALLOWED_ANSWERS))
    
def profile_maker_city(msg):
    BOT.send_message(msg.chat.id, 'Из какого ты города?')
    
def profile_maker_name(msg):
    BOT.send_message(msg.chat.id, 'Как мне тебя называть?')
    
def profile_maker_description(msg):
    BOT.send_message(msg.chat.id, 'Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию.')
    
def profile_maker_photo_video(msg):
    BOT.send_message(msg.chat.id, 'Теперь пришли фото 👍 — его будут видеть другие пользователи.')
    
def profile_maker_show_result(msg):
    BOT.send_message(msg.chat.id, 'Так выглядит твоя анкета:')
    BOT.send_photo(msg.chat.id, main_user.photo_video.photo[-1].file_id,
                   '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id, 'Все верно?',
                     reply_markup=bot_create_reply_keyboard(STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS))

# ------ #
# SEARCH #
# ------ #

def search_loop(msg):
    global profile
    global temp_profile
    
    while (profile == temp_profile):
        profile = random.choice(fake_users)
    
    temp_profile = profile
    
    if (profile.photo_video == ''):
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(profile.name, profile.age, profile.city, profile.description),
                         reply_markup=bot_create_reply_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    else:
        BOT.send_photo(msg.chat.id, profile.photo_video,
                       '{0}, {1}, {2}\n\n{3}'.format(profile.name, profile.age, profile.city, profile.description),
                       reply_markup=bot_create_reply_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    
def write_to_user(msg):
    BOT.send_message(msg.chat.id, 'Напиши сообщение для этого пользователя:',
                     reply_markup=bot_create_reply_keyboard(STATE_WRITE_TO_USER_ALLOWED_ANSWERS))
    
def sleep_mode(msg):
    BOT.send_message(msg.chat.id, 'Подождем, пока кто-то увидит твою анкету.')
    BOT.send_message(msg.chat.id, '1. Смотреть анкеты.\n2. Моя анкета.\n3. Я больше не хочу никого искать.',
                     reply_markup=bot_create_reply_keyboard(STATE_SLEEP_MODE_ALLOWED_ANSWERS))

def my_profile(msg):
    BOT.send_message(msg.chat.id, 'Так выглядит твоя анкета:')
    BOT.send_photo(msg.chat.id, main_user.photo_video.photo[-1].file_id,
                   '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id, '1. Смотреть анкеты.\n2. Заполнить анкету заново.',
                     reply_markup=bot_create_reply_keyboard(STATE_MY_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile_ask(msg):
    BOT.send_message(msg.chat.id, 'Так ты не узнаешь, что кому-то нравишься... Точно хочешь удалить свою анкету?',
                     reply_markup=bot_create_reply_keyboard(STATE_DELETE_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile(msg):
    BOT.send_message(msg.chat.id, 'Надеюсь, ты нашел кого-то благодаря мне! Рад был с тобой пообщаться, будет скучно — пиши, обязательно найдем тебе кого-нибудь!',
                     reply_markup=bot_create_reply_keyboard(STATE_POST_DELETION_ALLOWED_ANSWERS))
    
def delete_profile_and_disable_bot(msg):
    BOT.send_message(msg.chat.id, 'Анкета удалена. Бот будет выключен в течение 10 секунд.')
    BOT.stop_bot()

# --------------------------------------------------------------------------- #
# ENTRY POINT                                                                 #
# --------------------------------------------------------------------------- #

if (__name__ == '__main__'):
    main_user = BotUser
    
    fake_user_1 = BotUser('18', 'male', 'females',
                          'Москва', 'Модный чел', 'чисто девчонку чтоб завалиться в клуб побухать аее))',
                          'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/1.jpg')
    
    fake_user_2 = BotUser('23', 'female', 'males',
                          'Москва', 'Девушка мечты', 'Учусь в Литературном институте, интересуюсь вышиванием и танцами. Хочу сходить на свидание с милым парнем ^^',
                          'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/2.jpg')
    
    fake_user_3 = BotUser('44', 'female', 'males',
                          'Москва', 'Лидия', 'Ищу верного, надежного мужчину для построения семьи! Есть ребенок!',
                          'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/3.jpg')
    
    fake_user_4 = BotUser('53', 'male', 'everyone',
                          'Москва', 'Владимир Ульянов', 'Товарищи! Не верьте всему тому, что пишут в интернете!',
                          'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/4.jpg')
    
    fake_user_5 = BotUser('32', 'female', 'everyone',
                          'Москва', 'Катя', 'Хотелось бы найти друзей, с которыми можно будет ходить гулять по нашему чудесному городу)\n\nP. S. Отношения не интересуют, так как есть молодой человек.',
                          'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/5.jpg')
    
    fake_users = [fake_user_1, fake_user_2, fake_user_3,
                  fake_user_4, fake_user_5]
    
    BOT.infinity_polling()