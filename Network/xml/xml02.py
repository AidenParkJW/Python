import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET

_url = input("Enter XML URL : ")

if not _url :
    _url = "http://py4e-data.dr-chuck.net/comments_207835.xml"

_response = urllib.request.urlopen(_url)
#print(_response.read().decode())
_data = _response.read().decode() # _response.read() The bytes type is also allowed.
print(_data)

_xml = ET.fromstring(_data)
# print(type(_xml))   # <class 'xml.etree.ElementTree.ElementTree'>
print(_xml.find("note").text)

_comments = _xml.findall("comments/comment")
print("Comment count :", len(_comments))
print()

print("{:20} {:10}".format("name", "count"))
print("-" * 20, "-" * 10)
for _comment in _comments :
    #print("name :", _comment.find("name").text)
    #print("count :", _comment.find("count").text)
    #print()
    print("{:20} {:10}".format(_comment.find("name").text, _comment.find("count").text))
