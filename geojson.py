import urllib.request, urllib.parse, urllib.error
import json

serviceUrl = "https://maps.googleapis.com/maps/api/geocode/json?"

while True :
    address = input("Enter location : ")

    if len(address) < 1 :
        break;

    url = serviceUrl + urllib.parse.urlencode({"address":address, "key":"AIzaSyA8IymBhchDz7YbY54gbJYEQuJYVRf7i08"})

    print("Retrieving :", url)
    _response = urllib.request.urlopen(url)
    #print(type(_response))

    # print header info.
    for k, v in _response.getheaders() :
        print("{:>20} : {}".format(k, v))

    print()

    _data = _response.read().decode()  # _response.read() 해도 json.loads(_data) 된다.
    #print(type(_data)) # <class 'str'>
    print("Retrieved", len(_data), "characters")
    print("Retrieved json :")
    print(data)
    print()

    try :
        # loads converts JSON -> Python object
        js = json.loads(_data)  # unicode str, utf-8 bytes 모두 된다.
        #print(type(js)) # <class 'dict'>
        print("json :")
        print(js)
        print()

    except Exception as e :
        print("Exception : ", e)
        js = None

    if not js or "status" not in js or js["status"] != "OK" :
        print("===== Failure To Retrieve =====")
        print(data)
        continue

    # dumps converts Python object -> JSON String
    print(json.dumps(js, indent=4))

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    print("lat : {}, lng : {}".format(lat, lng))
    location = js["results"][0]["formatted_address"]
    print("loacation :", location)
    print()
