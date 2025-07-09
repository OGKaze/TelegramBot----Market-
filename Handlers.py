from aiogram import F,Router
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,Command
import App.Keyboard as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    PhoneNumber = State()

@router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('Здарова',reply_markup=kb.main)
    await message.reply('Иди нахуй')


@router.message(Command('Help'))
async def cmd_Help(message:Message):
    await message.answer('Кто в слове негр букву г перевернул?')

@router.message(Command('Данил'))
async def cmd_Danil(message: Message):
        await message.answer('Найди работу')

@router.message(Command('Кирилл'))
async def cmd_Cyr(message: Message):
        await message.answer('Хуячь в АРМИЮ')

@router.message(F.text == 'Каталог')
async def catalog(message:Message):
    await message.answer('Выберите категорию:',
                         reply_markup=kb.catalog)

@router.callback_query(F.data =='t-shirt')
async def t_shirt(callback:CallbackQuery):
    await callback.answer('Вы выбрали категорию',show_alert=True)
    await callback.message.answer('Вы выбрали категорию футболок')


@router.message(Command('register'))
async def register(message:Message,state:FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя')

@router.message(Register.name)
async def register_name(message:Message,state:FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer('Введите ваш возраст')

@router.message(Register.age)
async def register_age(message:Message,state:FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.PhoneNumber)
    await message.answer('Введите ваш номер телефона',reply_markup=kb.get_number)

@router.message(Register.PhoneNumber,F.contact)
async def register_pn(message:Message,state:FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f'Ваше имя:{data["name"]} \n Ваш возраст:{data["age"]} \n Ваш номер телефона{data["number"]}')
    await  state.clear()