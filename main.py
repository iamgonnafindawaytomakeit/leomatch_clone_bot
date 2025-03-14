# --------------------------- #
#      Written by KIRYA       #
#   Created on: 14.03.2025    #
# Last updated on: 14.03.2025 #
# --------------------------- #

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

BOT_TOKEN = '<put-your-token-here>'
BOT = TeleBot(BOT_TOKEN)

# ------ #
# STATES #
# ------ #

current_state = None
STATES = ['start', 'profile_maker_age', 'profile_maker_sex',
          'profile_maker_preffered_sex', 'profile_maker_city', 'profile_maker_name',
          'profile_maker_description', 'profile_maker_photo_video', 'profile_maker_show_result',
          'search_loop']

# --------------- #
# ALLOWED ANSWERS #
# --------------- #

STATE_START_ALLOWED_ANSWERS = ['👍']
STATE_SEX_ALLOWED_ANSWERS = ['Я — парень', 'Я — девушка']
STATE_PREFFERED_SEX_ALLOWED_ANSWERS = ['Девушки', 'Парни', 'Все равно']
STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS = ['Да', 'Изменить анкету']

# -------------- #
# USER'S PROFILE #
# -------------- #

user_age = None
user_sex = None
user_preffered_sex = None
user_city = None
user_name = None
user_description = None
user_photo_video = None

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
                     reply_markup=cmd_start_keyboard())
                     
def cmd_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(STATE_START_ALLOWED_ANSWERS[0]))
    return markup

# --------------------------------------------------------------------------- #
# HANDLERS                                                                    #
# --------------------------------------------------------------------------- #

# ---------------- #
# MESSAGES HANDLER #
# ---------------- #

# ----------------------------------------- #
#              !!! WARNING !!!              #
# THIS SECTION IS FULL OF POOR-QUALITY CODE #
#            YOU'VE BEEN WARNED             #
# ----------------------------------------- #

@BOT.message_handler(func = lambda msg: True, content_types=['text', 'photo'])
def messages_handler(msg):
    global current_state, user_age, user_sex,\
           user_preffered_sex, user_city, user_name,\
           user_description, user_photo_video
    
    match current_state:
        
        case 'start':
            if (msg.text in STATE_START_ALLOWED_ANSWERS):
                match msg.text:
                    case '👍':
                        current_state = STATES[1]
                        profile_maker_age(msg)
                        
        case 'profile_maker_age':
            if (not msg.text.isdigit()):
                BOT.send_message(msg.chat.id, 'Укажи правильный возраст. Только цифры.')
            else:
                user_age = msg.text
                current_state = STATES[2]
                profile_maker_sex(msg)
            
        case 'profile_maker_sex':
            if (msg.text in STATE_SEX_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Я — парень':
                        user_sex = 'male'
                    case 'Я — девушка':
                        user_sex = 'female'
                current_state = STATES[3]
                profile_maker_preffered_sex(msg)
            
        case 'profile_maker_preffered_sex':
            if (msg.text in STATE_PREFFERED_SEX_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Девушки':
                        user_preffered_sex = 'females'
                    case 'Парни':
                        user_preffered_sex = 'males'
                    case 'Все равно':
                        user_preffered_sex = 'everyone'
                current_state = STATES[4]
                profile_maker_city(msg)
            
        case 'profile_maker_city':
            if (not msg.text.isalpha()):
                BOT.send_message(msg.chat.id, 'Укажи правильное название города. Только буквы.')
            else:
                user_city = msg.text
                current_state = STATES[5]
                profile_maker_name(msg)
            
        case 'profile_maker_name':
            if (not msg.text.isalpha()):
                BOT.send_message(msg.chat.id, 'Укажи правильное имя. Только буквы.')
            else:
                user_name = msg.text
                current_state = STATES[6]
                profile_maker_description(msg)
            
        case 'profile_maker_description':
            if (len(msg.text) > 900):
                BOT.send_message(msg.chat.id, 'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
            else:
                user_description = msg.text
                current_state = STATES[7]
                profile_maker_photo_video(msg)
            
        case 'profile_maker_photo_video':
            if (not msg.content_type == 'photo'):
                BOT.send_message(msg.chat.id, 'Не удалось загрузить фото либо оно не было добавлено. Попробуй еще раз.')
            else:
                user_photo_video = msg
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
            
        case _:
            BOT.send_message(msg.chat.id, 'Нет такого варианта ответа.')

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
                     reply_markup=profile_maker_sex_keyboard())
    
def profile_maker_sex_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(STATE_SEX_ALLOWED_ANSWERS[0]))
    markup.add(KeyboardButton(STATE_SEX_ALLOWED_ANSWERS[1]))
    return markup
    
def profile_maker_preffered_sex(msg):
    BOT.send_message(msg.chat.id, 'Кто тебе интересен?',
                     reply_markup=profile_maker_preffered_sex_keyboard())
    
def profile_maker_preffered_sex_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(STATE_PREFFERED_SEX_ALLOWED_ANSWERS[0]))
    markup.add(KeyboardButton(STATE_PREFFERED_SEX_ALLOWED_ANSWERS[1]))
    markup.add(KeyboardButton(STATE_PREFFERED_SEX_ALLOWED_ANSWERS[2]))
    return markup
    
def profile_maker_city(msg):
    BOT.send_message(msg.chat.id, 'Из какого ты города?')
    
def profile_maker_name(msg):
    BOT.send_message(msg.chat.id, 'Как мне тебя называть?')
    
def profile_maker_description(msg):
    BOT.send_message(msg.chat.id, 'Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию.')
    
def profile_maker_photo_video(msg):
    BOT.send_message(msg.chat.id, 'Теперь пришли фото или запиши видео 👍 (до 15 сек.), его будут видеть другие пользователи.')
    
def profile_maker_show_result(msg):
    BOT.send_message(msg.chat.id, 'Так выглядит твоя анкета:')
    BOT.send_photo(msg.chat.id, user_photo_video.photo[-1].file_id,
                   '{0}, {1}, {2}\n\n{3}'.format(user_name, user_age, user_city, user_description))
    BOT.send_message(msg.chat.id, 'Все верно?',
                     reply_markup=profile_maker_show_result_keyboard())
    
def profile_maker_show_result_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton(STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS[0]))
    markup.add(KeyboardButton(STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS[1]))
    return markup

# ------ #
# SEARCH #
# ------ #

def search_loop(msg):
    return

# --------------------------------------------------------------------------- #
# ENTRY POINT                                                                 #
# --------------------------------------------------------------------------- #

if (__name__ == '__main__'):
    BOT.infinity_polling()