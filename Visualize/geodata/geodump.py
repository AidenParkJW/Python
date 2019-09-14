import sqlite3, json, codecs

# If no database exists, a new database is created.
conn = sqlite3.connect("geodata.sqlite")
# if specified like this one, returns dictionary cursor, otherwise underly returns a tuple of tuples
conn.row_factory = sqlite3.Row
csr = conn.cursor()

csr.execute("SELECT * FROM Locations")
fh = codecs.open("where.js", "w", "utf-8")
fh.write("myData = [\n")
_addressList = list()

# The script below has the same meaning.
# _rows = csr.fetchall()
# for row in _rows :
#     print(row)

for i, row in enumerate(csr) :
    data = row["geodata"].decode()

    try :
        js = json.loads(data)

    except Exception as e :
        print("Exception : ", e)
        continue

    # honestly, below script doesn't need, because validated location data is already saved.
    if not("status" in js and js["status"] == "OK") :
        print("skip!", row["address"])
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 :
        print("skip!", row["address"])
        continue

    address = js["results"][0]["formatted_address"]
    address = address.replace("'", "")

    try :
        print("no : {}, lat : {}, lng : {}\naddress : {}\n".format(i, lat, lng, address))
        _addressList.append("[{}, {}, '{}']".format(lat, lng, address))

    except Exception as e :
        print("Exception : ", e)
        continue

fh.write(",\n".join(_addressList))
fh.write("\n];\n")
fh.close()

csr.close()
conn.close()

print(len(_addressList), "records written to where.js")
print("Open where.html to view the data in a browser")
