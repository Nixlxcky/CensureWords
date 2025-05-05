import time

import aiogram.utils.exceptions
from aiogram import types, Dispatcher

from create_bot import bot, db_clients, db_admins
from texts import client_texts
from keyboards import client_kb, admin_registartion_kb


async def get_creator_username():
    return '@Nixlxcky' # bot creator username


async def edit_message(callback_data: types.CallbackQuery, text: str, reply_markup: types.InlineKeyboardMarkup = None):
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=text,
        reply_markup=reply_markup
    )


async def languages_choose(callback_data: types.CallbackQuery):
    client_language = callback_data.data.split('-')[1]

    if callback_data.from_user.id not in await db_clients.read_client(write_ids=True):
        await db_clients.add_client(
            callback_data.from_user.id,
            callback_data.from_user.first_name,
            client_language
        )

    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=client_texts.ClientTexts.get_client(client_language).language_response
    )
    await bot.answer_callback_query(callback_data.id)
    await callback_data.message.answer(
        client_texts.ClientTexts.get_client(client_language).welcome_message_firstly.format(
            callback_data.from_user.first_name),
        reply_markup=client_kb.ClientKeyboards.get_client_keyboard(client_language).welcome_keyboard
    )
    await callback_data.answer()


async def welcome_keyboard(callback_data: types.CallbackQuery):
    if callback_data.from_user.id in await db_clients.read_client(write_ids=True):
        creaot_username = await get_creator_username()
        client_language = await db_clients.read_client(client_id=callback_data.from_user.id)
        suffix = callback_data.data.split('-')[1]

        if suffix == 'how':
            await callback_data.answer()
            video_back = client_kb.ClientKeyboards.get_back_button(client_language, 'welcome_video')
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).please_wait)
            await bot.send_video(
                chat_id=callback_data.message.chat.id,
                video=open(f'videos/BotPrieview{client_language}.mp4', 'rb'),
                caption=client_texts.ClientTexts.get_client(client_language).description.format(creaot_username),
                reply_markup=types.InlineKeyboardMarkup().add(video_back)
            )
            await bot.delete_message(
                chat_id=callback_data.message.chat.id,
                message_id=callback_data.message.message_id
            )

        elif suffix == 'creator':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).creator_welcome,
                               reply_markup=client_kb.ClientKeyboards.get_client_keyboard(
                                   client_language).creator_keyboard)
            await callback_data.answer()
        elif suffix == 'buy':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).payment,
                               reply_markup=client_kb.ClientKeyboards.get_client_keyboard(client_language).pay_keyboard)
            await callback_data.answer()


async def creator_keyboard(callback_data: types.CallbackQuery):
    if callback_data.from_user.id in await db_clients.read_client(write_ids=True):
        The_God_username = await get_creator_username()
        client_language = await db_clients.read_client(client_id=callback_data.from_user.id)
        suffix = callback_data.data.split('-')[1]
        back = types.InlineKeyboardMarkup().add(client_kb.ClientKeyboards.get_back_button(client_language, 'creator'))

        if suffix == 'name':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).creator_name.format(
                                   The_God_username), reply_markup=back)
        elif suffix == 'technology':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).creator_technology,
                               reply_markup=back)
        elif suffix == 'date':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).creator_realise,
                               reply_markup=back)
        await callback_data.answer()


async def payment_handler(callback_data: types.CallbackQuery):
    if callback_data.from_user.id in await db_clients.read_client(write_ids=True):
        client_language = await db_clients.read_client(client_id=callback_data.from_user.id)
        suffix = callback_data.data.split('-')[1]
        if suffix == 'pay':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).pay_success,
                               reply_markup=client_kb.ClientKeyboards.get_client_keyboard(
                                   client_language).continue_keyboard)


async def done_handler(callback_data: types.CallbackQuery):
    client_language = await db_clients.read_client(client_id=callback_data.from_user.id)
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=client_texts.ClientTexts.get_client(client_language).languages_choose,
        reply_markup=admin_registartion_kb.AdminRegistrationKeyboards.get_registration_class(
            client_language).languages_choose_keyboard
    )
    await callback_data.answer()


async def languages_handler(callback_data: types.CallbackQuery):
    language_suffix = callback_data.data.split('-')[1]
    await callback_data.answer()

    buyer_name = callback_data.from_user.first_name
    sub_time = int(time.time()) + await db_admins.convert_days(14)

    await db_admins.add_buyer(
        name=buyer_name,
        language=language_suffix,
        sub_time=sub_time,
        buyer_id=callback_data.from_user.id
    )

    await db_clients.delete_client(callback_data.from_user.id)

    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=client_texts.ClientTexts.get_client(language_suffix).registration_success
    )


async def back_command_client(callback_data: types.CallbackQuery):
    if callback_data.from_user.id in await db_clients.read_client(write_ids=True):
        client_language = await db_clients.read_client(client_id=callback_data.from_user.id)
        suffix = callback_data.data.split('-')[1]
        if suffix == 'welcome':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).welcome_message,
                               reply_markup=client_kb.ClientKeyboards.get_client_keyboard(
                                   client_language).welcome_keyboard)
        elif suffix == 'welcome_video':
            try:
                await bot.delete_message(
                    chat_id=callback_data.message.chat.id,
                    message_id=callback_data.message.message_id
                )
            except aiogram.utils.exceptions.MessageCantBeDeleted:
                pass
            await bot.send_message(
                chat_id=callback_data.message.chat.id,
                text=client_texts.ClientTexts.get_client(client_language).welcome_message,
                reply_markup=client_kb.ClientKeyboards.get_client_keyboard(client_language).welcome_keyboard
            )
        elif suffix == 'creator':
            await edit_message(callback_data=callback_data,
                               text=client_texts.ClientTexts.get_client(client_language).creator_welcome,
                               reply_markup=client_kb.ClientKeyboards.get_client_keyboard(
                                   client_language).creator_keyboard)

        await callback_data.answer()


def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(languages_choose, lambda call: call.data.split('-')[0] == 'language')
    dp.register_callback_query_handler(welcome_keyboard, lambda call: call.data.split('-')[0] == 'welcome')
    dp.register_callback_query_handler(creator_keyboard, lambda call: call.data.split('-')[0] == 'creator')
    dp.register_callback_query_handler(payment_handler, lambda call: call.data.split('-')[0] == 'pay')
    dp.register_callback_query_handler(done_handler, lambda call: call.data == 'continue')
    dp.register_callback_query_handler(languages_handler, lambda call: call.data.split('-')[0] == 'choose')

    dp.register_callback_query_handler(back_command_client, lambda call: call.data.split('-')[0] == 'back')
