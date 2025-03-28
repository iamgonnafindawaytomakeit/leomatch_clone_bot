# --------------------------- #
#      Written by KIRYA       #
#   Created on: 14.03.2025    #
# Last updated on: 22.03.2025 #
# --------------------------- #

# --------------------------------------------------------------------------- #
# THIRD-PARTY LIBRARIES                                                       #
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

current_state = ''
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
STATE_PHOTO_VIDEO_ALLOWED_ANSWERS = ['Продолжить без фото/видео']
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
            self, age='', sex='',
            preffered_sex='', city='', name='',
            description='', photo=None, video=None):
        self.age = age
        self.sex = sex
        self.preffered_sex = preffered_sex
        self.city = city
        self.name = name
        self.description = description
        self.photo = photo
        self.video = video

# ------ #
# SEARCH #
# ------ #

local_suitable_profiles = []
nonlocal_suitable_profiles = []
main_profiles_list = []
seen_profiles = []

# ------------- #
# FAKE DATABASE #
# ------------- #

main_user = None

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

# --------------------------------------------------------------------------- #
# SYSTEM FUNCTIONS                                                            #
# --------------------------------------------------------------------------- #

def bot_create_keyboard(options_list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                   row_width=4)
    buttons = [KeyboardButton(option) for option in options_list]
    keyboard.add(*buttons)
    return keyboard
    
def bot_wrong_answer(msg):
    BOT.send_message(msg.chat.id,
                     'Нет такого варианта ответа. Пожалуйста, попробуй еще раз.')
    
def bot_wrong_input(msg):
    BOT.send_message(msg.chat.id,
                     'Некорректный ввод. Пожалуйста, попробуй еще раз.')

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
                     reply_markup=bot_create_keyboard(STATE_START_ALLOWED_ANSWERS))

# --------------------------------------------------------------------------- #
# HANDLERS                                                                    #
# --------------------------------------------------------------------------- #

# ---------------- #
# MESSAGES HANDLER #
# ---------------- #

@BOT.message_handler(func = lambda msg: True, content_types=['text', 'photo', 'video'])
def messages_handler(msg):
    global current_state
    
    match current_state:
        
        case 'start':
            if (msg.text in STATE_START_ALLOWED_ANSWERS):
                match msg.text:
                    case '👍':
                        current_state = STATES[1]
                        profile_maker_init(msg)
            else:
                bot_wrong_answer(msg)
                        
        case 'profile_maker_age':
            if (msg.content_type == 'text'):
                if (not msg.text.isdigit()):
                    BOT.send_message(msg.chat.id,
                                     'Укажи правильный возраст. Только цифры.')
                else:
                    if (int(msg.text) > 110):
                        BOT.send_message(msg.chat.id,
                                         'Укажи настоящий возраст.')
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
                    BOT.send_message(msg.chat.id,
                                     'Укажи правильное название города. Только буквы.')
                else:
                    main_user.city = msg.text
                    current_state = STATES[5]
                    profile_maker_name(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_name':
            if (msg.content_type == 'text'):
                if (not msg.text.isalpha()):
                    BOT.send_message(msg.chat.id,
                                     'Укажи правильное имя. Только буквы.')
                else:
                    main_user.name = msg.text
                    current_state = STATES[6]
                    profile_maker_description(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_description':
            if (msg.content_type == 'text'):
                if (len(msg.text) > 900):
                    BOT.send_message(msg.chat.id,
                                     'Слишком длинное описание. Лимит — 900 знаков (включая пробелы).')
                else:
                    main_user.description = msg.text
                    current_state = STATES[7]
                    profile_maker_photo_video(msg)
            else:
                bot_wrong_input(msg)
            
        case 'profile_maker_photo_video':
            match msg.content_type:
                case 'text':
                    if (msg.text in STATE_PHOTO_VIDEO_ALLOWED_ANSWERS):
                        match msg.text:
                            case 'Продолжить без фото/видео':
                                current_state = STATES[8]
                                profile_maker_show_result(msg)
                    else:
                        bot_wrong_answer(msg)
                case 'photo':
                    main_user.photo = msg
                    current_state = STATES[8]
                    profile_maker_show_result(msg)
                case 'video':
                    main_user.video = msg
                    current_state = STATES[8]
                    profile_maker_show_result(msg)
                case _:
                    bot_wrong_input(msg)
            
        case 'profile_maker_show_result':
            if (msg.text in STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS):
                match msg.text:
                    case 'Да':
                        current_state = STATES[9]
                        search_loop(msg)
                    case 'Изменить анкету':
                        current_state = STATES[1]
                        profile_maker_init(msg)
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
                        BOT.send_message(msg.chat.id,
                                         'Лайк отправлен, ждем ответа.')
                        current_state = STATES[9]
                        search_loop(msg)
            else:
                bot_wrong_input(msg)
            
        case 'sleep_mode':
            if (msg.text in STATE_SLEEP_MODE_ALLOWED_ANSWERS):
                match msg.text:
                    case '1':
                        BOT.send_message(msg.chat.id,
                                         '✨🔍')
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
                        BOT.send_message(msg.chat.id,
                                         '✨🔍')
                        current_state = STATES[9]
                        search_loop(msg)
                    case '2':
                        current_state = STATES[1]
                        profile_maker_init(msg)
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

def profile_maker_init(msg):
    global main_user
    global local_suitable_profiles
    global nonlocal_suitable_profiles
    global main_profiles_list
    global seen_profiles
    
    main_user = BotUser()
    
    if (local_suitable_profiles):
        local_suitable_profiles = []
        
    if (nonlocal_suitable_profiles):
        nonlocal_suitable_profiles = []
        
    if (main_profiles_list):
        main_profiles_list = []
        
    if (seen_profiles):
        seen_profiles = []
        
    profile_maker_age(msg)

def profile_maker_age(msg):    
    BOT.send_message(msg.chat.id,
                     'Сколько тебе лет?')
    
def profile_maker_sex(msg):
    BOT.send_message(msg.chat.id,
                     'Теперь определимся с полом.',
                     reply_markup=bot_create_keyboard(STATE_SEX_ALLOWED_ANSWERS))
    
def profile_maker_preffered_sex(msg):
    BOT.send_message(msg.chat.id,
                     'Кто тебе интересен?',
                     reply_markup=bot_create_keyboard(STATE_PREFFERED_SEX_ALLOWED_ANSWERS))
    
def profile_maker_city(msg):
    BOT.send_message(msg.chat.id,
                     'Из какого ты города?')
    
def profile_maker_name(msg):
    BOT.send_message(msg.chat.id,
                     'Как мне тебя называть?')
    
def profile_maker_description(msg):
    BOT.send_message(msg.chat.id,
                     'Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. Это поможет лучше подобрать тебе компанию.')
    
def profile_maker_photo_video(msg):
    BOT.send_message(msg.chat.id,
                     'Теперь пришли фото или видео 👍 — его будут видеть другие пользователи.',
                     reply_markup=bot_create_keyboard(STATE_PHOTO_VIDEO_ALLOWED_ANSWERS))
    
def profile_maker_show_result(msg):
    BOT.send_message(msg.chat.id,
                     'Так выглядит твоя анкета:')
    if (not main_user.photo is None):
        BOT.send_photo(msg.chat.id, main_user.photo.photo[-1].file_id,
                       '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    elif (not main_user.video is None):
        BOT.send_video(msg.chat.id, main_user.video.video.file_id,
                       caption='{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    else:
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id,
                     'Все верно?',
                     reply_markup=bot_create_keyboard(STATE_PROFILE_MAKER_SHOW_RESULTS_ALLOWED_ANSWERS))

# ------ #
# SEARCH #
# ------ #

def search_loop(msg):
    global local_suitable_profiles
    global nonlocal_suitable_profiles
    global main_profiles_list
    global seen_profiles
    
    profile_to_show = None
    
    if ((not local_suitable_profiles) and (not nonlocal_suitable_profiles)):
        for profile in fake_profiles:
            if ((profile.sex == main_user.preffered_sex)
                    or (main_user.preffered_sex == 'everyone')):
                if (profile.city == main_user.city):
                    if (main_profiles_list):
                        main_profiles_list = []
                    local_suitable_profiles.append(profile)
                else:
                    if (main_profiles_list):
                        main_profiles_list = []
                    nonlocal_suitable_profiles.append(profile)
                    
    if (not main_profiles_list):
        if (local_suitable_profiles):
            main_profiles_list = local_suitable_profiles
        elif (nonlocal_suitable_profiles):
            BOT.send_message(msg.chat.id,
                             'Я не смог найти пользователей, соответствующих твоим требованиям, в твоем городе :(\nПопробую поискать в других местах...')
            main_profiles_list = nonlocal_suitable_profiles
        else:
            BOT.send_message(msg.chat.id,
                             'Я не смог найти пользователей, соответствующих твоим требованиям :(\nНо я могу показать все имеющиеся в базе профили!')
            main_profiles_list = fake_profiles
            
    if (set(main_profiles_list).issubset(seen_profiles)):
        seen_profiles = []
    
    for profile in main_profiles_list:
        if (not profile in seen_profiles):
            seen_profiles.append(profile)
            profile_to_show = profile
            break
    
    if (not profile_to_show.photo is None):
        BOT.send_photo(msg.chat.id, profile_to_show.photo,
                       '{0}, {1}, {2}\n\n{3}'.format(profile_to_show.name, profile_to_show.age, profile_to_show.city, profile_to_show.description),
                       reply_markup=bot_create_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    elif (not profile_to_show.video is None):
        BOT.send_video(msg.chat.id, profile_to_show.video,
                       caption='{0}, {1}, {2}\n\n{3}'.format(profile_to_show.name, profile_to_show.age, profile_to_show.city, profile_to_show.description),
                       reply_markup=bot_create_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    else:
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(profile_to_show.name, profile_to_show.age, profile_to_show.city, profile_to_show.description),
                         reply_markup=bot_create_keyboard(STATE_SEARCH_LOOP_ALLOWED_ANSWERS))
    
def write_to_user(msg):
    BOT.send_message(msg.chat.id,
                     'Напиши сообщение для этого пользователя:',
                     reply_markup=bot_create_keyboard(STATE_WRITE_TO_USER_ALLOWED_ANSWERS))
    
def sleep_mode(msg):
    BOT.send_message(msg.chat.id,
                     'Подождем, пока кто-то увидит твою анкету.')
    BOT.send_message(msg.chat.id,
                     '1. Смотреть анкеты.\n2. Моя анкета.\n3. Я больше не хочу никого искать.',
                     reply_markup=bot_create_keyboard(STATE_SLEEP_MODE_ALLOWED_ANSWERS))

def my_profile(msg):
    BOT.send_message(msg.chat.id,
                     'Так выглядит твоя анкета:')
    if (not main_user.photo is None):
        BOT.send_photo(msg.chat.id, main_user.photo.photo[-1].file_id,
                       '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    elif (not main_user.video is None):
        BOT.send_video(msg.chat.id, main_user.video.video.file_id,
                       caption='{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    else:
        BOT.send_message(msg.chat.id,
                         '{0}, {1}, {2}\n\n{3}'.format(main_user.name, main_user.age, main_user.city, main_user.description))
    BOT.send_message(msg.chat.id,
                     '1. Смотреть анкеты.\n2. Заполнить анкету заново.',
                     reply_markup=bot_create_keyboard(STATE_MY_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile_ask(msg):
    BOT.send_message(msg.chat.id,
                     'Так ты не узнаешь, что кому-то нравишься... Точно хочешь удалить свою анкету?',
                     reply_markup=bot_create_keyboard(STATE_DELETE_PROFILE_ALLOWED_ANSWERS))
    
def delete_profile(msg):
    BOT.send_message(msg.chat.id,
                     'Надеюсь, ты нашел кого-то благодаря мне! Рад был с тобой пообщаться, будет скучно — пиши, обязательно найдем тебе кого-нибудь!',
                     reply_markup=bot_create_keyboard(STATE_POST_DELETION_ALLOWED_ANSWERS))

# --------------------------------------------------------------------------- #
# ENTRY POINT                                                                 #
# --------------------------------------------------------------------------- #

if (__name__ == '__main__'):
    BOT.infinity_polling()