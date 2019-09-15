import sqlite3

con = sqlite3.connect("lotto.sqlite")
con.row_factory = sqlite3.Row
csr = con.cursor()

csr.executescript('''
    CREATE TABLE IF NOT EXISTS Lotto
    ( SEQ   INTEGER PRIMARY KEY
    , NO1   INTEGER NOT NULL
    , NO2   INTEGER NOT NULL
    , NO3   INTEGER NOT NULL
    , NO4   INTEGER NOT NULL
    , NO5   INTEGER NOT NULL
    , NO6   INTEGER NOT NULL
    );

    DELETE FROM Lotto;
''')

_lotto = list()
# This file is in reverse order.
fh = open("lotto.txt")
for i, row in enumerate(fh) :
    print(i, end=" ")
    _lotto.insert(0, tuple(row.rstrip().split()))    # type of tuple of list

_values = tuple(_lotto) # convert type of tuple of tuples
csr.executemany("INSERT INTO Lotto (NO1, NO2, NO3, NO4, NO5, NO6) VALUES (?, ?, ?, ?, ?, ?)", _values)
con.commit()
csr.close()
con.close()
