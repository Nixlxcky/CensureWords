from abc import ABC

from aiogram import types


class BuyerTexts(ABC):

    @staticmethod
    def get_buyer(language: str):
        if language.strip() == 'rus':
            return BuyerTextsRus
        elif language.strip() == 'en':
            return BuyerTextsEn

        return 'Check the languages!!!'

    help_text: str = None
    add_group_text: str = None
    add_group_command: str = None

    add_group_success: str = None

    delete_group_text: str = None
    bot_was_kicked: str = None
    delete_group_success: str = None
    add_group_fail: str = None
    group_already_exists: str = None

    limit_of_groups: str = None

    buy_subscription: str = None
    subscription_info: str = None

    select_currency: str = None

    PRICE_EUR: types.LabeledPrice = None
    PRICE_RUB: types.LabeledPrice = None
    PRICE_USD: types.LabeledPrice = None

    renew_subscription: str = None
    renew_subscription_info: str = None
    successful_payment: str = None

    error_payment_message: str = None


class BuyerTextsRus(BuyerTexts):
    add_group_command = 'Тебе нужно добавить бота в группу и дать ему права админа.\n' \
                        'Пожалуйста, не меняй название группы в ближайшее время.'
    add_group_text = 'Пришли название (tittle) группы, которую хочешь добавить.\n' \
                     'Пожалуйста, пришли название группы без лишних символов, лучше просто скопируй его.'
    help_text = 'Так как ты покупатель, ты можешь добавлять и удалять группы из бота.\n' \
                'Добавить_группу - нажми, чтобы добавить группу. Всего можно добавить 5 групп.\n' \
                'Удалить_группу - нажми, чтобы удалить группу из своего списка.'
    add_group_success = 'Группа успешно добавлена! Еще можно добавить {}/5 групп \U00002705\n' \
                        'Нажми /start, и если ты создатель добавленной группы, то у тебя обновиться интерфейс!'
    delete_group_text = 'Нажми на название той группы, которую хочешь удалить из бота.'
    bot_was_kicked = '\nПожалуйста, удаляй группу из бота перед тем как удалять бота из твоей группы.\n' \
                     'Чтобы удалить группу из бота, которой нет в этом сообщении,\n' \
                     'верни бота в твой чат, дай ему права админа и используй эту команду еще раз.'
    delete_group_success = 'Группа с названием - "{}" успешна удалена \U00002705\n' \
                           'У тебя осталось {}/5 групп.'
    limit_of_groups = 'Ты не можешь больше добавить группу, воспользуйся командой /Удалить_группу, чтобы освободить место.'

    buy_subscription = 'Твое время подписки на бота подошло к концу! Воспользуйся командой "/Продлить_подписку", чтобы продлить подписку еще на один месяц.'
    subscription_info = 'Твоя нынешняя подписка действительна, примерно, до этой даты: {}.\n' \
                        'Нажми "Продолжить", если хочешь продлить подписку на 30 дней ( ≈ {}).'

    PRICE_EUR = types.LabeledPrice(label='Продление подписки.', amount=500)
    PRICE_RUB = types.LabeledPrice(label='Продление подписки.', amount=35000)
    PRICE_USD = types.LabeledPrice(label='Продление подписки.', amount=500)

    renew_subscription = 'Продление подписки.'
    renew_subscription_info = 'Твое нынешняя подписка действительна, примерно, до этой даты: {}.\n' \
                              'Оплати, чтобы продлить подписку на 30 дней ( ≈ {}).'
    successful_payment = 'Оплата прошла успешно! Твоя подписка продлена до этой даты: ≈ {}.\n' \
                         'Приятного пользования! \U0001F91D'
    select_currency = 'Выбери валюту.'

    error_payment_message = 'Что - то пошло не так. Попробуй заплатить еще раз через несколько минут.'
    add_group_fail = 'Что - то пошло не так ...\n' \
                     'Возможно ты забыл добавить бота в группу и дать ему права админа, или ты ошибся в написании названия группы.\n' \
                     'Убедись в том, что ты выполнил все пункты правильно, и попробуй прислать название группы еще раз.\n' \
                     'Если проблема все еще не решена, попробуй удалить бота из группы и добавить заново, выдав прав админа.'
    group_already_exists = 'Эта группа уже зарегистрирована!!!\n' \
                           'Пришли название другой группы'


class BuyerTextsEn(BuyerTexts):
    add_group_command = 'You must add the bot to the right group and give him an admin rights.\n' \
                        'Please do not change the name of group in the neat future.'
    add_group_text = 'Send the name (title) of the group you want to add.\n' \
                     'Please send the name of the group without extra characters, it is better to just copy it.'
    help_text = 'Since you are an buyer, you can add or delete groups from bot.\n' \
                'Add_group - click to add group. A total of 5 groups can be added.\n' \
                'Delete_group - click to delete group from bot.'
    add_group_success = 'Group added successfully! You can also add {}/5 groups \U00002705\n' \
                        'Press /start, and if you are the creator of the added group, then your interface will be updated!'
    delete_group_text = 'Click on the name of the group you want to remove from the bot.'
    bot_was_kicked = '\nPlease, remove a group from a bot before removing a bot from your group.\n' \
                     'To remove a group from a bot that is not in this message,\n' \
                     'return the bot to your chat, give it admin rights and use this command again.'
    delete_group_success = 'Group with name - {}" successfully deleted \U00002705\n' \
                           'Remaining groups: {}/5.'

    limit_of_groups = 'You cannot add an additional group, use command /Delete_group to free up space.'

    buy_subscription = 'Bot subscription time has come to the end! Use the "/Renew_subscription" command to renew your subscription for another month.'
    subscription_info = 'Your current subscription is valid until around this date: {}.\n' \
                        'Press "Continue" if you want renew subscription for 30 days ( ≈ {}).'

    PRICE_EUR = types.LabeledPrice(label='Subscription renewing.', amount=500)
    PRICE_RUB = types.LabeledPrice(label='Subscription renewing.', amount=35000)
    PRICE_USD = types.LabeledPrice(label='Subscription renewing.', amount=500)

    renew_subscription = 'Subscription renewing.'
    renew_subscription_info = 'Your current subscription is valid until around this date: {}.\n' \
                              'Pay to renew subscription for 30 days ( ≈ {}).'
    successful_payment = 'Payment is successful! Your subscription is valid until this date: ≈ {}.\n' \
                         'Happy using! \U0001F91D'
    select_currency = 'Select currency. '

    error_payment_message = 'Something went wrong. Tryto pay again in few minutes.'

    add_group_fail = 'Something went wrong . . .\n' \
                     'Perhaps you forgot to add the bot to the group and give it admin rights, or you made a mistake in writing the group name.\n' \
                     'Make sure that you have completed all the steps correctly, and try to send the name of the group again.\n' \
                     'If the problem is still not resolved, try removing the bot from the group and adding it again with admin rights.'
    group_already_exists = 'This group with is already registered!\n' \
                           'Call the other tittle of group.'
