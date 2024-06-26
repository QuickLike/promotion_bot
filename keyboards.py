from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard():
    check = InlineKeyboardButton(text='✅Проверить подписку', callback_data='check')
    buy = InlineKeyboardButton(text='Купить все способы за 399р', callback_data='buy')
    follow = InlineKeyboardButton(text='Подписаться', callback_data='follow', url='https://t.me/+c7FLoAZM1To0YTYy')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [check], [buy], [follow]]
    )
    return markup


def sposob_markup():
    buy = InlineKeyboardButton(text='Купить все способы за 399р', callback_data='buy')
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [buy]
        ]
    )
    return markup
