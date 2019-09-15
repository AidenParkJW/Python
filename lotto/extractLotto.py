import sqlite3, random

def makeLotto() :
    _lotto = list()

    while len(_lotto) < 6 :
        _no = random.randrange(1, 45)

        if _no in _lotto :
            continue

        else :
            _lotto.append(_no)

    _lotto.sort()
    return tuple(_lotto)

con = sqlite3.connect("lotto.sqlite")
con.row_factory = sqlite3.Row
csr = con.cursor()

csr.executescript('''
    CREATE TABLE IF NOT EXISTS MyLotto
    ( SEQ       INTEGER PRIMARY KEY
    , NO1       INTEGER NOT NULL
    , NO2       INTEGER NOT NULL
    , NO3       INTEGER NOT NULL
    , NO4       INTEGER NOT NULL
    , NO5       INTEGER NOT NULL
    , NO6       INTEGER NOT NULL
    , COUNT     INTEGER NOT NULL DEFAULT 1
    , REG_DT    TEXT NOT NULL
    , MOD_DT    TEXT NOT NULL
    );
''')

while True :
    _lotto = makeLotto()

    csr.execute('''
        SELECT *
        FROM Lotto
        WHERE NO1   = ?
        AND NO2     = ?
        AND NO3     = ?
        AND NO4     = ?
        AND NO5     = ?
        AND NO6     = ?
    ''', _lotto)

    _row = csr.fetchone()

    # if duplicate.
    if _row is not None :
        continue

    else :
        csr.execute('''
            SELECT *
            FROM MyLotto
            WHERE NO1   = ?
            AND NO2     = ?
            AND NO3     = ?
            AND NO4     = ?
            AND NO5     = ?
            AND NO6     = ?
        ''', _lotto)

        _myLotto = csr.fetchone()

        if not _myLotto :
            # insert new my lotto No.
            csr.execute('''
                    INSERT INTO MyLotto (NO1, NO2, NO3, NO4, NO5, NO6, COUNT, REG_DT, MOD_DT)
                    VALUES (?, ?, ?, ?, ?, ?, 1, DATETIME('now', 'localtime'), DATETIME('now', 'localtime'))
            ''', _lotto)
            print("New Lotto : ", end=" ")

        else :
            # update COUNT, MOD_DT of existing my lotto No.
            csr.execute('''UPDATE MyLotto SET COUNT = COUNT + 1, MOD_DT = DATETIME('now', 'localtime')
                WHERE NO1   = ?
                AND NO2     = ?
                AND NO3     = ?
                AND NO4     = ?
                AND NO5     = ?
                AND NO6     = ?
            ''', _lotto)
            print("Existing Lotto : ", end=" ")

        print(_lotto)
        break

con.commit()
csr.close()
con.close()
