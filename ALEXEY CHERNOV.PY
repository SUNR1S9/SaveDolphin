#aiogram версия дл 2.5
import datetime
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
#Бот сделан Алексеем Черновым МБОУ ТЭЛ



# Создаем экземпляр бота и диспетчер
bot_token = 'TOKEN'
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Определяем состояние для обработки передачи геолокации
class GeolocationState(StatesGroup):
    waiting_for_location = State()
    waiting_for_photo = State()
    waiting_for_question_answer = State()

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [
        types.KeyboardButton('🐬 Контакты для связи 🐬'),
        types.KeyboardButton('🐬 Получить информацию 🐬'),
        types.KeyboardButton('🐬 Передать информацию 🐬')
    ]
    keyboard.add(*buttons)
    await message.answer('Здравствуйте! \n 🐬🐬🐬 Этот сервис разработан для помощи дельфинам на берегу Черного моря и сбора статистических данных.\nВыбрав соответствующие кнопки ниже, Вы можете получить полезную информацию, связаться с нами или передать нужную нам информацию о состоянии животного.', reply_markup=keyboard)

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик кнопки "Контакты"
@dp.message_handler(lambda message: message.text == '🐬 Контакты для связи 🐬')
async def contacts(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    await message.answer('Если Вы хотите связаться с волонтерами, выберете один из способов: \n Центр 1: \n e-mail: acher3442@gmail.com \n номер тел.: [+79991234567] \n Центр 2: \n e-mail: acher3442@gmail.com \n номер тел.: [+79991234567]', reply_markup=keyboard)
#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик кнопки "Получить информацию"
@dp.message_handler(lambda message: message.text == '🐬 Получить информацию 🐬')
async def get_info(message: types.Message):
    # Обработчик кнопки "Получить информацию"
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)

    await message.answer('По ссылке ниже Вы можете перейти на официальный сайт центра «ДЕЛЬФА»:  https://delfacenter.org/', reply_markup=keyboard)
    await message.answer('По ссылке ниже Вы можете перейти на официальный сайт центра «БЕЗМЯТЕЖНОЕ МОРЕ»: https://serenesea.org/', reply_markup=keyboard)
#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик кнопки "Передать информацию"
@dp.message_handler(lambda message: message.text == '🐬 Передать информацию 🐬')
async def send_info(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    geolocation_button = types.KeyboardButton('📍 Отправить местоположение')
    photo_button = types.KeyboardButton('📎 Отправить фото/видео')
    questions_button = types.KeyboardButton('📝 Отправить информацию')
    back_button = types.KeyboardButton('Назад')
    keyboard.add(geolocation_button, photo_button, questions_button, back_button)
    await message.answer('Выберите способ передачи информации:', reply_markup=keyboard)

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик кнопки "Передать геолокацию"
@dp.message_handler(lambda message: message.text == '📍 Отправить местоположение')
async def send_geolocation(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    await message.answer('Пожалуйста, отправьте свою геолокацию. Для этого нажмите иконку скрепки 📎 и выберите во всплывающем меню пункты «Геопозиция» или «Место» 📍', reply_markup=keyboard)
    await GeolocationState.waiting_for_location.set()

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик геолокации
@dp.message_handler(content_types=['location'], state=GeolocationState.waiting_for_location)
async def handle_location(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    latitude = message.location.latitude
    longitude = message.location.longitude
    # Бот сделан Алексеем Черновым МБОУ ТЭЛ
    # Запись данных в таблицу excel
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [time, message.from_user.username, latitude, longitude, '', '', '', '']
    save_to_excel(data)

    await message.answer('Геолокация успешно передана!', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text="/start")
#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик кнопки "Передать фото"
@dp.message_handler(lambda message: message.text == '📎 Отправить фото/видео')
async def send_photo(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    back_button = types.KeyboardButton('Назад')
    keyboard.add(back_button)
    await message.answer('Пожалуйста, отправьте фото:', reply_markup=keyboard)
    await GeolocationState.waiting_for_photo.set()

#Бот сделан Алексеем Черновым МБОУ ТЭЛ
# Обработчик фото
@dp.message_handler(content_types=['photo'], state=GeolocationState.waiting_for_photo)
async def handle_photo(message: types.Message, state: FSMContext):
    # Сохранение фото на диск
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    photo_dir = 'photos'
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)
    photo_file = f'{photo_dir}/{timestamp}.jpg'
    await message.photo[-1].download(photo_file)
    # Бот сделан Алексеем Черновым МБОУ ТЭЛ
    # Запись данных в таблицу excel
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [time, message.from_user.username, '', '', photo_file, '', '', '']
    save_to_excel(data)

    await message.answer('Фото успешно передано!', reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text="/start")

# Обработчик кнопки "Ответить на вопросы"
@dp.message_handler(lambda message: message.text == '📝 Отправить информацию')
async def answer_questions(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    yes_button = types.KeyboardButton('Да')
    no_button = types.KeyboardButton('Нет')
    unsure_button = types.KeyboardButton('Не знаю')
    back_button = types.KeyboardButton('Назад')
    keyboard.add(yes_button, no_button, unsure_button, back_button)

    await message.answer('Ответьте на следующие вопросы:', reply_markup=keyboard)
    await GeolocationState.waiting_for_question_answer.set()
    await message.answer('Есть ли у животного дыхание?')


# Обработчик ответа на вопросы
@dp.message_handler(lambda message: message.text in ['Да', 'Нет', 'Не знаю'], state=GeolocationState.waiting_for_question_answer)
async def handle_question_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not data.get('question1'):
            data['question1'] = message.text
            await message.answer('Двигает ли животное глазами?')
        elif not data.get('question2'):
            data['question2'] = message.text
            await message.answer('Животное движется самостоятельно?')
        else:
            data['question3'] = message.text

            # Запись данных в таблицу excel
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = message.from_user.username
            latitude = data.get('latitude', '')
            longitude = data.get('longitude', '')
            photo_file = data.get('photo_file', '')
            question1 = 1 if data.get('question1') == 'Да' else -1 if data.get('question1') == 'Нет' else 0
            question2 = 1 if data.get('question2') == 'Да' else -1 if data.get('question2') == 'Нет' else 0
            question3 = 1 if data.get('question3') == 'Да' else -1 if data.get('question3') == 'Нет' else 0

            save_to_excel([time, user, latitude, longitude, photo_file, question1, question2, question3])

            await message.answer('Ответы успешно переданы!', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
            await bot.send_message(chat_id=message.chat.id, text="/start")

# Обработчик кнопки "Назад"
@dp.message_handler(lambda message: message.text == 'Назад')
async def back(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [
        types.KeyboardButton('🐬 Контакты для связи 🐬'),
        types.KeyboardButton('🐬 Получить информацию 🐬'),
        types.KeyboardButton('🐬 Передать информацию 🐬')
    ]
    keyboard.add(*buttons)
    await message.answer(
        'Здравствуйте! \n 🐬🐬🐬 Этот сервис разработан для помощи дельфинам на берегу Черного моря и сбора статистических данных.\nВыбрав соответствующие кнопки ниже, Вы можете получить полезную информацию, связаться с нами или передать нужную нам информацию о состоянии животного.',
        reply_markup=keyboard)

# Функция для записи данных в таблицу Excel
def save_to_excel(data):
    import openpyxl
    excel_file = 'data.xlsx'

    if not os.path.exists(excel_file):
        wb = openpyxl.Workbook()
        ws = wb.active
        headers = ["Время", "Имя пользователя", "Широта", "Долгота", "Ссылка на фото", "Вопрос 1", "Вопрос 2", "Вопрос 3"]
        ws.append(headers)
        wb.save(excel_file)

    wb = openpyxl.load_workbook(excel_file)
    ws = wb.active
    ws.append(data)
    wb.save(excel_file)

# Запускаем бота
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(dp.start_polling())
    finally:
        loop.run_until_complete(dp.bot.session.close())
        loop.close()

