import sqlite3
from pathlib import Path

"""
parents[0] - app/repositories
parents[1] - app/

resolve() - full absolute path    
"""
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "german_nouns_only.db"


def lookup_noun(noun):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    #(noun,) - means it's a tuple containing one value
    #Tuple - immutable, ordered list, can contain almost anything
    # Do not just use a string, as sql might see it as an iterable element
    cursor.execute("SELECT word, gender FROM entries WHERE word = ? COLLATE NOCASE", (noun,))
    rows = cursor.fetchall()
    connection.close()


    return rows



#print(lookup_noun("Sonne"))
