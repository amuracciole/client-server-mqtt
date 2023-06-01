import paho.mqtt.client as mqtt
import mysql.connector
import config

#Set variables
broker = config.EMQX_BROKER
puerto = config.EMQX_PORT
emqx_user = config.EMXQ_USER
emqx_pass = config.EMQX_PASSWORD

# Funtion to stablish connection to database
def establish_connection():
    cnx = mysql.connector.connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASS,
        database=config.MYSQL_DATABASE
    )
    return cnx

# Funcction to close connection
def close_connection(cnx):
    cnx.close()

# Function to read data base
def read_table(cnx, table_name):

    cursor = cnx.cursor()

    read_table_query = f"SELECT * FROM {table_name}"
    cursor.execute(read_table_query)
    rows = cursor.fetchall()

    #return rows
    formatted_rows = []
    for row in rows:
        formatted_row = f"events/{row[1]}, {row[2]}, {row[3].strftime('%Y-%m-%d')}, {row[4]}, {row[5]}"
        formatted_rows.append(formatted_row)

    return formatted_rows

# Function to create "static topics" like public holidays
def create_static_topics(connection, table_name, client):    
    table = read_table(connection, table_name)
    for row in table:
        msg=row
        topic="events/"+table_name
        client.publish(topic, msg, retain=False)
        print("SENT (" + topic + ") -- ", msg)
    

#### PROGRAM ####
connection = establish_connection()

# Create MQTT client instance
client = mqtt.Client()

# Asign auth credentials
client.username_pw_set(emqx_user, emqx_pass)

# Connect to EMQX server
client.connect(broker, puerto)

#Create statics topics
create_static_topics(connection, "holidays_uruguay", client)

# EMQX disconnect
client.disconnect()

# DStop client MQTT loop
client.loop_stop()

#SE ENVIAN TODOS LOS EVENTOS PERO SOLO SE RECIVE EL PRIMERO EN EL SERVER!