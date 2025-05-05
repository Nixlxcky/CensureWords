import itertools
import string

import aiogram.utils.exceptions
from aiogram import types, Dispatcher
from cleantext import remove_emoji

from create_bot import bot, db_admins
from help_functions import check_edit_groups


async def user_text(language: str) -> str:
    sample = '<i><b>{}</b></i>:'
    if language == 'rus':
        return sample.format('Пользователь')
    elif language == 'en':
        return sample.format('User')
    return 'Check the languages!!'


async def bot_cant_delete(language: str) -> str:
    if language == 'rus':
        return '<i>Бот не может удалить сообщение, выдай ему нужные права</i>\n'
    elif language == 'en':
        return '<i>Bot cannot delete message, give it rights</i>\n'


async def get_letters_dict(language: str) -> dict:
    rus_en = {'а': ['а', '@', 'ā', 'a', 'а', 'а'],
              'б': ['б', '6', 'b', 'б', 'б'],
              'в': ['в', 'v', 'b', 'в', 'в', 'в'],
              'г': ['г', 'g', 'ğ', 'г', 'г', 'г'],
              'д': ['д', 'd', 'д', 'д', 'д'],
              'е': ['е', 'je', 'ē', 'je', 'ə', 'е', 'Ә', 'e'],
              'ё': ['ё', 'e', 'є'],
              'ж': ['ж', 'zh', '*', 'ж'],
              'з': ['з', '3', 'z', 'з'],
              'и': ['и', 'i', 'ī', '!', 'и', 'ї', 'і', 'і', '|/|', 'ї', '¡'],
              'й': ['й', 'j', 'й', 'ӣ', 'й', 'й'],
              'к': ['к', 'k', 'i{', '|{', 'қ', '|(', 'қ', 'к', 'к'],
              'л': ['л', 'l', 'i', 'љ', 'л', r'/\''],
              'м': ['м', 'm', 'ფ', 'м'],
              'н': ['н', 'n', 'њ', 'ң' 'н', '№'],
              'о': ['о', 'o', '0', '#', 'ö', 'ტ', 'ө', 'о', 'о', 'о', '()'],
              'п': ['п', 'n', 'п', 'п', 'p'],
              'р': ['р', 'r', '₽'],
              'с': ['с', 's', 'ç', 'c', 'с', 'с', '$', '§'],
              'т': ['т', 'm', 't', 'т'],
              'у': ['у', 'u', 'џ', 'ū', 'ü', 'ў', 'ყ', 'ү', 'y', 'ӯ', '¥'],
              'ф': ['ф', 'f', 'ғ', 'ғ', 'ф'],
              'х': ['х', 'x', 'h', '}{', ')(', '][', 'ђ', 'ћ', 'ҳ', 'х', '><', '≥≤'],
              'ц': ['ц', 'c'],
              'ч': ['ч', 'ch', '4', 'ҷ', 'ч', 'ч'],
              'ш': ['ш', 'sh', '|_|_|', 'ш'],
              'щ': ['щ', 'sch'],
              'ь': ['ь', 'b'],
              'э': ['э', 'e', 'э'],
              'ы': ['ы', 'i'],
              'ъ': ['ъ', 'ъ'],
              'ю': ['ю', 'io', 'ю'],
              'я': ['я', 'ya', 'ja', 'я', 'я']
              }
    en_rus = {'a': ['a', 'а', '@'],
              'b': ['b', 'б', '@'],
              'c': ['c', 'с', 'ц', '(', 'ж', 'к', 'ч'],
              'd': ['d', 'д', 'ь'],
              'e': ['e', 'e', 'ё', 'э'],
              'f': ['f', 'ф'],
              'g': ['g', 'г'],
              'h': ['h', 'х', 'ч'],
              'i': ['i', 'и', '|'],
              'j': ['j', 'й', 'дж'],
              'k': ['k', 'к'],
              'l': ['l', 'л'],
              'm': ['m', 'м'],
              'n': ['n', 'н'],
              'o': ['o', 'о', '0', '()'],
              'p': ['p', 'п', 'p'],
              'q': ['q', 'о'],
              'r': ['r', 'р'],
              's': ['s', 'с'],
              't': ['t', 'т'],
              'u': ['u', 'у'],
              'v': ['v', 'в'],
              'w': ['w', 'в'],
              'x': ['x', 'х', '}{'],
              'y': ['y', 'у'],
              'z': ['z', 'з', '2', 'ж']

              }

    if language == 'rus':
        return rus_en
    elif language == 'en':
        return en_rus


def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


fast_distance = lambda word, other_word: distance(word, other_word) <= len(other_word) * 0.17


async def change_letters(text: str, letters_dict: dict) -> str:
    for rus_letter, en_letters in letters_dict.items():
        for en_letter in en_letters:
            if en_letter in text and len(en_letter) > 1:
                text = text.replace(en_letter, rus_letter)

    for rus_letter, en_letters in letters_dict.items():
        for en_letter in en_letters:
            if en_letter in text and len(en_letter) == 1:
                text = text.replace(en_letter, rus_letter)

    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()


async def remove_punctuation(text: str) -> str:
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower()


async def remove_double_letters(text: str) -> str:
    text = ''.join(ch for ch, _ in itertools.groupby(text.lower())).strip()
    return text.lower()


async def censure_word_list(message_text: list, word: str) -> list:
    word_index = message_text.index(word)
    message_text[word_index] = message_text[word_index].replace(word, len(word) * '*').lower()
    return message_text


async def send_correct_message(message: types.Message, file: dict, caption: str = None, reply_to_message: bool = False):
    try:
        file_items = list(file.items())[0][1]
        file_keys = file.keys()
        if reply_to_message:
            if 'text' in file_keys:
                await message.reply_to_message.reply(text=caption)
            elif 'video' in file_keys:
                await message.reply_to_message.reply_video(
                    video=file_items,
                    caption=caption,
                )
            elif 'photo' in file_keys:
                await message.reply_to_message.reply_photo(
                    photo=file_items,
                    caption=caption,
                )
            elif 'document' in file_keys:
                await message.reply_to_message.reply_document(
                    document=file_items,
                    caption=caption,
                )
        else:
            if 'text' in file_keys:
                await message.answer(text=caption)
            elif 'video' in file_keys:
                await message.answer_video(
                    video=file_items,
                    caption=caption,
                )
            elif 'photo' in file_keys:
                await message.answer_photo(
                    photo=file_items,
                    caption=caption,
                )
            elif 'document' in file_keys:
                await message.answer_document(
                    document=file_items,
                    caption=caption,

                )
    except:
        return None


async def words_filter(message: types.Message):
    await check_edit_groups()

    if message.chat.id in await db_admins.read_admins(write_group_ids=True) and await db_admins.get_sub_status(
            [await db_admins.read_buyer(group_id=message.chat.id)]):
        if message.text is not None or message.caption is not None:

            flag_edit = False
            flag_continue = False

            buyer_id = await db_admins.read_buyer(group_id=message.chat.id)
            admin_language = await db_admins.get_language([buyer_id])
            admin_letters_dict = await get_letters_dict(admin_language)

            message_text = message.text or message.caption
            message_text = ' '.join(remove_emoji(message_text).split())

            if message.chat.id != message.from_user.id:
                telegram_group_admins = await bot.get_chat_administrators(message.chat.id)
                group_admins = list(filter(lambda admin: not admin['user']['is_bot'], telegram_group_admins))
                telegram_group_creator = group_admins[0]['user'][
                    'id']
                database_group_creator = await db_admins.get_group_creator(message.chat.id)

                if int(telegram_group_creator) != int(database_group_creator):
                    await db_admins.update_admin(int(telegram_group_creator), message.chat.id)

            censored_words = [word[0] for word in await db_admins.read_words(buyer_id)]
            space_coefficient = (len(message_text.split())) / (len(message_text) or 1)

            censored_words.sort(key=lambda x: len(x), reverse=True)

            for fake_key, fake_word in fake_ban.items():
                for message_part in range(len(fake_word)):
                    message_fragment = message_text[message_part: message_part + len(fake_word)]
                    if fake_word in message_fragment.lower():
                        message_text = message_text.replace(message_fragment, fake_key)

            if 0.13 < space_coefficient < 0.18:
                message_text = message_text.split()
                for word in message_text:
                    for censored_word in censored_words:
                        if fast_distance(word, censored_word):
                            # word without fictions
                            message_text = await censure_word_list(message_text, word)
                            flag_edit = True
                            break
                        elif fast_distance(await remove_double_letters(await remove_punctuation(word)), censored_word):
                            # word without double letters and punctuation
                            message_text = await censure_word_list(message_text, word)
                            flag_edit = True
                            break
                        elif fast_distance(await remove_double_letters(await change_letters(word, admin_letters_dict)),
                                           censored_word):
                            # word without double letters, and with changed letters
                            message_text = await censure_word_list(message_text, word)
                            flag_edit = True
                            break

                message_text = ' '.join(message_text)
            else:
                for message_part in range(len(message_text)):
                    for censored_word in censored_words:
                        message_fragment = message_text[message_part: message_part + len(censored_word)]
                        if fast_distance(message_fragment, censored_word):
                            # message_fragment without fictions
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')
                            flag_edit = True
                            break

                        elif fast_distance(await remove_double_letters(await remove_punctuation(message_fragment)),
                                           censored_word):
                            # message_fragment without double_letters
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')
                            flag_edit = True
                            break

                        elif fast_distance(
                                await remove_double_letters(await change_letters(message_fragment, admin_letters_dict)),
                                censored_word):
                            # message_fragment without double_letters, with changed letters
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')
                            flag_edit = True
                            break


            for censored_word in censored_words:
                if censored_word in await change_letters(await remove_double_letters(message_text.replace(' ', '')),
                                                         admin_letters_dict) \
                        or censored_word in await remove_double_letters(message_text.replace(' ', '')) \
                        or censored_word in await remove_punctuation(message_text.replace(' ', '')) \
                        or censored_word in await remove_double_letters(
                    await remove_punctuation(message_text.replace(' ', ''))):
                    flag_continue = True
                    break

            if flag_continue:

                for message_part in range(len(message_text)):
                    for censored_word in censored_words:
                        message_fragment = message_text[message_part: message_part + len(censored_word) * 3]
                        if fast_distance(message_fragment.replace(' ', '').lower(), censored_word):
                            # message_fragment without fictions
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')

                            break

                        elif fast_distance(await remove_double_letters(
                                await remove_punctuation(message_fragment.replace(' ', ''))), censored_word):

                            # message_fragment without double_letters
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')
                            break
                        elif censored_word in await change_letters(
                                await remove_double_letters(message_fragment.replace(' ', '')), admin_letters_dict):
                            message_text = list(message_text)
                            message_text[message_part: message_part + len(censored_word) * 3] = (
                                await change_letters(await remove_double_letters(message_fragment.replace(' ', '')),
                                                     admin_letters_dict)).replace(censored_word,
                                                                                  '*' * len(censored_word))
                            message_text = ''.join(message_text)

                            break
                        elif fast_distance(await remove_double_letters(
                                await change_letters(message_fragment.replace(' ', ''), admin_letters_dict)),
                                           censored_word):
                            # message_fragment without double_letters, with changed letters
                            message_text = message_text.replace(message_fragment, len(message_fragment) * '*')

                            break
                flag_edit = True

            if flag_edit:
                name = (message.from_user.first_name + str(
                    message.from_user.last_name or '')) or message.from_user.username

                text = f'{await user_text(admin_language)} {name}\n{message_text}'

                try:
                    await message.delete()
                except aiogram.utils.exceptions.MessageCantBeDeleted:
                    text = await bot_cant_delete(admin_language) + text

                if message.content_type == 'photo':
                    message_file_id = message.photo[-1]['file_id']
                elif message.content_type in ['document', 'video']:
                    message_file_id = message[message.content_type]['file_id']
                else:
                    message_file_id = None

                if message.reply_to_message is not None:
                    await send_correct_message(
                        message=message,
                        file={message.content_type: message_file_id},
                        caption=text,
                        reply_to_message=True
                    )
                else:
                    await send_correct_message(
                        message=message,
                        file={message.content_type: message_file_id},
                        caption=text
                    )


def register_handlers_words_filter(dp: Dispatcher):
    dp.register_message_handler(words_filter, content_types=['text', 'video', 'photo', 'document'])


if __name__ == '__main__':
    db_admins.create_pool()
