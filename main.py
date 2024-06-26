import asyncio
from datetime import datetime
import logging
import os
import sys

import pytz
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import ContentType
from aiogram.filters.command import Command
from environs import Env

import baza
from constraints import SEND_MESSAGE_TIME
import keyboards
import textes


env = Env()
env.read_env()

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_CHECK = os.getenv('CHAT_CHECK')
YOOTOKEN = os.getenv('YOOTOKEN')


bot = Bot(BOT_TOKEN)
dp = Dispatcher()
router = Router()


async def mailing():
    logging.info(f'mailing')
    while True:
        time = datetime.now(pytz.timezone('Europe/Moscow'))
        if time.hour == SEND_MESSAGE_TIME and time.minute == 0:
            users = await baza.get_ids()
            lines = await baza.get_lines()
            logging.debug(users)
            for i in users:
                try:
                    number = await baza.get_sposob(i)
                    logging.debug(number)
                    s = lines[number].partition('.')[0] + '/30' + lines[number].partition('.')[2]
                    await bot.send_message(chat_id=i, text=s, reply_markup=keyboards.sposob_markup())
                    await bot.send_message(chat_id=i,
                                           text=f'Следующий способ я отправлю завтра в {SEND_MESSAGE_TIME}:00 по МСК')
                    await baza.update_sposob(i, number + 1)
                except Exception as e:
                    logging.error(e)
            logging.info('Способы разосланы')
            await asyncio.sleep(70)
        await asyncio.sleep(5)


@dp.message(Command('start'))
async def start(message: types.Message):
    logging.info(f'Команда /start получена от пользователя {message.from_user.id}')
    await bot.send_message(chat_id=message.from_user.id,
                           text=textes.start_text(message.from_user.first_name),
                           reply_markup=keyboards.start_keyboard(),
                           disable_web_page_preview=True)
    status = await baza.check_user(message.from_user.id)
    if not status:
        await baza.add_user(message.from_user.id)
        logging.info(f'Пользователь {message.from_user.id} не найден в базе данных, добавляю.')
    else:
        logging.info(f'Пользователь {message.from_user.id} уже существует в базе данных.')


@dp.callback_query(F.data.in_(['check', 'buy']))
async def check_callback(callback: types.CallbackQuery):
    if callback.data == 'check':
        user_channel_status = await bot.get_chat_member(chat_id=CHAT_CHECK, user_id=callback.from_user.id)
        if user_channel_status.status != 'left':
            await callback.message.delete()
            f = open('start_inform.txt', encoding='utf-8')
            s = f.read()
            await bot.send_message(chat_id=callback.from_user.id, text=s)
            lines = await baza.get_lines()
            s = lines[0].partition('.')[0] + '/30' + lines[0].partition('.')[2]
            await bot.send_message(chat_id=callback.from_user.id, text=s, reply_markup=keyboards.sposob_markup())
            await baza.update_sposob(callback.from_user.id, 1)

            await bot.send_message(chat_id=callback.from_user.id,
                                   text=f'Следующий способ я отправлю завтра в {SEND_MESSAGE_TIME}:00 по МСК')
            await baza.update_status(callback.from_user.id)
        else:
            await bot.send_message(chat_id=callback.from_user.id, text='Вы не подписались, попробуйте еще раз')
    if callback.data == 'buy':
        await bot.send_invoice(chat_id=callback.from_user.id,
                               title='Оформление рассылки',
                               description='Покупка способов',
                               payload='sub',
                               provider_token=YOOTOKEN,
                               currency='RUB',
                               start_parameter='test_bot',
                               prices=[{'label': 'rub', 'amount': 39900}])


@router.pre_checkout_query()
async def checkout(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


# @dp.message(content_types=ContentType.SUCCESSFUL_PAYMENT)
@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types.Message):
    if message.successful_payment.invoice_payload == 'sub':
        f = open('start_inform.txt', encoding='utf-8')
        s = f.read()
        await bot.send_message(chat_id=message.from_user.id, text=s)
        lines = await baza.get_lines()
        for line in lines:
            await bot.send_message(chat_id=message.from_user.id,
                                   text=line)
            await baza.update_sposob(message.from_user.id, 0)


async def main():
    await baza.Create_baza()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,  # В случае отладки кода: level=logging.DEBUG
        format=('%(asctime)s, '
                '%(levelname)s, '
                '%(funcName)s, '
                '%(lineno)d, '
                '%(message)s'
                ),
        encoding='UTF-8',
        handlers=[logging.FileHandler('main.log'),
                  logging.StreamHandler(sys.stdout)]
    )
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(mailing())
    loop.run_forever()
