# --------------------------- #
#      Written by KIRYA       #
#   Created on: 14.03.2025    #
# Last updated on: 17.03.2025 #
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

BOT_TOKEN = '<place-your-bot-token-here>'
BOT = TeleBot(BOT_TOKEN)

# ------ #
# STATES #
# ------ #

current_state = None
STATES = [
    'start', 'profile_maker_age', 'profile_maker_sex',
    'profile_maker_preffered_sex', 'profile_maker_city', 'profile_maker_name',
    'profile_maker_description', 'profile_maker_photo_video', 'profile_maker_show_result',
     'search_loop', 'write_to_user', 'sleep_mode',
    'my_profile', 'delete_profile_ask', 'delete_profile'
    ]

# --------------- #
# ALLOWED ANSWERS #
# --------------- #

STATE_START_ALLOWED_ANSWERS = ['👍']
STATE_SEX_ALLOWED_ANSWERS = ['Я — парень', 'Я — девушка']
STATE_PREFFERED_SEX_ALLOWED_ANSWERS = ['Девушки', 'Парни', 'Все равно']
STATE_PHOTO_VIDEO_ALLOWED_ANSWERS = ['Продолжить без фото']
STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS = ['Да', 'Изменить анкету']
STATE_SEARCH_LOOP_ALLOWED_ANSWERS = ['❤️', '💌', '👎', '💤']
STATE_WRITE_TO_USER_ALLOWED_ANSWERS = ['Вернуться назад']
STATE_SLEEP_MODE_ALLOWED_ANSWERS = ['1', '2', '3']
STATE_MY_PROFILE_ALLOWED_ANSWERS = ['1 🚀', '2']
STATE_DELETE_PROFILE_ALLOWED_ANSWERS = ['😴 Удалить анкету', '← Назад']
STATE_POST_DELETION_ALLOWED_ANSWERS = ['СТАРТ']

# -------------------- #
# USER'S PROFILE CLASS #
# -------------------- #

class BotUser:
    def __init__(
            self, age=None, sex=None,
            preffered_sex=None, city=None, name=None,
            description=None, photo_video=None):
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

local_profiles = []
main_profiles_list = []
filtered_profiles = []
seen_profiles = []

# --------------------------------------------------------------------------- #
# SYSTEM FUNCTIONS                                                            #
# --------------------------------------------------------------------------- #

def bot_create_reply_keyboard(options_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(option) for option in options_list]
    keyboard.add(*buttons)
    return keyboard
    
def bot_wrong_answer(msg):
    BOT.send_message(msg.chat.id, 'Нет такого варианта ответа. Пожалуйста, попробуй еще раз.')
    
def bot_wrong_input(msg):
    BOT.send_message(msg.chat.id, 'Некорректный ввод. Пожалуйста, попробуй еще раз.')

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
            if (msg.content_type == 'text'):
                if (not msg.text.isdigit()):
                    BOT.send_message(msg.chat.id, 'Укажи правильный возраст. Только цифры.')
                else:
                    main_user.age = msg.text
                    current_state = STATES[2]
                    profile_maker_sex(msg)
            else:
                bot_wrong_input(msg)
            
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
                        main_user.preffered_sex = 'female'
                    case 'Парни':
                        main_user.preffered_sex = 'male'
                    case 'Все равно':
                        main_user.preffered_sex = 'everyone'
                current_state = STATES[4]
                profile_maker_city(msg)
            else:
                bot_wrong_answer(msg)
            
        case 'profile_maker_city':
            if (msg.content_type == 'text'):
                if (not msg.text.isalpha()):
                    BOT.send_message(msg.chat.id, 'Укажи правильное название города. Только буквы.')
                else:
                    main_user.city = msg.text
                    current_state = STATES[5]
                    profile_maker_name(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_name':
            if (msg.content_type == 'text'):
                if (not msg.text.isalpha()):
                    BOT.send_message(msg.chat.id, 'Укажи правильное имя. Только буквы.')
                else:
                    main_user.name = msg.text
                    current_state = STATES[6]
                    profile_maker_description(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_description':
            if (msg.content_type == 'text'):
                if (len(msg.text) > 900):
                    BOT.send_message(msg.chat.id, 'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
                else:
                    main_user.description = msg.text
                    current_state = STATES[7]
                    profile_maker_photo_video(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_photo_video':
            if (not msg.content_type == 'photo'):
                if (msg.text in STATE_PHOTO_VIDEO_ALLOWED_ANSWERS):
                    match msg.text:
                        case 'Продолжить без фото':
                            current_state = STATES[8]
                            profile_maker_show_result(msg)
                else:
                    BOT.send_message(msg.chat.id, 'Не удалось загрузить фото. Попробуй еще раз.')
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
            if (msg.content_type == 'text'):
                if (msg.text in STATE_WRITE_TO_USER_ALLOWED_ANSWERS):
                    match msg.text:
                        case 'Вернуться назад':
                            current_state = STATES[9]
                            search_loop(msg)
                else:
                    if (len(msg.text) > 900):
                        BOT.send_message(msg.chat.id,
                                         'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
                    else:
                        BOT.send_message(msg.chat.id, 'Лайк отправлен, ждем ответа.')
                        current_state = STATES[9]
                        search_loop(msg)
            else:
                bot_wrong_input(msg)
            
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
                    case '← Назад':
                        current_state = STATES[12]
                        my_profile(msg)
            else:
                bot_wrong_answer(msg)
                
        case 'delete_profile':
            if (msg.text in STATE_POST_DELETION_ALLOWED_ANSWERS):
                match msg.text:
                    case 'СТАРТ':
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
    global local_profiles
    global main_profiles_list
    global filtered_profiles
    global seen_profiles
    
    if (not main_user.photo_video is None):
        main_user.photo_video = None
    
    if (local_profiles):
        local_profiles.clear()
        
    if (main_profiles_list):
        main_profiles_list.clear()
        
    if (filtered_profiles):
        filtered_profiles.clear()
        
    if (seen_profiles):
        seen_profiles.clear()
    
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
    BOT.send_message(msg.chat.id, 'Теперь пришли фото 👍 — его будут видеть другие пользователи.',
                     reply_markup=bot_create_reply_keyboard(STATE_PHOTO_VIDEO_ALLOWED_ANSWERS))
    
def profile_maker_show_result(msg):
    BOT.send_message(msg.chat.id, 'Так выглядит твоя анкета:')
    if (not main_user.photo_video is None):
        BOT.send_photo(msg.chat.id, main_user.photo_video.photo[-1].file_id,
                       '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    else:
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id, 'Все верно?',
                     reply_markup=bot_create_reply_keyboard(STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS))

# ------ #
# SEARCH #
# ------ #

def search_loop(msg):
    global local_profiles
    global main_profiles_list
    global filtered_profiles
    global seen_profiles
    
    profile_to_show = None
    
    if (not local_profiles):
        for profile in fake_profiles:
            if (profile.city == main_user.city):
                local_profiles.append(profile)
    
    if (not main_profiles_list):
        if (local_profiles):
            main_profiles_list = local_profiles
        else:
            BOT.send_message(msg.chat.id,
                             'К сожалению, я не нашел пользователей из твоего города :(\nНо я могу показать тебе всех остальных!')
            main_profiles_list = fake_profiles
    
    if (not filtered_profiles):
        for profile in main_profiles_list:
            if (profile.sex == main_user.preffered_sex) or (main_user.preffered_sex == 'everyone'):
                filtered_profiles.append(profile)
    
    if (set(filtered_profiles).issubset(seen_profiles)):
        seen_profiles.clear()
    
    for profile in filtered_profiles:
        if (not profile in seen_profiles):
            seen_profiles.append(profile)
            profile_to_show = profile
            break
    
    if (profile_to_show.photo_video is None):
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(profile_to_show.name, profile_to_show.age, profile_to_show.city, profile_to_show.description),
                         reply_markup=bot_create_reply_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    else:
        BOT.send_photo(msg.chat.id, profile_to_show.photo_video,
                       '{0}, {1}, {2}\n\n{3}'.format(profile_to_show.name, profile_to_show.age, profile_to_show.city, profile_to_show.description),
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
    if (not main_user.photo_video is None):
        BOT.send_photo(msg.chat.id, main_user.photo_video.photo[-1].file_id,
                       '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    else:
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id, '1. Смотреть анкеты.\n2. Заполнить анкету заново.',
                     reply_markup=bot_create_reply_keyboard(STATE_MY_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile_ask(msg):
    BOT.send_message(msg.chat.id, 'Так ты не узнаешь, что кому-то нравишься... Точно хочешь удалить свою анкету?',
                     reply_markup=bot_create_reply_keyboard(STATE_DELETE_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile(msg):
    BOT.send_message(msg.chat.id, 'Надеюсь, ты нашел кого-то благодаря мне! Рад был с тобой пообщаться, будет скучно — пиши, обязательно найдем тебе кого-нибудь!',
                     reply_markup=bot_create_reply_keyboard(STATE_POST_DELETION_ALLOWED_ANSWERS))

# --------------------------------------------------------------------------- #
# ENTRY POINT                                                                 #
# --------------------------------------------------------------------------- #

if (__name__ == '__main__'):
    main_user = BotUser()
    
    fake_profile_1 = BotUser('18', 'male', 'female',
                             'Москва', 'Модный чел', 'чисто девчонку чтоб завалиться в клуб побухать аее))',
                             'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/1.jpg')
    
    fake_profile_2 = BotUser('23', 'female', 'male',
                             'Москва', 'Девушка мечты', 'Учусь в Литературном институте, интересуюсь вышиванием и танцами. Хочу сходить на свидание с милым парнем ^^',
                             'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/2.jpg')
    
    fake_profile_3 = BotUser('44', 'female', 'male',
                             'Ижевск', 'Лидия', 'Ищу верного, надежного мужчину для построения семьи! Есть ребенок!',
                             'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/3.jpg')
    
    fake_profile_4 = BotUser('53', 'male', 'everyone',
                             'Москва', 'Владимир Ульянов', 'Товарищи! Не верьте всему тому, что пишут в интернете!',
                             'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/4.jpg')
    
    fake_profile_5 = BotUser('32', 'female', 'everyone',
                             'Сочи', 'Катя', 'Хотелось бы найти друзей, с которыми можно будет ходить гулять по нашему чудесному городу)\n\nP. S. Отношения не интересуют, так как есть молодой человек.',
                             'https://raw.githubusercontent.com/iamgonnafindawaytomakeit/leomatch_clone_bot/refs/heads/main/fake_users/5.jpg')
    
    fake_profiles = [
        fake_profile_1, fake_profile_2, fake_profile_3,
        fake_profile_4, fake_profile_5
        ]
    
    BOT.infinity_polling()