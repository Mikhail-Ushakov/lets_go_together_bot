import asyncio
import logging

from config_reader import config

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, FSInputFile
# from aiogram.filters.command import Command
from aiogram.filters import Command, StateFilter, CommandObject, or_f
from aiogram.enums import ParseMode


API_TOKEN = config.bot_token.get_secret_value()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

users = {}

LIST_INTERESTS = [
    ['спорт', 'музыка', 'вечеринки', 'IT'], 
    ['путешествия', 'природа', 'волонтерство', 'развлечения'], 
    ['искусство', 'астрология', 'кино', 'еда'], 
    ['прогулки']
]

class ProfileForm(StatesGroup):
    name = State()
    age = State()
    city = State()
    photo = State()
    description = State()
    interests = State()


def get_main_kb():
    kb = [[types.KeyboardButton(text='Кнопка заглушка')]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@dp.message(Command("start"))
async def start(message: types.Message):
    kb = [
        [types.KeyboardButton(text='Заполнить свой профиль')]
    ]
    
    if message.from_user.language_code == "ru":
        markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Этот бот поможет тебе найти напарника для спорта, творчества, компанию для похода в бар или просто собеседника! Заполни профиль и приступай к поиску!", reply_markup=markup)
    else:
        markup = ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Fill out Profile")]], resize_keyboard=True)
        await message.answer("This bot will help you find a partner for sports, creativity, company for going to the bar or just a companion! Fill out your profile and start searching!", reply_markup=markup)
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {'name': 'Аноним', 'age': '', 'city': '', 'photo': '', 'description': '', 'liked': [], 'interests': []}
        photo = FSInputFile("default_avatar.png")
        await message.answer('Так выглядит твоя анкета:')
        answer = await message.answer_photo(
            photo=photo,
            caption=users[user_id].get("name")
        )
        users[user_id].update(photo=answer.photo[-1].file_id)
        await message.answer('Давай заполним ее!')





@dp.message(Command("profile"))
async def get_profile(message: types.Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    user = users.get(user_id)
    file_id = user.get('photo')
    await message.answer('Так выглядит твоя анкета:')
    await message.answer_photo(
        photo=file_id,
        caption=f'''{"🟢" if user.get("interests") else ""}{"🟢".join([i for i in user.get("interests") if i])}

{user.get("name")}{', ' if user.get("age") else ""}{user.get("age")}{', ' if user.get("city") else ""}{user.get("city")}

{user.get("description")}''',
        reply_markup=get_main_kb()
    )

@dp.message(Command("interests"))
async def set_interests(message: types.Message, state: FSMContext):
    list_callbacks = [
        [types.InlineKeyboardButton(text=col, callback_data=col) for col in row] for row in LIST_INTERESTS
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=list_callbacks)
    await state.clear()
    await message.answer(
        text="Введите интересы, по которым вы ищите спутника, партнера, напарника и т.д.\nЕсли их несколько, пожалуйста, через запятую:", 
        reply_markup=keyboard
    )


    #DOOOOOOOOOOOOOOOOOOOOOOOOOO
    await message.answer(text='', reply_markup=ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text='Отмена')]]
        ))
    await state.set_state(ProfileForm.interests) 

@dp.message(ProfileForm.interests)
async def set_city(message: types.Message, state: FSMContext):
    user_interests = list(map(lambda el: el.strip(' .!&*:;').lower().capitalize(), message.text.split(',')))
    print(user_interests)
    # await state.update_data(interests=user_interests)
    # user_data = await state.get_data()
    user_id = message.from_user.id
    users[user_id].update(interests=user_interests)
    await get_profile(message, state)


@dp.message(F.text.lower() == "отмена")
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await state.clear()
    await message.answer(
        text="Действие отменено" if current_state else "Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )
    await get_profile(message, state)


@dp.message(StateFilter(None), Command("edit"))
@dp.message(StateFilter(None), or_f(F.text == "Заполнить свой профиль", F.text == "Fill out Profile"))
async def set_name(message: types.Message, state: FSMContext):
    await message.answer("Please enter your name:", 
                         reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[types.KeyboardButton(text='Отмена')]]
                                                )
                                        
    )
    await state.set_state(ProfileForm.name) 

@dp.message(ProfileForm.name, ~F.text.startswith('/'), F.text.len() <= 30)
async def set_name_done(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Please enter your age:")
    await state.set_state(ProfileForm.age) 

@dp.message(ProfileForm.name)
async def set_name_incorrectly(message: types.Message, state: FSMContext):    
    await message.answer("Имя не должно начинаться с '/' и количество символов должно быть не более 30" )


@dp.message(ProfileForm.age, F.text.regexp(r'^[1-9][0-9]?$|^100$'))
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Please enter your city:")
    await state.set_state(ProfileForm.city)

@dp.message(ProfileForm.age)
async def set_age_incorrectly(message: types.Message, state: FSMContext):    
    await message.answer("Введите корректный возраст")


@dp.message(ProfileForm.city, ~F.text.startswith('/'), F.text.len() <= 30)
async def set_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id
    users[user_id].update(**user_data)
    await get_profile(message, state)
    # await state.clear()

@dp.message(ProfileForm.city)
async def set_city_incorrectly(message: types.Message, state: FSMContext):    
    await message.answer("Город не должно начинаться с '/' и количество символов должно быть не более 30" )


@dp.message(Command('changephoto'))
async def set_photo(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Please send your photo:",
                         reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[types.KeyboardButton(text='Отмена')]]
                                                ))
    await state.set_state(ProfileForm.photo)

@dp.message(ProfileForm.photo, F.photo)
async def set_photo_done(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await state.update_data(photo=file_id)
    user_data = await state.get_data()
    user_id = message.from_user.id
    users[user_id].update(**user_data)
    # await state.clear()
    await get_profile(message, state)

@dp.message(ProfileForm.photo)
async def set_photo_incorrectly(message: types.Message, state: FSMContext):    
    await message.answer("Не похоже на фоточку")






@dp.message(Command('changedescription'))
async def set_description(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Опишите что хотите:",
                         reply_markup=ReplyKeyboardMarkup(
                                                    keyboard=[[types.KeyboardButton(text='Отмена')]]
                                                ))
    await state.set_state(ProfileForm.description)

@dp.message(ProfileForm.description)
async def set_description_done(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    user_data = await state.get_data()
    user_id = message.from_user.id
    users[user_id].update(**user_data)
    await get_profile(message, state)
    # await state.clear()






@dp.message(lambda message: message.text == "Browse Profiles")
async def browse_profiles(message: types.Message):
    # Implement code to browse other users' profiles
    pass

@dp.message(lambda message: message.text == "Swipe")
async def swipe_profile(message: types.Message):
    # Implement code to swipe on profiles
    pass

@dp.message(lambda message: message.text == "My Matches")
async def my_matches(message: types.Message):
    # Implement code to display matched profiles and enable communication
    pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())