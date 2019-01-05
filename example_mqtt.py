import time
from common_utils.mqtt import mqtt_connection

#MQTT connection details
client_id = 'python_mqtt_client'
usr = 'user'
passw = 'secure_password_1234'
host = '10.0.0.23'
port = '1883'
topic = 'my_mqtt_topic'

#function to act upon message
def on_message(client, userdata, message):
    print('Got a message at '+topic+', it reads: '+message)

#Start MQTT
mqtt = mqtt_connection(client_id,host,port,usr,passw,topic,on_message)

#Publishing to topic
mqtt.publish_to_topic('Hello from Python!')

#Keeps main script from closing
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."

#cleans up connection
mqtt.clean_up()
