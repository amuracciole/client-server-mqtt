import paho.mqtt.client as mqtt
import config

# EMQX configuration
broker = config.EMQX_BROKER
port = config.EMQX_PORT
user = config.EMXQ_USER
password = config.EMQX_PASSWORD

# Global variable to save conection status
connected = False

# Callback for mange conection to EMQX server
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        connected = True
    else:
        print("Connection error:", rc)

# Create client MQTT instance
client = mqtt.Client()

# Asign auth credentials
client.username_pw_set(user, password)

# Asigna callback for conection
client.on_connect = on_connect

# Connect to EMQX server
client.connect(broker, port)

# Wait until connection established
client.loop_start()

while not connected:
    pass

# Message
msg="events/topic2, Andres, 1993-02-15, Birthday, 0"

data = msg.split(", ")

client.publish(data[0], msg, retain=False)
print("SENT (" + data[0] + ") -- ", msg)

# EMQX disconnect
client.disconnect()

# DStop client MQTT loop
client.loop_stop()

