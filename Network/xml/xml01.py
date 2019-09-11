import xml.etree.ElementTree as ET

data = '''
<person>
    <name>Chunk</name>
    <pone type="intl">+1 734 303 4456</pone>
    <email hide="yes"/>
</person>
'''

print(data)
tree = ET.fromstring(data)
print(type(tree))   # <class 'xml.etree.ElementTree.Element'>
print("Name :", tree.find("name").text)
print("Attr :", tree.find("email").get("hide"))
print()

data = '''
<stuff>
    <users>
        <user x="2">
            <id>001</id>
            <name>Chuck</name>
        </user>
        <user x="7">
            <id>009</id>
            <name>Brent</name>
        </user>
    </users>
</stuff>
'''

print(data)
tree = ET.fromstring(data)
print(type(tree))   # <class 'xml.etree.ElementTree.Element'>
_users = tree.findall("users/user")
print("User count :", len(_users))
print(type(_users)) # <class 'list'>
print()

for _user in _users :
    print(type(_user))  # <class 'xml.etree.ElementTree.Element'>
    print("Name :", _user.find("name").text)
    print("Id :", _user.find("id").text)
    print("Attribute X :", _user.get("x"))
    print()
