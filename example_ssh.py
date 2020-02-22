import time
from common_utils.ssh import ssh_client

host = 'localhost'
port = '20'
username = 'caio'
password = 'password'

#Starting SSH Client
ssh = ssh_client(host, username, password, port=22, key=None, passphrase=None)

#adding user
r = ssh.execute('ls /bin',sudo=False)

#Printing out returns
print('out: ')
for x in r['out']:
    print(x)
print('err: ')
for x in r['err']:
    print(x)
print('retval: '+ str(r['retval']))

#Keeps main script from closing
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."

#cleans up connection
ssh.clean_up()
