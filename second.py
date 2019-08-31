count = 0;
sum = 0;
largest_so_far = -1
smallest = None
print("Before : ", largest_so_far, count, sum)

for num in [9, 41, 12, 3, 74, 15] :
    count += 1
    sum += num

    if smallest is None :
        smallest = num
    elif num < smallest :
        smallest = num

    if num > largest_so_far :
        largest_so_far = num
    print(count, sum, num)

print("After : ", largest_so_far, smallest, count, sum, round(sum/count, 3))
