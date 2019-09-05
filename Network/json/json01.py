import json

data = '''{"name":"Chuck", "phone":{"type":"tntl", "number":"+1 734 303 4456"}, "email" : {"hide":"yes"}}'''

info = json.loads(data)
print(type(info))
print("Name :", info["name"])
print("Hide :", info["email"]["hide"])
print()


data = '''[{"id":"001", "x":"2", "name":"Chuck"}, {"id":"009", "x":"7", "name":"Chuck"}]'''

info = json.loads(data)
print(type(info))
print("Length :", len(info))

for item in info :
    print("Name :", item["name"])
    print("id :", item["id"])
    print("X :", item["x"])
    print()
