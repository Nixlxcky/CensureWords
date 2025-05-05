from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


class AdminKeyboards(ABC):

    @staticmethod
    def get_admin_keyboard(language: str):
        if language.strip() == 'rus':
            return AdminKeyboardsRus
        elif language.strip() == 'en':
            return AdminKeyboardsEn

        return 'Check the languages!!!'

    main_keyboard_admin: ReplyKeyboardMarkup = None

    button_ban: KeyboardButton = None
    button_unban: KeyboardButton = None
    button_view: KeyboardButton = None

    cancel_command_admin: InlineKeyboardMarkup = None


class AdminKeyboardsRus(AdminKeyboards):
    main_keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

    button_ban = KeyboardButton(text='/Запретить')
    button_unban = KeyboardButton(text='/Удалить')
    button_view = KeyboardButton(text='/Просмотреть')

    main_keyboard_admin.add(button_view).row(button_unban, button_ban)

    cancel_command_admin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('\U0001F6AB Отменить \U0001F6AB', callback_data='cancel'))


class AdminKeyboardsEn(AdminKeyboards):
    main_keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)

    button_ban = KeyboardButton(text='/Ban')
    button_unban = KeyboardButton(text='/Unban')
    button_view = KeyboardButton(text='/View')

    main_keyboard_admin.add(button_view).row(button_unban, button_ban)

    cancel_command_admin = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton('\U0001F6AB Cancel \U0001F6AB', callback_data='cancel'))


if __name__ == '__main__':
    print(AdminKeyboardsRus.main_keyboard_admin)
