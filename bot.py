import json
import os
from dotenv import load_dotenv
import aiohttp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Easy crypto bot

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(bot)

# session aiohttp otherwise get-request

button_btc_usdt, button_eth_usdt,\
button_eth_rus, button_btc_rus = KeyboardButton('₿ btc_usdt'),\
                                   KeyboardButton('💵 eth_usdt'),\
                                   KeyboardButton('💤 eth_rub'),\
                                   KeyboardButton('🕺 btc_rub')
crypto_keyboard = ReplyKeyboardMarkup()
crypto_keyboard.add(button_btc_usdt,
                    button_eth_usdt,
                    button_eth_rus,
                    button_btc_rus)

async def get_price(symbol1: str='BTC', symbol2: str='USDT'):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={symbol1}{symbol2}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print(resp.status)
            data = await response.text()

    return json.loads(data)

# dict unpacking function
def prepare_answer(data: dict):
    return '\n'.join(f'{key} : {value}' for key, value in data.items())

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Hello\nWelcome to cryptocurrency price bot",
                        reply_markup=crypto_keyboard)

@dp.message_handler()
async def response_message(msg: types.Message):
    try:
        currency1, currency2 = msg.text.upper()[2:].split('_')
        data = await get_price(currency1, currency2)
        await bot.send_message(msg.from_user.id, prepare_answer(data))
    except:
        await bot.send_message(msg.from_user.id, "you should split currency by _")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)