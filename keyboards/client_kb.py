from abc import ABC

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ClientKeyboards(ABC):

    @staticmethod
    def get_client_keyboard(language: str):
        if language.strip() == 'rus':
            return ClientKeyboardsRus
        elif language.strip() == 'en':
            return ClientKeyboardsEn

        return 'Check the languages!!!'

    @staticmethod
    def get_back_button(language: str, callback_data: str):
        text = None
        if language == 'rus':
            text = '<-- Назад'
        elif language == 'en':
            text = '<-- Back'

        back_button = InlineKeyboardButton(text=text, callback_data=f'back-{callback_data}')
        return back_button

    languages_choice = InlineKeyboardMarkup(row_width=2)
    rus_button = InlineKeyboardButton(text='Rus', callback_data='language-rus')
    en_button = InlineKeyboardButton(text='En', callback_data='language-en')
    languages_choice.add(rus_button).add(en_button)

    welcome_keyboard: InlineKeyboardMarkup = None
    why_this_button: InlineKeyboardButton = None
    how_work_button: InlineKeyboardButton = None
    creator_button: InlineKeyboardButton = None
    buy_button: InlineKeyboardButton = None

    creator_keyboard: InlineKeyboardMarkup = None
    creator_name_button: InlineKeyboardButton = None
    technology_button: InlineKeyboardButton = None
    realise_date_button: InlineKeyboardButton = None

    buy_keyboard: InlineKeyboardMarkup = None
    webmoney_button: InlineKeyboardButton = None
    card_button: InlineKeyboardButton = None

    webmoney_keyboard: InlineKeyboardMarkup = None
    send_link_button: InlineKeyboardButton = None

    card_keyboard: InlineKeyboardMarkup = None
    send_account_button: InlineKeyboardButton = None

    pay_keyboard: InlineKeyboardMarkup = None
    pay_button: InlineKeyboardButton = None

    continue_keyboard: InlineKeyboardMarkup = None
    continue_button: InlineKeyboardButton = None


class ClientKeyboardsRus(ClientKeyboards):
    welcome_keyboard = InlineKeyboardMarkup(row_width=1)
    how_work_button = InlineKeyboardButton(text='Как работает бот?', callback_data='welcome-how')
    creator_button = InlineKeyboardButton(text='Информация о разработке', callback_data='welcome-creator')
    buy_button = InlineKeyboardButton(text='Покупка бота, '
                                           '2 недели бесплатно!', callback_data='welcome-buy')
    welcome_keyboard.add(how_work_button).add(creator_button).add(buy_button)

    creator_keyboard = InlineKeyboardMarkup(row_width=1)
    creator_name_button = InlineKeyboardButton(text='Создатель', callback_data='creator-name')
    technology_button = InlineKeyboardButton(text='С помощью чего сделан бот?', callback_data='creator-technology')
    realise_date_button = InlineKeyboardButton(text='Дата выпуска', callback_data='creator-date')
    creator_back = ClientKeyboards.get_back_button('rus', 'welcome')
    creator_keyboard.add(creator_name_button).add(technology_button).add(realise_date_button).add(creator_back)



    pay_keyboard = InlineKeyboardMarkup(row_width=1)
    pay_button = InlineKeyboardButton(text='Получить две недели бесплатно!', callback_data='pay-pay')
    pay_back = ClientKeyboards.get_back_button('rus', 'welcome')
    pay_keyboard.add(pay_button).add(pay_back)

    continue_keyboard = InlineKeyboardMarkup(row_width=1)
    continue_button = InlineKeyboardButton(text='Продолжить', callback_data='continue')
    continue_keyboard.add(continue_button)


class ClientKeyboardsEn(ClientKeyboards):
    welcome_keyboard = InlineKeyboardMarkup(row_width=1)
    how_work_button = InlineKeyboardButton(text='How does this bot work?', callback_data='welcome-how')
    creator_button = InlineKeyboardButton(text='Development information', callback_data='welcome-creator')
    buy_button = InlineKeyboardButton(text='Bot buying, '
                                           '2 weeks is for free!', callback_data='welcome-buy')
    welcome_keyboard.add(how_work_button).add(creator_button).add(buy_button)

    creator_keyboard = InlineKeyboardMarkup(row_width=1)
    creator_name_button = InlineKeyboardButton(text='Creator', callback_data='creator-name')
    technology_button = InlineKeyboardButton(text='How is this bot created?', callback_data='creator-technology')
    realise_date_button = InlineKeyboardButton(text='Release', callback_data='creator-date')
    creator_back = ClientKeyboards.get_back_button('en', 'welcome')
    creator_keyboard.add(creator_name_button).add(technology_button).add(realise_date_button).add(creator_back)


    pay_keyboard = InlineKeyboardMarkup(row_width=2)
    pay_button = InlineKeyboardButton(text='Get two weeks for free!', callback_data='pay-pay')
    pay_back = ClientKeyboards.get_back_button('en', 'welcome')
    pay_keyboard.add(pay_button).add(pay_back)

    continue_keyboard = InlineKeyboardMarkup(row_width=1)
    continue_button = InlineKeyboardButton(text='Continue', callback_data='continue')
    continue_keyboard.add(continue_button)


if __name__ == '__main__':
    print(ClientKeyboardsRus.back_button.callback_data)
