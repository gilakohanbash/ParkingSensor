import paho.mqtt.client as mqtt
import time



def on_message(mqtt_client, userdata, message):
        print("Custom Callback " + message.payload.decode())

def on_message_from_sensor(mqtt_client,userdata,message):
        print(message.payload.decode())

def on_connect(mqtt_client, userdata,flags,rc):
        mqtt_client.subscribe("parking/sensor")
        mqtt_client.message_callback_add("parking/sensor",on_message_from_sensor)


if __name__ == '__main__':
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.on_connect = on_connect
        mqtt_client.connect("172.20.10.4",1883,60)
        mqtt_client.loop_forever()


