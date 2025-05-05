from abc import ABC


class AdminTexts(ABC):

    @staticmethod
    def get_admin(language: str):
        if language.strip() == 'rus':
            return AdminTextsRus
        elif language.strip() == 'en':
            return AdminTextsEn

        return 'Check the languages!!!'

    help_text: str = None

    ban_command: str = None
    unban_command: str = None
    cancel_command: str = None

    ban_word_success: str = None
    ban_word_failure: str = None

    unban_word_success: str = None
    unban_word_failure: str = None
    unban_word_possible: str = None

    ask_subscription: str = None


class AdminTextsRus(AdminTexts):
    help_text = 'Выбери команду!\n' \
                'Просмотреть - просмотреть ВСЕ запрещенные слова (команда присылает текстовой файл).\n' \
                'Удалить - удалить ключевое слово/слова из списка запрещенных.\n' \
                'Запретить - запретить ключевое слово/слова.'

    ban_command = 'Напиши ключевое слово/слова, которые хочешь запретить.\n' \
                  'Каждое новое слово отделяй пробелом \U0001F447'
    unban_command = 'Напиши ключевое слово/слова, которые удалить из списка запрещенных.\n' \
                    'Каждое новое слово отделяй пробелом \U0001F447'
    cancel_command = '\U0001F6AB Действие отменено \U0001F6AB'

    ban_word_success = "Ключевое слово '{}' успешно запрещено \U00002705 buyer_name: {}\n"
    ban_word_failure = "Ключевое слово '{}' уже запрещено \U0000274c buyer_name: {}\n"

    unban_word_success = "Ключевое слово '{}' успешно удалено из списка запрещенных \U00002705 buyer_name: {}\n{}\n"  # third - '*' * 30
    unban_word_failure = "Ключевого слова '{}' нет в списке запрещенных \U0000274c buyer_name: {}\n{}\n"  # third - '*' * 30
    unban_word_possible = "Ключевого слова '{}' нет в списке запрещенных \U0000274c\n" \
                          "Возможно вы имели ввиду следующие слова: {} \U0001F914 buyer_name: {}\n{}\n"  # first - word, second - possible_words, fourth - '*' * 30

    ask_subscription = 'Время подписки на бота подошло к концу! Попросите человека, который приобрел подписку у бота, продлить ее.'


class AdminTextsEn(AdminTexts):
    help_text = 'Choose command!\n' \
                'View - view ALL censored words (the command sends a text file).\n' \
                'Unban - remove the word(s) from the banned list.\n' \
                'Ban - ban word(s).'

    ban_command = 'Write the word(s) you want to ban.\n' \
                  'Separate each new word with a space \U0001F447'
    unban_command = 'Write the word(s) to be removed from the banned list.\n' \
                    'Separate each new word with a space \U0001F447'
    cancel_command = '\U0001F6AB Action canceled \U0001F6AB'

    ban_word_success = "Word '{}' banned successfully \U00002705 buyer_name: {}\n"
    ban_word_failure = "Word '{}' is already banned \U0000274c buyer_name: {}\n"

    unban_word_success = "Word '{}' successfully removed from the banned list \U00002705 buyer_name: {}\n{}\n"  # third - '*' * 30
    unban_word_failure = "Word '{}' is not in the banned list \U0000274c buyer_name: {}\n{}\n"  # third - '*' * 30
    unban_word_possible = "Word '{}' is not in the banned list \U0000274c\n" \
                          "Perhaps you meant the following words: {} \U0001F914 buyer_name: {}\n{}\n"  # first - word, second - possible_words, fourth - '*' * 30
    ask_subscription = 'Bot subscription time has come to an end! Ask the person who purchased the bot subscription  to renew it.'

if __name__ == '__main__':
    print(AdminTexts.get_admin('rus').help_text)
