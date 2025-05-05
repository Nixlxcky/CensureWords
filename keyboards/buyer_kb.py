from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton


class BuyerKeyboards(ABC):
    @staticmethod
    def get_buyer_kb(language: str):
        if language.strip() == 'rus':
            return BuyerKeyboardsRus
        elif language.strip() == 'en':
            return BuyerKeyboardsEn

        return 'Check the languages!!!'

    buyer_kb: ReplyKeyboardMarkup = None
    add_group_button: KeyboardButton = None
    delete_group_button: KeyboardButton = None

    cancel_button: InlineKeyboardButton = None

    done_button: InlineKeyboardButton = None

    renew_subscription: InlineKeyboardButton = None

    continue_subscription: InlineKeyboardButton = None

    EUR_currency: InlineKeyboardButton = InlineKeyboardButton('EUR', callback_data='eur_currency-buyer')
    RUB_currency: InlineKeyboardButton = InlineKeyboardButton('RUB', callback_data='rub_currency-buyer')
    USD_currency: InlineKeyboardButton = InlineKeyboardButton('USD', callback_data='usd_currency-buyer')

class BuyerKeyboardsRus(BuyerKeyboards):
    buyer_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_group_button = KeyboardButton('/Добавить_группу')
    delete_group_button = KeyboardButton('/Удалить_группу')
    renew_subscription = KeyboardButton('/Продлить_подписку')

    buyer_kb.add(add_group_button, delete_group_button).row(renew_subscription)

    cancel_button = InlineKeyboardButton(text='\U0001F6AB Отменить \U0001F6AB', callback_data='cancel_cancel-buyer')

    done_button = InlineKeyboardButton('Готово', callback_data='done-buyer')

    continue_subscription = InlineKeyboardButton('Продолжить', callback_data='buy_subscription-buyer')


class BuyerKeyboardsEn(BuyerKeyboards):
    buyer_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_group_button = KeyboardButton('/Add_group')
    delete_group_button = KeyboardButton('/Delete_group')
    renew_subscription = KeyboardButton('/Renew_subscription'
                                        )
    buyer_kb.add(add_group_button, delete_group_button).row(renew_subscription)

    cancel_button = InlineKeyboardButton(text='\U0001F6AB Cancel \U0001F6AB', callback_data='cancel_cancel-buyer')

    done_button = InlineKeyboardButton('Done', callback_data='done-buyer')

    continue_subscription = InlineKeyboardButton('Continue', callback_data='buy_subscription-buyer')
