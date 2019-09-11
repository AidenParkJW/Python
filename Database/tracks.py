import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect("trackdb.sqlite")
csr = conn.cursor()

# Make some fresh tables using executescript()
csr.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

def lookup(track, keyName) :
    found = False

    for ele in track :
        if found :
            return ele.text

        if ele.tag == "key" and ele.text == keyName :
            found = True

    return None

xmlFilename = input("Enter Filename : ")

if not xmlFilename :
    xmlFilename = "Library.xml"

_xml = ET.parse(xmlFilename)
# print(type(_xml))   # <class 'xml.etree.ElementTree.ElementTree'>

_trackList = _xml.findall("dict/dict/dict")
print("Track count :", len(_trackList))

# enumerate makes and returns the tuple that has sequence.
for i, _track in enumerate(_trackList) :
    if lookup(_track, "Track ID") is None :
        continue

    _trackId    = lookup(_track, "Track ID")
    _name       = lookup(_track, "Name")
    _artist     = lookup(_track, "Artist")
    _album      = lookup(_track, "Album")
    _count      = lookup(_track, "Play Count")
    _rating     = lookup(_track, "Rating")
    _length     = lookup(_track, "Total Time")

    if _name is None or _artist is None or _album is None or _count is None or _rating is None or _length is None:
        continue

    print("{:3} {:10} {:50} {:30} {:30} {:10} {:10} {:10}".format(i, _trackId, _name, _artist, _album, _count, _rating, _length))

    csr.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)", (_artist,))
    csr.execute("SELECT id FROM Artist WHERE name = ?", (_artist,))
    _artist_id = csr.fetchone()[0]

    csr.execute("INSERT OR IGNORE INTO Album (title, artist_id) VALUES (?, ?)", (_album, _artist_id))
    csr.execute("SELECT id FROM Album WHERE title = ?", (_album,))
    _album_id = csr.fetchone()[0]

    csr.execute('''INSERT OR REPLACE INTO Track (title, album_id, len, rating, count)
                   VALUES (?, ?, ?, ?, ?)''', (_name, _album_id, _length, _rating, _count))

    conn.commit()

csr.close()
conn.close()
