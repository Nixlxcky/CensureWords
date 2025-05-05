from datetime import datetime
from time import time

import aiogram.utils.exceptions
from aiogram.utils import exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.types.message import ContentType

from create_bot import bot, db_admins, PAYMENT_TOKEN
from keyboards import buyer_kb
from texts import buyer_texts, admin_texts
from help_functions import check_edit_groups


class BuyerStates(StatesGroup):
    add_group = State()


async def add_group_command(message: types.Message):
    if message.from_user.id in await db_admins.read_buyer(write_buyer_ids=True) and await db_admins.get_sub_status(
            [message.from_user.id]):
        await check_edit_groups()
        buyer_id = message.from_user.id
        buyer_language = await db_admins.get_language([buyer_id])
        if len(await db_admins.get_buyer_groups(message.from_user.id)) <= 5:
            await message.delete()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).done_button).add(
                buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).cancel_button)
            await bot.send_message(
                chat_id=message.chat.id,
                text=buyer_texts.BuyerTexts.get_buyer(buyer_language).add_group_command,
                reply_markup=keyboard
            )

        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=buyer_texts.BuyerTexts.get_buyer(buyer_language).limit_of_groups
            )


async def done_buyer(callback_data: types.CallbackQuery):
    buyer_id = callback_data.from_user.id
    buyer_language = await db_admins.get_language([buyer_id])
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).cancel_button)
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=buyer_texts.BuyerTexts.get_buyer(buyer_language).add_group_text,
        reply_markup=keyboard
    )
    await BuyerStates.add_group.set()
    await callback_data.answer()


async def add_group(message: types.Message, state: FSMContext):
    await check_edit_groups()
    group_tittle = message.text.strip()
    group_id = await db_admins.get_possible_group_id(group_tittle) or 0
    buyer_language = await db_admins.get_language(buyer_id=[message.from_user.id])


    if group_id in await db_admins.read_admins(write_group_ids=True):
        await message.delete()
        await bot.send_message(
            chat_id=message.chat.id,
            text=buyer_texts.BuyerTexts.get_buyer(buyer_language).group_already_exists
        )
        await BuyerStates.add_group.set()
    else:
        try:
            await bot.get_chat(group_id)

            group_admins = await bot.get_chat_administrators(group_id)
            group_creator = list(filter(lambda admin: admin['status'] == 'creator', group_admins))[0]['user']['id']

            await db_admins.add_admin(
                admin_id=group_creator,
                group_id=group_id,
                buyer_id=message.from_user.id
            )
            await db_admins.delete_possible_group(group_id)

            await state.finish()

            await message.delete()
            await bot.send_message(
                chat_id=message.chat.id,
                text=buyer_texts.BuyerTexts.get_buyer(buyer_language).add_group_success.format(
                    len(await db_admins.get_buyer_groups(message.from_user.id)))
            )

        except exceptions.ChatNotFound:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot.send_message(
                chat_id=message.chat.id,
                text=buyer_texts.BuyerTexts.get_buyer(buyer_language).add_group_fail
            )
            await BuyerStates.add_group.set()
        except aiogram.utils.exceptions.BotKicked:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
            await bot.send_message(
                chat_id=message.chat.id,
                text=buyer_texts.BuyerTexts.get_buyer(buyer_language).add_group_command.replace('.', '!')
            )


async def delete_group_command(message: types.Message):
    if message.from_user.id in await db_admins.read_buyer(write_buyer_ids=True) and await db_admins.get_sub_status(
            [message.from_user.id]):
        await check_edit_groups()
        buyer_id = message.from_user.id
        buyer_language = await db_admins.get_language([buyer_id])

        keyboad = types.InlineKeyboardMarkup()
        buyer_groups = await db_admins.get_buyer_groups(message.from_user.id) or []
        data_sample = 'group@{}'

        for group_id in buyer_groups:
            group_date = await bot.get_chat(group_id)
            button = types.InlineKeyboardButton(text=group_date['title'],
                                                callback_data=data_sample.format(group_id))
            keyboad.add(button)

        keyboad.add(buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).cancel_button)

        text = buyer_texts.BuyerTexts.get_buyer(buyer_language).delete_group_text

        await message.delete()
        await bot.send_message(
            chat_id=message.chat.id,
            text=text,
            reply_markup=keyboad
        )


async def delete_group(callback_data: types.CallbackQuery):
    buyer_id = callback_data.from_user.id
    buyer_language = await db_admins.get_language([buyer_id])

    group_id = int(callback_data.data.split('@')[1])
    group_name = await bot.get_chat(group_id)

    await db_admins.delete_group(group_id)
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=buyer_texts.BuyerTexts.get_buyer(buyer_language).delete_group_success.format(group_name['title'],
                                                                                          len(await db_admins.get_buyer_groups(
                                                                                              buyer_id)))
    )
    await callback_data.answer()


async def renew_subscription_command(message: types.Message):
    if message.from_user.id in await db_admins.read_buyer(write_buyer_ids=True):
        buyer_id = message.from_user.id
        buyer_language = await db_admins.get_language([buyer_id])

        old_subscription = await db_admins.get_sub_time(buyer_id)
        old_subscription_date = datetime.fromtimestamp(int(old_subscription)).strftime('%d.%m.%Y')

        if old_subscription < int(time()):
            old_subscription = int(time())

        new_subscription_date = datetime.fromtimestamp(
            await db_admins.convert_days(30) + int(old_subscription)).strftime('%d.%m.%Y')

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).continue_subscription).add(
            buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).cancel_button)
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text=buyer_texts.BuyerTexts.get_buyer(buyer_language).subscription_info.format(old_subscription_date,
                                                                                           new_subscription_date),
            reply_markup=keyboard
        )


async def select_currency(callback_data: types.CallbackQuery):
    buyer_id = callback_data.from_user.id
    buyer_language = await db_admins.get_language([buyer_id])

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        buyer_kb.BuyerKeyboards.EUR_currency
    ).add(
        buyer_kb.BuyerKeyboards.USD_currency
    ).add(
        buyer_kb.BuyerKeyboards.RUB_currency
    ).add(
        buyer_kb.BuyerKeyboards.get_buyer_kb(buyer_language).cancel_button
    )

    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=buyer_texts.BuyerTexts.get_buyer(buyer_language).select_currency,
        reply_markup=keyboard
    )


async def send_bill(callback_data: types.CallbackQuery):
    if PAYMENT_TOKEN.split(':')[1] == 'LIVE':
        buyer_id = callback_data.from_user.id
        buyer_language = await db_admins.get_language([buyer_id])

        old_subscription = await db_admins.get_sub_time(buyer_id)
        old_subscription_date = datetime.fromtimestamp(int(old_subscription)).strftime('%d.%m.%Y')

        if old_subscription < int(time()):
            old_subscription = time()

        new_subscription = await db_admins.convert_days(30) + old_subscription
        new_subscription_date = datetime.fromtimestamp(new_subscription).strftime('%d.%m.%Y')

        currency = callback_data.data.split('_')[0]

        prices = None
        if currency == 'eur':
            prices = [buyer_texts.BuyerTexts.get_buyer(buyer_language).PRICE_EUR]
        elif currency == 'usd':
            prices = [buyer_texts.BuyerTexts.get_buyer(buyer_language).PRICE_USD]
        elif currency == 'rub':
            prices = [buyer_texts.BuyerTexts.get_buyer(buyer_language).PRICE_RUB]

        await bot.delete_message(
            chat_id=callback_data.message.chat.id,
            message_id=callback_data.message.message_id
        )
        await bot.send_invoice(
            callback_data.message.chat.id,
            title=buyer_texts.BuyerTexts.get_buyer(buyer_language).renew_subscription,
            description=buyer_texts.BuyerTexts.get_buyer(buyer_language).renew_subscription_info.format(
                old_subscription_date, new_subscription_date),
            provider_token=PAYMENT_TOKEN,
            currency=callback_data.data.split('_')[0],
            is_flexible=False,
            prices=prices,
            start_parameter='censure-words-buy',
            payload='buy-accept',

        )


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    buyer_id = pre_checkout_query.from_user.id
    buyer_language = await db_admins.get_language([buyer_id])
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=buyer_texts.BuyerTexts.get_buyer(
        buyer_language).error_payment_message)


async def renew_subscription(message: types.Message):

    payment_information = message.successful_payment.to_python()
    await db_admins.add_payment_information(
        username=message.from_user.username,
        date=datetime.fromtimestamp(int(time())).strftime('%d.%m.%Y %H:%M:%S'),
        currency=payment_information['currency'],
        total_amount=int(payment_information['total_amount'] / 100),
        tg_pm_chg_id=payment_information['telegram_payment_charge_id'],
        prov_pm_chg_id=payment_information['provider_payment_charge_id']
    )

    buyer_id = message.from_user.id
    buyer_language = await db_admins.get_language([buyer_id])

    old_subscription = await db_admins.get_sub_time(buyer_id)

    if old_subscription < int(time()):
        old_subscription = int(time())

    new_subscription = old_subscription + await db_admins.convert_days(30)
    new_subscription_date = datetime.fromtimestamp(new_subscription).strftime('%d.%m.%Y')
    await db_admins.update_sub_time(buyer_id, new_subscription)

    await bot.send_message(
        message.chat.id,
        buyer_texts.BuyerTexts.get_buyer(buyer_language).successful_payment.format(new_subscription_date)
    )


async def cancel_command_buyer(callback_data: types.CallbackQuery, state: FSMContext):
    buyer_language = await db_admins.get_language([callback_data.from_user.id])

    await state.finish()
    await callback_data.answer()
    await bot.edit_message_text(
        chat_id=callback_data.message.chat.id,
        message_id=callback_data.message.message_id,
        text=admin_texts.AdminTexts.get_admin(buyer_language).cancel_command,
    )


def register_handlers_buyer(dp: Dispatcher):
    dp.register_message_handler(add_group_command, commands=['Добавить_группу', 'Add_group'])
    dp.register_callback_query_handler(done_buyer, lambda call: call.data == 'done-buyer')
    dp.register_message_handler(add_group, content_types=['text'], state=BuyerStates.add_group)

    dp.register_message_handler(delete_group_command, commands=['Удалить_группу', 'Delete_group'])
    dp.register_callback_query_handler(delete_group, lambda call: call.data.split('@')[0] == 'group')

    dp.register_message_handler(renew_subscription_command, commands=['Продлить_подписку', 'Renew_subscription'])
    dp.register_callback_query_handler(select_currency, lambda call: call.data == 'buy_subscription-buyer')
    dp.register_callback_query_handler(send_bill, lambda call: call.data.split('_')[1] == 'currency-buyer')
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, lambda query: True)
    dp.register_message_handler(renew_subscription, content_types=ContentType.SUCCESSFUL_PAYMENT)

    dp.register_callback_query_handler(cancel_command_buyer, lambda call: call.data.split('_')[1] == 'cancel-buyer',
                                       state='*')
