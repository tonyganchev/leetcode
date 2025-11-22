import enchant
d = enchant.Dict("en_US")

wi = [0 for i in range(5)]
could_inc = True
while could_inc:
    for i in range(5):
        if wi[i] == 25:
            if i == 4:
                could_inc = False
                break
            else:
                wi[i] = 0
        else:
            wi[i] += 1
            could_inc = True
            break
    w = ''
    s = ''
    for i in range(5):
        c = chr(ord('a') + wi[i])
        w += c
        s += "\t" + c
    if d.check(w):
        print(s)