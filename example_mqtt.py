import time
from common_utils.mqtt import mqtt_connection

#MQTT connection details
client_id = ''
usr = 'test'
passw = 'test'
host = 'localhost'
port = '1883'
topic = 'test'

#function to act upon message
def on_message(client, userdata, message):
    print('Got a message at '+topic+', it reads: '+message.payload)

#Start MQTT
mqtt = mqtt_connection(client_id,host,port,usr,passw,topic,on_message)

#Publishing to topic
mqtt.publish_to_topic('Hello from Python!')

#Keeps main script from closing
try:
    while True:
    	time.sleep(0.1)
        imp = str(raw_input("mqtt > "))
        mqtt.publish_to_topic(imp)
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."

#cleans up connection
mqtt.clean_up()
