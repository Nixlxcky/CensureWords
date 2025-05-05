from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from create_bot import bot, db_admins
from keyboards import admin_kb
from handlers.words_filter import distance
from texts import admin_texts


class AdminStatesGroup(StatesGroup):
    word_ban = State()
    word_unban = State()
    add_group = State()


async def view(message: types.Message):
    if message.from_user.id in await db_admins.read_admins(write_ids=True) and await db_admins.get_sub_status(
            await db_admins.read_buyer(admin_id=message.chat.id)):


        buyer_ids = await db_admins.read_buyer(admin_id=message.from_user.id)

        for buyer_id in buyer_ids:
            text = ''
            for number, censored_word in enumerate([word[0] for word in await db_admins.read_words(buyer_id)]):
                text += f'{number + 1}) {censored_word}\n'

            with open(f'to_read/censored_{buyer_id}_words.txt', 'w') as file:
                file.write(text)

            await bot.send_document(message.from_user.id, open(f'to_read/censored_{buyer_id}_words.txt'), 'rb')


async def ban_word_command(message: types.Message):
    if message.from_user.id in await db_admins.read_admins(write_ids=True) and await db_admins.get_sub_status(
            await db_admins.read_buyer(admin_id=message.from_user.id)):
        admin_language = await db_admins.get_language(await db_admins.read_buyer(admin_id=message.from_user.id))
        await message.delete()
        await bot.send_message(
            chat_id=message.chat.id,
            text=admin_texts.AdminTexts.get_admin(admin_language).ban_command,
            reply_markup=admin_kb.AdminKeyboards.get_admin_keyboard(admin_language).cancel_command_admin,
        )
        await AdminStatesGroup.word_ban.set()


async def ban_word(message: types.Message, state: FSMContext):

    buyer_ids = await db_admins.read_buyer(admin_id=message.from_user.id)
    admin_language = await db_admins.get_language(buyer_ids)
    answer = ''
    for buyer_id in buyer_ids:
        buyer_name = await db_admins.get_buyer_name(buyer_id)
        for word in [word1.lower().strip() for word1 in message.text.split(' ')]:
            if word in [word2[0] for word2 in await db_admins.read_words(buyer_id)]:
                answer += admin_texts.AdminTexts.get_admin(admin_language).ban_word_failure.format(word, buyer_name)
            else:


                await db_admins.add_word(word, buyer_id)
                answer += admin_texts.AdminTexts.get_admin(admin_language).ban_word_success.format(word, buyer_name)

    await message.delete()
    await bot.send_message(chat_id=message.chat.id, text=answer)
    await state.finish()


async def unban_word_command(message: types.Message):
    if message.from_user.id in await db_admins.read_admins(write_ids=True) and await db_admins.get_sub_status(
            await db_admins.read_buyer(admin_id=message.from_user.id)):
        admin_language = await db_admins.get_language(await db_admins.read_buyer(admin_id=message.from_user.id))
        await message.delete()
        await bot.send_message(
            chat_id=message.chat.id,
            text=admin_texts.AdminTexts.get_admin(admin_language).unban_command,
            reply_markup=admin_kb.AdminKeyboards.get_admin_keyboard(admin_language).cancel_command_admin,
        )
        await AdminStatesGroup.word_unban.set()


async def unban_word(message: types.Message, state: FSMContext):

    buyer_ids = await db_admins.read_buyer(admin_id=message.from_user.id)
    admin_language = await db_admins.get_language(buyer_ids)
    answer = ''
    for buyer_id in buyer_ids:
        buyer_name = await db_admins.get_buyer_name(buyer_id)
        for word in [word1.lower().strip() for word1 in message.text.split(' ')]:
            if word not in [word2[0] for word2 in await db_admins.read_words(buyer_id)]:
                possible_words = ''

                for censored_word in [word2[0] for word2 in await db_admins.read_words(buyer_id)]:
                    if distance(word, censored_word) <= len(censored_word) * 0.25:
                        possible_words += f"'{censored_word}', "

                if len(possible_words) >= 1:
                    answer += admin_texts.AdminTexts.get_admin(admin_language).unban_word_possible.format(word,
                                                                                                          possible_words,
                                                                                                          buyer_name,
                                                                                                          '*' * 30)
                else:
                    answer += admin_texts.AdminTexts.get_admin(admin_language).unban_word_failure.format(word,
                                                                                                         buyer_name,
                                                                                                         '*' * 30)

            else:
                await db_admins.delete_word(word, buyer_id)
                answer += admin_texts.AdminTexts.get_admin(admin_language).unban_word_success.format(word,
                                                                                                     buyer_name,
                                                                                                     '*' * 30)
    await message.delete()
    await bot.send_message(chat_id=message.chat.id, text=(answer[::-1].replace(',', '', 1))[::-1])
    await state.finish()


async def cancel_command_admin(callback_data: types.CallbackQuery, state: FSMContext):

    admin_language = await db_admins.get_language(await db_admins.read_buyer(admin_id=callback_data.from_user.id))
    current_state = await state.get_state()

    if current_state is None:
        return None

    await state.finish()
    await callback_data.answer()
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        text=admin_texts.AdminTexts.get_admin(admin_language).cancel_command,
        message_id=callback_data.message.message_id
    )


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(view, commands=['Просмотреть', 'View'])
    dp.register_message_handler(ban_word_command, commands=['Запретить', 'Ban'], state=None)
    dp.register_message_handler(ban_word, content_types=['text'], state=AdminStatesGroup.word_ban)
    dp.register_message_handler(unban_word_command, commands=['Удалить', 'Unban'], state=None)
    dp.register_message_handler(unban_word, content_types=['text'], state=AdminStatesGroup.word_unban)
    dp.register_callback_query_handler(cancel_command_admin, lambda call: call.data == 'cancel', state='*')
