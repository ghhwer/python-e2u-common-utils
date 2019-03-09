import time
from common_utils.mqtt import mqtt_connection

#MQTT connection details
client_id = ''
usr = 'MY_USER'
passw = "MY_PASS"
host = 'my.mqttserver.me'
port = 8883 #Secure
#port = 1883 #Non Secure
topic = 'test'

#function to act upon message
def on_message(client, userdata, message):
	print('Got a message at '+topic+', it reads: '+str(message.payload))

#Start MQTT
#TLS MQTT
mqtt = mqtt_connection(client_id,host,port,usr,passw,topic,on_message,cert="my_certificate_if_any.pem")
#NON TLS MQTT
#mqtt = mqtt_connection(client_id,host,port,usr,passw,topic,on_message,cert=None)

#Publishing to topic
mqtt.publish_to_topic('Hello from Python!')

#Keeps main script from closing
try:
    while True:
        time.sleep(0.1)
        imp = str(input("mqtt > "))
        mqtt.publish_to_topic(imp)
except KeyboardInterrupt:
    print ('')
    print ("Stopping Services...")

#cleans up connection
mqtt.clean_up()
