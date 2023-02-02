from aiogram import types
import asyncio
from random import randint
from loader import dp, bot,game
from config import DESCRIPTION_TEXT, description_text, welcome_text, command_list

# Команда старт
@dp.message_handler(commands=['start'])
async def start_command(message: types.message):
    await message.answer(text=welcome_text + f'Неужели это гроза тысячи морей, <em>{message.from_user.first_name}</em> '
                                             f'собственной персоной! ',
                         parse_mode='html')
    await bot.send_sticker(message.from_user.id,
                           sticker='CAACAgIAAxkBAAEHitRj2moxE3Secd17J4zsW-CP2LAxJgACMwADDbbSGUVhcOyd4UGCLgQ')
    await message.delete()


# Команда хэлп
@dp.message_handler(commands=['help'])
async def help_command(message: types.message):
    await message.reply(text=command_list, parse_mode='html')


# автоудаление сообщения, отправленного ботом пользователю, по таймеру
@dp.message_handler(commands=['description'])
async def description_command(message: types.message):
    mes_to_del = await message.answer(text=DESCRIPTION_TEXT, parse_mode='html')
    await asyncio.sleep(7)
    await mes_to_del.delete()
    await message.answer(text=description_text, parse_mode='html')


# Команда кик
@dp.message_handler(commands=['kick'])
async def sticker_command(message: types.message):
    await message.reply(text='Введите количество бутылок, которые принес юнга')


@dp.message_handler()
async def digit_input(message: types.message):
    if message.text.isdigit():
        # первоначальное объявление количество конфет и выбор первого игрока
        if game.total == -1:
            game.total = int(message.text)
            await bot.send_message(chat_id=message.chat.id, text=f'На столе {game.total} бутылок', parse_mode='html')
            game.player1 = message.from_user.first_name
            game.player2 = 'Билли'
            game.flag = await first_turn_player(game.player1, game.player2, message)
            # Если ход игрока - первый
            if game.flag:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"{game.player1}, выкладывай сколько бутылок готов разбить? от 1 до {game.max_value} ")
            else:
                await bot.send_message(chat_id=message.chat.id,
                                       text=f"Ткни {game.player2} разок вилкой,чтобы он проснулся. (ввести число)")
        # ловим ходы
        else:
            if game.total > game.max_value:
                if game.flag:
                    count = int(message.text)
                    game.counter1 += count
                    game.total -= count
                    game.flag = False
                    await game_stat_print(game.player1, count, game.counter1, game.total,message)
                    await bot.send_message(chat_id=message.chat.id,
                                           text=f"Ткни {game.player2} разок вилкой,чтобы он проснулся. (ввести число)")
                else:
                    count = await bot_turn(game.total, game.max_value)
                    game.counter2 += count
                    game.total -= count
                    game.flag = True
                    await game_stat_print(game.player2, count, game.counter2, game.total,message)
                    await bot.send_message(chat_id=message.chat.id,
                                     text=f"{game.player1}, выкладывай сколько бутылок готов разбить? от 1 до {game.max_value} ")
            else:
                # проверка, пора ли закончить игру
                if game.flag :
                    await bot.send_message(chat_id=message.chat.id,
                                           text=f"Поздравляю, {game.player1} - сегодня фортуна улыбнулась тебе! ")
                    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEHj9hj29KwVhBxAs4uX-OLulJh9kaX0QACNAADDbbSGXym6GAzec6iLgQ')
                else:
                    await bot.send_message(chat_id=message.chat.id,
                                       text=f"Ну, {game.player1}, сегодня ты пойдешь на корм рыбам!")
                    await bot.send_sticker(chat_id=message.chat.id, sticker='CAACAgIAAxkBAAEHj9Zj29Kv9WtOwXkWeCCyh-A7WEoE2gACLQADDbbSGVMtxqHEkftyLgQ')



async def first_turn_player(player1, player2, message: types.message):
    flag = randint(0, 2)  # флаг очередности
    if flag:
        await bot.send_message(chat_id=message.chat.id, text=f'Первым ходит {player1}')
    else:
        await bot.send_message(chat_id=message.chat.id, text=f'Первым ходит {player2}')
    return flag


async def game_stat_print(name, k, counter, value, message: types.message):
    await bot.send_message(chat_id=message.chat.id,
                           text=f"Ходил {name}, он разбил {k}, теперь у него {counter}. Осталось на столе {value} целых бутылок.")


async def bot_turn(value, max_value):
    count = randint(1, max_value + 1)
    while value - count <= max_value and value > max_value + 1:
        count = randint(1, max_value + 1)
    return count
