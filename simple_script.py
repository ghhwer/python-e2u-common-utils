import time

x = 0
while x <= 10:
    print x
    x+=1
    time.sleep(0.5)

print('I will trow an error now, lets see if you can catch it!')
i = 12
print('err '+i)
