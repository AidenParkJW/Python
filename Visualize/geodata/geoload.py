import urllib.request, urllib.parse, urllib.error
import json, ssl
import sqlite3
import time

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

serviceUrl = "https://maps.googleapis.com/maps/api/geocode/json?"

# If no database exists, a new database is created.
conn = sqlite3.connect("geodata.sqlite")
# if specified like this one, returns dictionary cursor, otherwise underly returns a tuple of tuples.
conn.row_factory = sqlite3.Row
csr = conn.cursor()

csr.execute("CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)")

fh = open("where.data")
count = 0
for line in fh :
    if count > 200 :
        print("Retrieved 200 locations, restart to retrieve more")
        break

    address = line.strip()
    print("")
    csr.execute("SELECT geodata FROM Locations WHERE address = :address", {"address":memoryview(address.encode())})

    try :
        _data = csr.fetchone()["geodata"]
        print("Found in database ", address)
        continue

    except :
        pass

    _parms = dict()
    _parms["address"] = address
    _parms["key"] = "AIzaSyA8IymBhchDz7YbY54gbJYEQuJYVRf7i08"
    url = serviceUrl + urllib.parse.urlencode(_parms)

    count += 1
    print(count, "Retrieving", url)
    _response = urllib.request.urlopen(url, context=ctx)
    _data = _response.read().decode()
    print("Retrived", len(_data), "characters", _data[:20].replace("\n", " "))

    try :
        js = json.loads(_data)

    except Exception as e :
        print("Exception : ", e)
        continue

    if not js or "status" not in js or js["status"] != "OK" or js["status"] == "ZERO_RESULTS" :
        print("===== Failure To Retrieve =====")
        print(_data)
        continue

    csr.execute("INSERT INTO Locations (address, geodata) VALUES (:address, :geodata)", {"address":memoryview(address.encode()), "geodata":memoryview(_data.encode())})
    conn.commit()

    if count % 10 == 0 :
        print("Pausing for a bit...")
        time.sleep(5)

csr.close()
conn.close()

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
