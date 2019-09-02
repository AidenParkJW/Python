import re

fileName = input("Enter file name : ")

if len(fileName) == 0 :
    fileName = "mbox-short.txt"

try :
    fh = open(fileName)
except :
    print("Invalid file")
    # quit()

for _line in fh :
    _line = _line.rstrip()

    # if _line.find("From:") >= 0 :
    if _line.startswith("From:") :
        print(_line)

print()
print("-" * 80)
print()

fh.seek(0)
for _line in fh :
    _line = _line.rstrip()

    # if re.search("From:", _line) :
    if re.search("^From:", _line) :
        print(_line)


print()
print("-" * 80)
print()

fh.seek(0)
idx = 0
for _line in fh :
    _line = _line.rstrip()

    # if re.search("X.*:", _line) :
    if re.search("X-\S+:", _line) :
        idx += 1
        print("{} : {}".format(idx, _line))


print()
print("-" * 80)
print()

fh.seek(0)
idx = 0
for _line in fh :
    _line = _line.rstrip()

    if re.search("^From (\S+@\S+)", _line) :
        idx += 1

        # re.findall() return List -> [''] or [('', '')]

        # 1 : ['stephen.marquard@uct.ac.za'] : ['uct.ac.za']
        print("{:5} : {} : {}".format(idx, re.findall("^From (\S+@\S+)", _line), re.findall("^From \S+@(\S+)", _line)))
        print("{:5} : {[0]:50} : {[0]:20}".format(idx, re.findall("^From (\S+@\S+)", _line), re.findall("^From \S+@(\S+)", _line)))


        # 여러개가 match된다면 groups으로 return한 groups은 tuple 형식이다. -> [('stephen.marquard', 'uct.ac.za')]
        # 1 : stephen.marquard@uct.ac.za                         : stephen.marquard     : uct.ac.za           
        print("{:5} : {} : {}".format(idx, re.findall("^From (\S+@\S+)", _line), re.findall("^From (\S+)@(\S+)", _line)))
        print("{0:5} : {1[0]:50} : {2[0][0]:20} : {2[0][1]:20}".format(idx, re.findall("^From (\S+@\S+)", _line), re.findall("^From (\S+)@(\S+)", _line)))
        print()