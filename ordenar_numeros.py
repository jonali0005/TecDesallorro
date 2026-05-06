a = 5
b = 3
c = 1

if a > b:
    if b > c:
        print(c, b, a)
    else:
        if c > a:
            print(b, a, c)
        else:
            print(b, c, a)
else:
    if a > c:
        print(c, a, b)
    else:
        if c > b:
            print(a, b, c)
        else:
            print(a, c, b)