import time
from common_utils.os_interface import linux_process

proc = linux_process('python simple_script.py')
proc.execute()
print(proc.get_pid())

#Keeps the program from exiting unless keyboard interrupted or error has occured on process
try:
    while True:
        time.sleep(0.5)
        if proc.isAvailable_err() == True:
            print('An error has ocurred while running process:\n')
            while proc.isAvailable_err():
                print(proc.read_next_err())
            print('\nExiting Now!')
            break
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."


#kills running applications
proc.kill_proc()
