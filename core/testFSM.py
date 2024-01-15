from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
from aiogram import Dispatcher, F
from db_funcs import admin_db, user_db, maps_db
from check_conditions import is_user_exist
from settings import PATH_TO_TEMP_FILES
from bot_initialize import bot
from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class GoShopping(StatesGroup):
    big_purchase = State()
    mid_purchase = State()
    small_purchase = State()


async def go_shopping(msg: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    monitor = InlineKeyboardButton(text='Монитор', callback_data='big_монитор')
    car = InlineKeyboardButton(text='Машина', callback_data='big_машина')
    builder.add(monitor, car)
    await msg.answer("Большая покупка", reply_markup=builder.as_markup())
    await state.set_state(GoShopping.big_purchase)


async def big_buttons(callback: CallbackQuery, state: FSMContext):
    _, purchase = callback.data.split('_')
    await callback.message.answer(f'Вы выбрали {purchase}')
    await state.update_data(big_purchase=purchase)
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    apple = InlineKeyboardButton(text='Яблоко', callback_data='apple')
    pineapple = InlineKeyboardButton(text='Ананас', callback_data='pineapple')
    builder.add(apple, pineapple)
    await callback.message.answer("Средняя покупка", reply_markup=builder.as_markup())
    await state.set_state(GoShopping.mid_purchase)


async def apple(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы выбрали яблоко')
    await state.update_data(mid_purchase='яблоко')
    await mid_low(callback, state)


async def pineapple(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы выбрали ананас')
    await state.update_data(mid_purchase='ананас')
    await mid_low(callback, state)


async def mid_low(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    builder = InlineKeyboardBuilder()
    twix = InlineKeyboardButton(text='Твикс', callback_data='twix')
    snickers = InlineKeyboardButton(text='Сникерс', callback_data='snickers')
    builder.add(twix, snickers)
    await callback.message.answer("Малая покупка", reply_markup=builder.as_markup())
    await state.set_state(GoShopping.small_purchase)


async def twix(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы выбрали твикс')
    await state.update_data(small_purchase='твикс')
    await low(callback, state)


async def snickers(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Вы выбрали сникерс')
    await state.update_data(small_purchase='сникерс')
    await low(callback, state)


async def low(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    raw_data = await state.get_data()
    big = raw_data['big_purchase']
    mid = raw_data['mid_purchase']
    small = raw_data['small_purchase']
    await callback.message.answer(str(big) + str(mid) + str(small))
    await state.clear()


def register_fsm_test(dp: Dispatcher):
    dp.message.register(go_shopping, StateFilter(None), Command(commands='go_shopping'))

    dp.callback_query.register(big_buttons, StateFilter(GoShopping.big_purchase), F.data.contains('big'))

    dp.callback_query.register(apple, StateFilter(GoShopping.mid_purchase), F.data == 'apple')
    dp.callback_query.register(pineapple, StateFilter(GoShopping.mid_purchase), F.data == 'pineapple')

    dp.callback_query.register(twix, StateFilter(GoShopping.small_purchase), F.data == 'twix')
    dp.callback_query.register(snickers, StateFilter(GoShopping.small_purchase), F.data == 'snickers')
