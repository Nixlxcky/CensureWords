from abc import ABC


class ClientTexts(ABC):

    @staticmethod
    def get_client(language: str):
        if language.strip() == 'rus':
            return ClientTextsRus
        elif language.strip() == 'en':
            return ClientTextsEn

        return 'Check the languages!!!'

    welcome_message = 'Привет, {}. Для продолжения работы, пожалуйста, выбери язык.\n\n' \
                      'Hello, {}. Please choose a language to continue.'
    welcome_message_firstly: str = None

    language_response: str = None

    description: str = None

    creator_welcome: str = None
    creator_name: str = None
    creator_technology: str = None
    creator_realise: str = None

    payment: str = None
    pay: str = None
    pay_success: str = None

    please_wait: str = None

    languages_choose: str = None

    registration_success: str = None
class ClientTextsRus(ClientTexts):
    welcome_message_firstly = 'Привет, {}! Ты запустил лучшего бота отвечающего за цензуру в чатах!\n' \
                              'Этот бот использует самые продвинутые и инновационные алгоритмы работы!\n' \
                              'Также бот предоставляет личную базу запрещенных слов, которую можно редактировать.'
    welcome_message = 'Добро пожаловать! Нажимай туда, куда хочешь!'

    language_response = 'Язык успешно выбран!'

    description = 'В видео показан пример работы бота.\n\n' \
                  'ЧТО НУЖНО ЗНАТЬ \U000026A0\n' \
                  '1) Если у вас анонимная группа, то бот не сможет распознать пользователя.\n' \
                  '2) Предустановленный файл запрещенных слов содержит только матерные слова.\n' \
                  '(Пока только на русском и английских языках)\n' \
                  '3) У каждого пользователя бота(админа бота) своя отдельная база слов.\n' \
                  '4) Все обновления базы данных происходят моментально.\n' \
                  '5) Если вы ошиблись с запретом или удалением слова.\n' \
                  '(К примеру, запретили уже запрещенное слово)\n' \
                  'То бот выведет соответствующее сообщение.\n' \
                  '6) Используя команды "/Запретить" и "/Удалить", \n' \
                  'можно запрещать и удалять сразу неограниченное количество слов.\n' \
                  'Главное - это отделять каждое новое слово пробелом.\n' \
                  '7) Бот не поддерживает запрет конкретных словосочетаний.\n' \
                  '8) Доступ к личной базе слов имеет только создатель группы, или, если его нет, человек, который идет дальше по списку (админы, участники ...)\n' \
                  '9) 1 месяц подписки стоит 5 евро/350 рублей/5 долларов.\n\n' \
                  'Если у тебя остались вопросы, пиши сюда: {}.'

    creator_welcome = 'Вся информация о разработке.'
    creator_name = 'Создатель: {}.\n' \
                   'Если есть вопросы, смело пиши.'
    creator_technology = 'Язык программирования: "python 3.10."\n' \
                         'Основная библиотека: "aiogram 2.12."'
    creator_realise = 'Дата выпуска: 08.01.2022.'

    payment = 'Покупка бота.'

    pay = 'Оплатить.'
    pay_success = 'Нажми "Продолжить" для того, чтобы начать регистрацию.'
    please_wait = 'Пожалуйста, подождите ... Загружается видео ...'

    languages_choose = 'Сейчас ты должен выбрать какой язык будет у твоего будущего интерфейса.\n' \
                       'Нужно знать, что алгоритмы работы будут выставлять в приоритет слова на выбранном языке.\n' \
                       'В будущем его НЕЛЬЗЯ будет поменять!\n' \
                       'Это никак не скажется на работе функций бота,\n' \
                       'однако ВСТРОЕННОЕ распознание слов с спецсимволами на другом языке(пример: @pple) станет затруднительным.'

    registration_success = 'Регистрация пройдена успешна!\n' \
                           'По умолчанию, иметь доступ с базе слов будут только админы группы.\n' \
                           'Сейчас тебе осталось нажать /start, и у тебя обновится интерфейс!.\n' \
                           'Приятного пользования!!!'
class ClientTextsEn(ClientTexts):
    welcome_message_firstly = 'Hello, {}! You launched the best chat censoring bot!\n' \
                              'This bot uses the most advanced and innovative work algorithms!\n' \
                              'The bot also provides a personal database of banned words that can be edited.'
    welcome_message = 'Welcome! Click where you want!'

    language_response = 'Language selected successfully!'

    description = 'The video shows an example of how the bot works.\n\n' \
                  'WHAT SHOULD YOU KNOW \U000026A0\n' \
                  '1) If you have an anonymous group, the bot will not be able to recognize the user.\n' \
                  '2) The preset censored word file contains only swear words.\n' \
                  '(Now only Russian and English)\n' \
                  '3) Each bot user (bot admin) has his own separate database of words.\n' \
                  '4) All database updates happen instantly.\n' \
                  '5) If you made a mistake with the ban or unban command.\n' \
                  '(For example, try to ban already banned word)\n' \
                  'The bot will display an appropriate message.\n' \
                  '6) Using the "/Ban" and "/Unban" commands,\n' \
                  'you can ban and unban an unlimited number of words at once.\n' \
                  'The main thing is to separate each new word with a space.\n' \
                  '7) Bot does not support banning specific phrases.\n' \
                  '8) Only creator of the group have access to the personal database of words, or, if he is not in group, the person next down the list (admins, contributors...)\n' \
                  '9) 1 month subscription costs 5 euros/350 rubles/5 dollars.\n\n' \
                  'If you have any questions, write here: {}'

    creator_welcome = 'All information about development'
    creator_name = 'Developer: {}.\n' \
                   'If you have any questions feel free to write.'
    creator_technology = 'Programming language: "python 3.10."\n' \
                         'The main package: "aiogram 2.12."'
    creator_realise = 'Release date: 08.01.2022.'

    payment = 'Bot buying.'
    pay = 'Pay.'
    pay_success = 'Press "Continue" to start registration.'

    please_wait = 'Please wait ... Video is downloading ...'

    languages_choose = 'Now you have to choose which language your future interface will have.\n' \
                       'You need to know that work algorithms will prioritize words in the selected language\n' \
                       'This will not affect the work of the bot functions in any way,\n' \
                       'however, BUILT-IN recognition of words with special characters in another language [example: ябл()к()] will become difficult.'
    registration_success = 'Registration completed successfully!\n' \
                           'By default, only group admins will have access to the word database.\n' \
                           'Now you just have to press /start, and then your interface will be updated!.\n' \
                           'Happy using!!!'


if __name__ == '__main__':
    print((ClientTexts.welcome_message))
