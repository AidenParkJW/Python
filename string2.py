counts = dict()
_str = open("test.txt", encoding="utf-8")
words = _str.read().split()

for word in words :
    counts[word] = counts.get(word, 0) + 1

bigWord = {"word":None, "count":None}

for k, v in counts.items() :
    if bigWord["word"] is None or bigWord["count"] < v :
        bigWord["word"] = k
        bigWord["count"] = v

print("The Most common words : ", bigWord)




# 많이 사용한 단어를 우선으로 - 전체 출력 
# lambda 이용
rank = sorted(counts.items(), key=lambda item:item[1], reverse=True)
for i in rank :
    print("{:>20} : {:5}".format(i[0], i[1]))
       
print()
print("-" * 70)
print()

# 많이 사용한 단어를 우선으로 - 상위 10개 출력
# lambda 이용
rank = sorted(counts.items(), key=lambda item:item[1], reverse=True)
for k, v in rank[0:10] :
    print("{:>20} : {:5}".format(k, v))


print()
print("-" * 70)
print()

# 많이 사용한 단어를 우선으로 - 상위 10개 출력
# List comprehension 이용
rank = sorted([(v, k) for k, v in counts.items()], reverse=True)    # sorted함수를 이용하면 tuple의 왼쪽 첫번째항목을 키로 정렬한다. 그래서 key와 value의 위치변경
for v, k in rank[0:10] :                                            # 다시 출력을 위해서 key와 value의 위치변경
	print("{:>20} : {:05}".format(k, v))







