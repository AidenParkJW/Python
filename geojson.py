import urllib.request, urllib.parse, urllib.error
import json

serviceUrl = "http://maps.googleapis.com/maps/api/geocode/json?"

while True :
    address = input("Enter location : ")

    if len(address) < 1 :
        break;

    url = serviceUrl + urllib.parse.urlencode({"address":address})

    print("Retrieving :", url)
    uh = urllib.request.urlopen(url)
    print(type(uh))
    data = uh.read().decode()
    print("Retrieved", len(data), "characters")

    try :
        js = json.loads(data)

    except Exception as e :
        print("Exception : ", e)
        js = None

    if not js or "status" not in js or js["status"] != "OK" :
        print("===== Failure To Retrieve =====")
        print(data)
        continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    print("lat : {}, lng : {}".format(lat, lng))
    location = js["results"][0]["formatted_address"]
    print("loacation :", location)
    print()
