def getStr(start, end, strVal):
    val = ''
    
    while start < end:
        val += strVal[start % len(strVal)]
        start += 1

    return val


n = int(input('Enter number of lines: '))
string = 'FORMULAQSOLUTIONS'
space = int(n / 2)

triangle = 1
iter = 0
height = int(n / 2) + 1

for i in range(0, height):
    for j in range(0, space):
        print(' ', end="")
    val = getStr(iter, triangle, string)
    print(val, end="")
    print()
    iter += 1
    triangle += 3
    space -= 1

# Printing the lower half of the diamond
triangle -= 4  # Adjust the starting point for the lower half
space += 2  # Adjust the spacing for the lower half


for i in range(height, n+1):
    for j in range(0, space):
        print(' ', end="")
    val = getStr(iter, triangle, string)
    print(val, end="")
    print()
    iter += 1
    triangle -= 1
    space += 1
