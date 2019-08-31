count = 0;
sum = 0.0;

while True :
    num = input("Enter a number : ")

    if num == "done" :
        break

    try :
        sum += float(num)
        count += 1

    except :
        print("Invalid input")
        continue

print("All Done : ", count, sum,  0 if count == 0 else round(sum/count, 3))
