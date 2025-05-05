from aiogram.utils.exceptions import ChatNotFound, BotKicked

from create_bot import bot, db_admins


async def check_edit_groups():
    for group_id in await db_admins.read_admins(write_group_ids=True):
        try:
            await bot.get_chat(group_id)
        except ChatNotFound:
            print('ChatNotFound', group_id)
            await db_admins.delete_group(group_id)
        except BotKicked:

            print('Bot kicked', group_id)
            await db_admins.delete_group(group_id)