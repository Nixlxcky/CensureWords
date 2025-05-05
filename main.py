import logging

from aiogram.utils import executor

from create_bot import dp, bot, db_clients, db_admins
from handlers import admin, words_filter, start, client, buyer



async def on_startup_pol(dip):
    await db_clients.create_pool()
    await db_admins.create_pool()



async def on_shutdown_pol(dip):
    await db_clients.close_pool()
    await db_admins.close_pool()



if __name__ == '__main__':

    start.register_handlers_start(dp)
    client.register_handlers_client(dp)
    admin.register_handlers_admin(dp)
    buyer.register_handlers_buyer(dp)
    words_filter.register_handlers_words_filter(dp)
    
    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dispatcher=dp, on_startup=on_startup_pol, on_shutdown=on_shutdown_pol, skip_updates=True)
