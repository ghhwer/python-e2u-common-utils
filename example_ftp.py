import time
from common_utils.ftp import ftp_server

#Starting FTP (ftp://localhost:2121)
f_srv = ftp_server(ip='localhost',port=2121,anonymous_can_write=False)

#adding user
f_srv.add_user('username','password','/home/username',give_write_permition=True)

#Keeps main script from closing
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."

#cleans up server
f_srv.clean_up()
