import urllib.request, urllib.parse, urllib.error

_response = urllib.request.urlopen("http://data.pr4e.org/romeo.txt")

print(type(_response))
# print header info.
for k, v in _response.getheaders() :
    print("{:>20} : {}".format(k, v))

print()

# 많이 사용하는 단어 출력하기 - 상위 10개 출력
counts = {}
for line in _response :
    print(line.decode().rstrip())

    for word in line.decode().rstrip().split() :
        counts[word] = counts.get(word, 0) + 1

print()

for k, v in sorted(counts.items(), key=lambda item:item[1], reverse=True)[0:10] :
    print("{:10} : {:>5}".format(k, v))
