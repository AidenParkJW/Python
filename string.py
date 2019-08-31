import inspect
print(inspect.getfile(inspect.currentframe()))

_str = "Banana"
i = 0;

while i < len(_str) :
    print(i, _str[i])
    i += 1


for c in _str :
    print(c)


words = "Connect Foundation"

if "F" in words :
    words.lower()
    words[7] = "&"
else :
    print(words)

print(words)
