y = input('Enter a number to check: ' )
def pal(num):
    x = num[::-1]
    if x == num:
        print('It is palindrom number')
    else:
        print('NOt palindrom')
print(pal(str(y)))