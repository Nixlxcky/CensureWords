import time
import logging
from typing import Union
import urllib.parse as up

import asyncpg
from asyncpg import pool

from create_bot import DATABASE_LINK


url = up.urlparse(DATABASE_LINK)


class AdminCommands:

    def __init__(self):
        self.pool: Union[None, pool.Pool] = None

    @staticmethod
    async def convert_days(days: int) -> int:
        return days * 24 * 60 * 60

    async def create_pool(self):

        self.pool = await asyncpg.create_pool(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            max_inactive_connection_lifetime=2.0,
            max_size=10,
            min_size=1,
        )
        if self.pool:
            logging.info('Database "Admin" connected')

    async def close_pool(self):
        await self.pool.close()
        logging.info('Database "Admin" unconnected')

    ADD_BUYER = 'INSERT INTO buyers(name, language, id, sub_time) VALUES($1, $2, $3, $4)'
    CREATE_BUYER_TABLE = 'CREATE TABLE "{}_words" AS TABLE words_start'

    DELETE_GROUP = 'DELETE FROM groups_and_admins WHERE group_id = $1'
    ADD_ADMIN = 'INSERT INTO groups_and_admins(group_id, admin_id, buyer_id) VALUES($1, $2, $3)'
    UPDATE_ADMIN = 'UPDATE groups_and_admins SET admin_id = $1 WHERE group_id = $2'

    GET_BUYER_ID_GROUP = 'SELECT buyer_id FROM groups_and_admins WHERE group_id = $1'
    GET_BUYER_ID_ADMIN = 'SELECT buyer_id FROM groups_and_admins WHERE admin_id = $1'
    GET_BUYER_NAME = 'SELECT name FROM buyers WHERE id = $1'
    GET_BUYER_IDS = 'SELECT id FROM buyers'
    GET_BUYER_GROUPS = 'SELECT group_id FROM groups_and_admins WHERE buyer_id = $1'

    GET_GROUP_CREATOR = 'SELECT admin_id FROM groups_and_admins WHERE group_id = $1'
    GET_BUYER_LANGUAGE = 'SELECT language FROM buyers WHERE id = $1'

    GET_ADMINS_ID = 'SELECT admin_id FROM groups_and_admins'
    GET_GROUPS_ID = 'SELECT group_id FROM groups_and_admins'

    UPDATE_SUB_TIME = 'UPDATE buyers SET sub_time = $1 WHERE id = $2'
    GET_SUB_TIME = 'SELECT sub_time FROM buyers WHERE id = $1'

    ADD_WORD = 'INSERT INTO "{}_words"(word) VALUES($1)'
    DELETE_WORD = 'DELETE FROM "{}_words" WHERE word = $1'
    READ_WORDS = 'SELECT * FROM "{}_words"'

    ADD_PAYMENT_INFORMATION = 'INSERT INTO payment_information(username, date, currency, total_amount, tg_pm_chg_id, prov_pm_chg_id) VALUES($1, $2, $3, $4, $5, $6)'

    ADD_POSSIBLE_GROUP = 'INSERT INTO possible_groups(group_id, group_tittle) VALUES($1, $2)'
    DELETE_POSSIBLE_GROUP = 'DELETE FROM possible_groups WHERE group_id = $1'
    READ_POSSIBLE_GROUPS_ID = 'SELECT group_id FROM possible_groups'
    READ_POSSIBLE_GROUPS_TITTLES = 'SELECT group_tittle FROM possible_groups'
    GET_POSSIBLE_GROUP_ID = 'SELECT group_id FROM possible_groups WHERE group_tittle = $1'
    UPDATE_POSSIBLE_GROUP_TITTLE = 'UPDATE possible_groups SET group_tittle = $1 WHERE group_id = $2'

    async def add_buyer(self, name: str, language: str, sub_time: int, buyer_id: int):
        args = [name, language, buyer_id, sub_time]
        await self.pool.fetchval(self.ADD_BUYER, *args)
        await self.pool.fetchval(self.CREATE_BUYER_TABLE.format(str(buyer_id)))

    async def add_admin(self, group_id: int, admin_id: int, buyer_id: int, ):
        args = [group_id, admin_id, buyer_id]
        await self.pool.fetchval(self.ADD_ADMIN, *args)

    async def update_admin(self, admin_id: int, group_id: int):
        args = [admin_id, group_id]
        await self.pool.fetchval(self.UPDATE_ADMIN, *args)

    async def read_buyer(self, group_id: int = None, admin_id: int = None, write_buyer_ids: bool = False):
        if group_id is not None:
            buyer_id = await self.pool.fetchval(self.GET_BUYER_ID_GROUP, group_id)
            return buyer_id

        elif admin_id is not None:
            buyer_ids = await self.pool.fetch(self.GET_BUYER_ID_ADMIN, admin_id)
            buyer_ids = list(set([list(buyer_id.values())[0] for buyer_id in buyer_ids]))
            return buyer_ids
        elif write_buyer_ids:
            buyer_ids = await self.pool.fetch(self.GET_BUYER_IDS)
            if not buyer_ids:
                return []

            return [list(buyer_id.values())[0] for buyer_id in buyer_ids]

    async def get_buyer_groups(self, buyer_id: int):
        buyer_groups = await self.pool.fetch(self.GET_BUYER_GROUPS, buyer_id)
        if not buyer_groups:
            return []

        return [list(buyer_group.values())[0] for buyer_group in buyer_groups]

    async def get_buyer_name(self, buyer_id: int):
        return await self.pool.fetchval(self.GET_BUYER_NAME, buyer_id)

    async def update_sub_time(self, buyer_id: int, sub_time: int):
        args = [sub_time, buyer_id]
        await self.pool.fetchval(self.UPDATE_SUB_TIME, *args)

    async def get_sub_status(self, buyer_ids: list):
        flag = True
        for buyer_id in buyer_ids:
            sub_time = await self.pool.fetchval(self.GET_SUB_TIME, buyer_id)
            if int(sub_time) < time.time():
                flag = False

        return flag

    async def get_sub_time(self, buyer_id):
        return await self.pool.fetchval(self.GET_SUB_TIME, buyer_id)

    async def read_admins(self, write_ids: bool = False, write_group_ids: bool = False):
        if write_ids:
            admin_ids = await self.pool.fetch(self.GET_ADMINS_ID)
            if not admin_ids:
                return []

            return [list(admin_id.values())[0] for admin_id in admin_ids]

        if write_group_ids:
            group_ids = await self.pool.fetch(self.GET_GROUPS_ID)
            if not group_ids:
                return []

            return [list(group_id.values())[0] for group_id in group_ids]

    async def get_language(self, buyer_id: list = None, group_id: int = None):
        if group_id is not None:
            buyer_id = [await self.pool.fetchval(self.GET_BUYER_ID_GROUP, group_id)]

        return await self.pool.fetchval(self.GET_BUYER_LANGUAGE, buyer_id[0])

    async def add_word(self, word: str, buyer_id: int):
        await self.pool.fetchval(self.ADD_WORD.format(str(buyer_id)), word)

    async def delete_word(self, word: str, buyer_id: int):
        await self.pool.fetchval(self.DELETE_WORD.format(str(buyer_id)), word)

    async def read_words(self, buyer_id: int):
        words = await self.pool.fetch(self.READ_WORDS.format(str(buyer_id)))
        return words

    async def get_group_creator(self, group_id: int):
        return await self.pool.fetchval(self.GET_GROUP_CREATOR, group_id)

    async def delete_group(self, group_id: int):
        await self.pool.fetchval(self.DELETE_GROUP, group_id)

    async def add_payment_information(self, username: str, date: str, currency: str, total_amount: int,
                                      tg_pm_chg_id: str, prov_pm_chg_id: str):
        args = [username, date, currency, total_amount, tg_pm_chg_id, prov_pm_chg_id]
        await self.pool.fetchval(self.ADD_PAYMENT_INFORMATION, *args)

    async def add_possible_group(self, group_id: int, group_tittle: str):
        args = [group_id, group_tittle]
        await self.pool.fetchval(self.ADD_POSSIBLE_GROUP, *args)

    async def delete_possible_group(self, group_id: int):
        await self.pool.fetchval(self.DELETE_POSSIBLE_GROUP, group_id)

    async def read_possible_groups(self, write_ids: bool = False, write_tittles: bool = False):
        if write_ids:
            group_ids = await self.pool.fetch(self.READ_POSSIBLE_GROUPS_ID)
            if not group_ids:
                return []

            return [list(group_id.values())[0] for group_id in group_ids]

        if write_tittles:
            group_tittles = await self.pool.fetch(self.READ_POSSIBLE_GROUPS_TITTLES)
            if not group_tittles:
                return []
            return [list(group_tittle.values())[0] for group_tittle in group_tittles]

    async def get_possible_group_id(self, group_tittle: str):
        possible_group_id = await self.pool.fetchval(self.GET_POSSIBLE_GROUP_ID, group_tittle)
        return possible_group_id

    async def update_possible_group_tittle(self, group_id: int, new_tittle: str):
        args = [new_tittle, group_id]
        await self.pool.fetchval(self.UPDATE_POSSIBLE_GROUP_TITTLE, *args)


class ClientCommands:

    def __init__(self):
        self.pool: Union[None, pool.Pool] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port,
            max_inactive_connection_lifetime=2.0,
            max_size=10,
            min_size=1,
        )
        if self.pool:
            logging.info('Database "Client" connected')

    async def close_pool(self):
        await self.pool.close()
        logging.info('Database "Client" unconnected')

    ADD_CLIENT = 'INSERT INTO clients (client_id, client_name, language) VALUES($1, $2, $3)'

    GET_CLIENT_LANGUAGE = 'SELECT language FROM clients WHERE client_id = $1'

    GET_CLIENT_IDS = 'SELECT client_id FROM clients'

    DELETE_CLIENT = 'DELETE FROM clients WHERE client_id = $1'

    async def add_client(self, client_id: int, client_name: str, language: str):
        args = [client_id, client_name, language]
        await self.pool.fetchval(self.ADD_CLIENT, *args)

    async def read_client(self, client_id: int = None, write_ids: bool = False):
        if client_id is not None:
            language = await self.pool.fetchval(self.GET_CLIENT_LANGUAGE, client_id)
            return language
        if write_ids:
            client_ids = await self.pool.fetch(self.GET_CLIENT_IDS)
            if client_ids is None:
                return []
            return [list(client_id.values())[0] for client_id in client_ids]

    async def delete_client(self, client_id: int):
        await self.pool.fetchval(self.DELETE_CLIENT, client_id)


if __name__ == '__main__':
    pass