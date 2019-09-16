import urllib.request, urllib.parse, urllib.error
import sqlite3, random

def makeLotto() :
    _lotto = list()

    while len(_lotto) < 6 :
        _no = random.randint(1, 45)

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

# retrieve latest lotto info and insert
_response = urllib.request.urlopen("http://lotto.kaisyu.com/api?method=get")
_dict = json.loads(_response.read())
# print(_dict)
# {'bnum': 24, 'gno': 876, 'gdate': '2019-09-14', 'nums': [5, 16, 21, 26, 34, 42]}
_gno = _dict["gno"]
_nums = _dict["nums"]
_nums.insert(0, _gno)
_latestLotto = tuple(_nums)
csr.execute("INSERT OR IGNORE INTO Lotto (SEQ, NO1, NO2, NO3, NO4, NO5, NO6) VALUES (?, ?, ?, ?, ?, ?, ?)", _latestLotto)
con.commit()

inputNum = 0
lottoCnt = 0

try :
    _input = input("How many lotto No. (Default 1) : ")
    inputNum = int(_input)

except KeyboardInterrupt :
    print("Program interrupted by user....")

except Exception as e :
    print("Exception : ", e)
    print("Run as 1")
    inputNum = 1

print()

while lottoCnt < inputNum :
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

    # if duplicate. retry
    if _row is not None :
        continue

    else :
        lottoCnt += 1

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

        _row = csr.fetchone()

        if not _row :
            # insert new my lotto No.
            csr.execute('''
                    INSERT INTO MyLotto (NO1, NO2, NO3, NO4, NO5, NO6, COUNT, REG_DT, MOD_DT)
                    VALUES (?, ?, ?, ?, ?, ?, 1, DATETIME('now', 'localtime'), DATETIME('now', 'localtime'))
            ''', _lotto)
            print("New Lotto :", end=" ")

        else :
            # update COUNT, MOD_DT of existing my lotto No.
            csr.execute("UPDATE MyLotto SET COUNT = COUNT + 1, MOD_DT = DATETIME('now', 'localtime') WHERE SEQ = :SEQ", {"SEQ":_row["SEQ"]})
            print("Old Lotto :", end=" ")

        print("%05s %05s %05s %05s %05s %05s" % _lotto)
        con.commit()

print()

csr.execute("SELECT * FROM (SELECT * FROM MyLotto ORDER BY SEQ DESC LIMIT ?) ORDER BY SEQ ASC", (inputNum, ))
cols = [col[0] for col in csr.description]

# print header
print("{:>5} | {:>5} {:>5} {:>5} {:>5} {:>5} {:>5} {:>8} {:20} {:20}".format(cols[0], cols[1], cols[2], cols[3], cols[4], cols[5], cols[6], cols[7], cols[8], cols[9]))
print("--" * 50)

# print data
rows = csr.fetchall()
for row in rows:
    print("{:5} | {:5} {:5} {:5} {:5} {:5} {:5} {:8} {:20} {:20}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

csr.close()
con.close()
