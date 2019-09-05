import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

_url = input("Enter url : ")

try :
    _response = urllib.request.urlopen(_url)
    _html = _response.read()
    _soup = BeautifulSoup(_html, "html.parser")

    # Retrieve all of the anchor tags
    _tags = _soup("img")
    for _tag in _tags :
        print(_tag.get("src", None))

except Exception as e :
    print("Exception :", e)
    #quit()
