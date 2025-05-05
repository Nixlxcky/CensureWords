from aiogram import types, Dispatcher

from create_bot import bot, db_admins, db_clients
from texts import admin_texts, client_texts, buyer_texts
from keyboards import admin_kb, client_kb, buyer_kb


async def start_command(message: types.Message):

    if message.from_user.id in await db_admins.read_admins(write_ids=True) and message.from_user.id in await db_admins.read_buyer(write_buyer_ids=True):
        buyer_language = await db_admins.get_language([message.from_user.id])

        if not await db_admins.get_sub_status(await db_admins.read_buyer(admin_id=message.from_user.id)):
            await bot.send_message(
                message.from_user.id,
                buyer_texts.BuyerTexts.get_buyer(buyer_language).buy_subscription
            )
        else:

            multi_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            multi_keyboard.add(admin_kb.AdminKeyboards.get_admin_keyboard(buyer_language).button_view).row(
                admin_kb.AdminKeyboards.get_admin_keyboard(buyer_language).button_ban,
                admin_kb.AdminKeyboards.get_admin_keyboard(buyer_language).button_unban
            ).row(
                buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).add_group_button,
                buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).delete_group_button
            ).row(
                buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).renew_subscription
            )

            multi_text = admin_texts.AdminTexts.get_admin(
                buyer_language).help_text + '\n\n' + buyer_texts.BuyerTexts.get_buyer(buyer_language).help_text
            await bot.send_message(
                message.from_user.id,
                multi_text,
                reply_markup=multi_keyboard
            )
    elif message.from_user.id in await db_admins.read_buyer(write_buyer_ids=True):
        buyer_language = await db_admins.get_language([message.from_user.id])
        if not await db_admins.get_sub_status(await db_admins.read_buyer(admin_id=message.from_user.id)):
            await bot.send_message(
                message.from_user.id,
                buyer_texts.BuyerTexts.get_buyer(buyer_language).buy_subscription
            )
        else:

            await bot.send_message(
                message.from_user.id,
                buyer_texts.BuyerTexts.get_buyer(buyer_language).help_text,
                reply_markup=buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).buyer_kb
            )

    elif message.from_user.id in await db_admins.read_admins(write_ids=True):
        admin_language = await db_admins.get_language(await db_admins.read_buyer(admin_id=message.from_user.id))
        if not await db_admins.get_sub_status(await db_admins.read_buyer(admin_id=message.from_user.id)):
            await bot.send_message(
                message.from_user.id,
                admin_texts.AdminTexts.get_admin(admin_language).ask_subscription
            )
        else:
            admin_language = await db_admins.get_language(await db_admins.read_buyer(admin_id=message.from_user.id))
            await bot.send_message(
                message.from_user.id,
                admin_texts.AdminTexts.get_admin(admin_language).help_text,
                reply_markup=admin_kb.AdminKeyboards.get_admin_keyboard(admin_language).main_keyboard_admin
            )

    elif message.from_user.id in await db_clients.read_client(write_ids=True):
        client_language = await db_clients.read_client(client_id=message.from_user.id)
        await bot.send_message(
            message.from_user.id,
            client_texts.ClientTexts.get_client(client_language).welcome_message,
            reply_markup=client_kb.ClientKeyboards.get_client_keyboard(client_language).welcome_keyboard
        )

    else:
        await bot.send_message(
            message.from_user.id,
            client_texts.ClientTexts.welcome_message.format(message.from_user.first_name, message.from_user.first_name),
            reply_markup=client_kb.ClientKeyboards.languages_choice
        )


async def add_possible_group(message: types.Message):
    possible_group_id = message.chat.id
    possible_group_tittle = message.chat.title


    if possible_group_id in await db_admins.read_possible_groups(write_ids=True) and possible_group_tittle not in await db_admins.read_possible_groups(write_tittles=True):
        await db_admins.update_possible_group_tittle(group_id=possible_group_id, new_tittle=possible_group_tittle)
    elif possible_group_id not in await db_admins.read_possible_groups(write_ids=True) and possible_group_tittle not in await db_admins.read_possible_groups(write_tittles=True):
        await db_admins.add_possible_group(
            group_id=possible_group_id,
            group_tittle=possible_group_tittle
        )




def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start', 'help'])
    dp.register_message_handler(add_possible_group, content_types=[types.ContentType.NEW_CHAT_MEMBERS])
