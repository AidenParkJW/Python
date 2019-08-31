def computepay(hours, rate) :
    try :
        xh = float(hours)
        xr = float(rate)

        if xh > 40 :
            xp = xh * xr
            xe = (xh - 40) * (xr * 0.5)
            xp = xp + xe
        else :
            xp = xh * xr

    except Exception as ex :
        print("wrong value. try again!", ex)
        quit() # exit()

    return xp;

xh = input("Enter Hours: ")
xr = input("Enter Rate: ")

print("pay", computepay(xh, xr))
