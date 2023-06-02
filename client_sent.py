import paho.mqtt.client as mqtt
import config
import time
import os

# EMQX configuration
broker = config.EMQX_BROKER
port = config.EMQX_PORT
emqx_user = config.EMXQ_USER
emqx_pass = config.EMQX_PASSWORD

# Función para establecer la conexión con el broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT")
    # Suscribirse a los tópicos deseados al establecer la conexión
    #client.subscribe("events/topic1")
    #client.subscribe("events/topic2")

# Función para procesar los mensajes recibidos
def on_message(client, userdata, msg):
    print("Mensaje recibido: Topic: {}, Mensaje: {}".format(msg.topic, msg.payload.decode()))
    #time.sleep(3)
    #os.system("clear")

# Crear instancia del cliente MQTT
client = mqtt.Client()

# Asignar funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Establecer credenciales de autenticación
client.username_pw_set(emqx_user, emqx_pass)

# Conectar al broker MQTT
client.connect(broker, port, 60)

# Iniciar el bucle de la aplicación MQTT
client.loop_start()

# Menú de opciones
while True:
    print("\nSelecciona una opción:")
    print("1. Publicar mensaje")
    print("2. Suscribirse a un tópico")
    print("3. Salir")

    opcion = input("Opción: ")

    if opcion == "1":
        topic = input("Name of the event (do not include events/): ")
        topic = "events/" + topic
        name = input("Name: ")
        date = input("Date (YYYY-MM-DD): ")
        event_type = input("1 - Birthday\n2 - Other\n")
        if event_type == "1":
            event_type = "Birthday"
        elif event_type == "2":
            event_type = "Event"
        recurring = input("1 - YES\n2 - NO\n")
        msg = topic + ", " + name + ", " + date + ", " + event_type + ", " + recurring
        client.publish(topic, msg, retain=False)
        print("Mensaje enviado")
    elif opcion == "2":
        topic = input("Indicate the name of the topic you want to subscribe to: ")
        topic = "events/" + topic
        client.subscribe(topic)
        print("Suscrito al tópico {}".format(topic))
    elif opcion == "3":
        break
    else:
        print("Opción inválida. Intente nuevamente.")

# Desconectar del broker MQTT
client.loop_stop()
client.disconnect()
print("Desconectado del broker MQTT")
