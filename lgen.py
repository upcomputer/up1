# coding: utf-8

delimeters = [60,100,120, 240]

offsets = [1,2,4]

if len(offsets) + 1 != len(delimeters):
    print("bad param len. \nexit...")
    exit()

seg_n = len(delimeters) - 1

k = 0

for i in range(0, seg_n):
    for j in range(delimeters[i], delimeters[i+1], offsets[i]):
        k = k+1
        if k % 10 == 0:
            comma = ',\n'
        else:
            comma = ', '
        print(j, end=comma)


print("totaly {} lines".format(k))
