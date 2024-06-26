import asyncio
import sqlite3 as sq
import logging


async def Create_baza():
    con = sq.connect("./bazas/UsersBaza.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id Integer, 
        sposob Integer,
        status Ineger
        )
        ''')
    con.close()
    logging.info("База данных создана или уже существует.")


async def check_user(user_id):
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f'select user_id from users where user_id = {user_id}'
    cur.execute(query)
    is_true = cur.fetchone()
    con.close()
    logging.info(f"Проверка пользователя {user_id}: {'найден' if is_true else 'не найден'}")
    return is_true is not None


async def add_user(user_id: int):
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    cur.execute('INSERT INTO users(user_id, sposob,status) VALUES(?,?,?)', (user_id, 0, 0))
    con.commit()
    con.close()
    logging.info(f"Пользователь {user_id} добавлен в базу данных.")


async def update_status(user_id: int):
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f"Update users set status = 1 where user_id = {user_id}"
    cur.execute(query)
    con.commit()
    con.close()
    logging.info(f"Статус пользователя {user_id} обновлен.")


async def get_ids():
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f'select user_id from users where status = 1'
    cur.execute(query)
    result = cur.fetchall()
    logging.info(f"Получены ID пользователей со статусом 1: {result}")
    return result


async def get_sposob(user_id):
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f'select sposob from users where user_id = {user_id}'
    cur.execute(query)
    number = cur.fetchone()
    logging.info(f"Способ пользователя {user_id}: {number}")
    return number


async def update_sposob(user_id, number):
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f"Update users set sposob = {number} where user_id = {user_id}"
    cur.execute(query)
    con.commit()
    con.close()
    logging.info(f"Способ пользователя {user_id} обновлен до {number}.")


async def get_lines():
    con = sq.connect("./bazas/UsersBaza.db")
    con.row_factory = lambda cursor, row: row[0]
    cur = con.cursor()
    query = f'select text from textes where text is not null'
    cur.execute(query)
    lines = cur.fetchall()
    logging.info(f"Получены строки из базы данных")
    return lines
