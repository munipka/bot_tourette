import config
from DBcm import UseDatabase

dbname = config.db_name


def create_table():
    with UseDatabase(dbname) as cursor:
        _SQL = """CREATE TABLE IF NOT EXISTS words(
        num INTEGER PRIMARY KEY,
        WORD TEXT);
        """
        cursor.execute(_SQL)


def get_word(num):
    with UseDatabase(dbname) as cursor:
        _SQL = """SELECT word FROM words
        WHERE num=?"""
        cursor.execute(_SQL, (num,))
        return cursor.fetchall()


def add_words(word):
    with UseDatabase(dbname) as cursor:
        _SQL = """INSERT INTO words (word)
        VALUES(?);"""
        cursor.execute(_SQL, (word,))


def update_table():
    with open("words.txt", "r", encoding="utf8") as file:
        for line in file:
            add_words(line)


create_table()
update_table()
