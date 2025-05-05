from abc import ABC

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AdminRegistrationKeyboards(ABC):

    @staticmethod
    def get_registration_class(language: str):
        if language.strip() == 'rus':
            return AdminRegistrationKeyboardsRus
        elif language.strip() == 'en':
            return AdminRegistrationKeyboardsEn

        return 'Check the languages!!!'

    languages_choose_keyboard = InlineKeyboardMarkup(row_width=2)
    russian_button = InlineKeyboardButton('Rus', callback_data='choose-rus')
    english_button = InlineKeyboardButton('En', callback_data='choose-en')
    languages_choose_keyboard.add(russian_button).add(english_button)

    done_button_keyboard: InlineKeyboardMarkup = None
    done_button_first: InlineKeyboardButton = None


class AdminRegistrationKeyboardsRus(AdminRegistrationKeyboards):
    done_button_keyboard = InlineKeyboardMarkup()
    done_button_first = InlineKeyboardButton(text='Готово', callback_data='done-first')
    done_button_keyboard.add(done_button_first)


class AdminRegistrationKeyboardsEn(AdminRegistrationKeyboards):
    done_button_keyboard = InlineKeyboardMarkup()
    done_button_first = InlineKeyboardButton(text='Done', callback_data='done-first')
    done_button_keyboard.add(done_button_first)


if __name__ == '__main__':
    print(AdminRegistrationKeyboardsRus.done_button_keyboard)
