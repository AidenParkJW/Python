import urllib.request, urllib.parse, urllib.error
import sqlite3
import ssl
from bs4 import BeautifulSoup

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect("spider.sqlite")
# if specified like this one, returns dictionary cursor, otherwise underly returns a tuple of tuples.
conn.row_factory = sqlite3.Row
csr = conn.cursor()

csr.executescript('''
    CREATE TABLE IF NOT EXISTS Pages
    ( id INTEGER PRIMARY KEY
    , url TEXT UNIQUE
    , html TEXT
    , error INTEGER
    , old_rank REAL
    , new_rank REAL);

    CREATE TABLE IF NOT EXISTS Links
    ( from_id INTEGER
    , to_id INTEGER);

    CREATE TABLE IF NOT EXISTS Webs
    (url TEXT UNIQUE);
''')

# Check to see if we are already in progress...
csr.execute("SELECT id, url FROM Pages WHERE html IS NULL AND error IS NULL ORDER BY RANDOM() LIMIT 1")
_row = csr.fetchone()

# If there is an item to crawl next.
if _row is not None :
    print("Restarting existing crawl. Remove spider.sqlite to start a fresh crawl.")

# if don't have item.
else :
    starturl = input("Enter web url or enter : ")

    if not starturl :
        starturl = "http://www.dr-chuck.com/"

    if starturl.endswith("/") :
        starturl = starturl[:-1]

    web = starturl

    if starturl.endswith(".htm") or starturl.endswith(".html") :
        pos = starturl.rfind("/")
        web = starturl[:pos]

    if len(web) > 1 :
        csr.execute("INSERT OR IGNORE INTO Webs (url) VALUES (:url)", {"url":web})
        csr.execute("INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (:url, NULL, 1.0)", {"url":web})
        conn.commit()

# Get the current Webs
csr.execute("SELECT url FROM Webs")
webs = [row["url"] for row in csr]
# webs = list()
# for row in csr :
#     webs.append(row["url"])

print(webs)

many = 0
while True :
    if many < 1 :
        sval = input("How many pages : ")

        if not sval :
            break
        many = int(sval)

    many -= 1

    # retrieve next crawl item.
    csr.execute("SELECT id, url FROM Pages WHERE html IS NULL AND error IS NULL ORDER BY RANDOM() LIMIT 1")
    try :
        row = csr.fetchone()
        from_id = row["id"]
        url = row["url"]

    except :
        print("No unretrieved HTML pages found")
        many = 0
        break;

    print(from_id, url, end=" ")

    # if we are retrieving this page. there should be no links from it
    csr.execute("DELETE FROM Links WHERE from_id = :from_id", {"from_id":from_id})
    try :
        _response = urllib.request.urlopen(url, context=ctx)

        html = _response.read()
        if _response.getcode() != 200 :
            print("Error on page : ", _response.getcode())
            csr.execute("UPDATE Pages SET error = :error WHERE url = :url", {"error":_response.getcode(), "url":url})

        if _response.info().get_content_type() != "text/html" :
            print("Ignore non text/html page")
            csr.execute("DELETE FROM Pages WHERE url = :url", {"url":url})
            conn.commit()
            continue

        print(len(html), end=" ")

        _soup = BeautifulSoup(html, "html.parser")

    except KeyboardInterrupt :
        print()
        print("Program interrupted by user....")
        break

    except :
        print()
        print("Unable to retrieve or parse page")
        csr.execute("UPDATE Pages SET error = -1 WHERE url = :url", {"url":url})
        conn.commit()
        continue

    csr.execute('''INSERT OR REPLACE INTO Pages (url, html, new_rank)
                VALUES (:url, :html, 1.0)''', {"url":url, "html":memoryview(html)})
    conn.commit()

    # Retrieve all of the anchor tags
    _tags = _soup("a")   # equal _soup.find_all("a")
    count = 0
    for _tag in _tags :
        href = _tag.get("href", None)

        if not href :
            continue

        # Resolve relative references like href="/contact"
        up = urllib.parse.urlparse(href)
        if len(up.scheme) < 1 :
            href = urllib.parse.urljoin(url, href)

        ipos = href.find("#")
        if ipos > 1 :
            href = href[:ipos]

        if href.endswith(".png") or href.endswith(".jpg") or href.endswith(".gif") :
            continue

        if href.endswith("/") :
            href = href[:-1]

        if len(href) < 1 :
            continue

        # Check if the URL is in any of the webs
        found = False
        for web in webs :
            if href.startswith(web) :
                found = True
                break

        if not found :
            continue

        csr.execute("INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (:url, NULL, 1.0)", {"url":href})
        count += 1
        conn.commit()

        csr.execute("SELECT id FROM Pages WHERE url = :url", {"url":href})
        try :
            row = csr.fetchone()
            to_id = row["id"]

        except :
            print("Could not retrieve id")
            continue

        csr.execute("INSERT OR IGNORE INTO Links (from_id, to_id) VALUES (:from_id, :to_id)", {"from_id":from_id, "to_id":to_id})
        conn.commit()

    print(count)

csr.close()
conn.close()
