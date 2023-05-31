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
        user=config.MYSQL_HOST,
        password=config.MYSQL_PASS,
        database=config.MYSQL_DATABASE
    )
    return cnx

# Funcction to close connection
def close_connection(cnx):
    cnx.close()

# Funcion qto check if table exist
def table_exists(cnx, table_name):
    cursor = cnx.cursor()

    query = "SHOW TABLES LIKE %s"
    data = (table_name,)

    cursor.execute(query, data)

    exists = cursor.fetchone() is not None

    cursor.close()

    return exists
    
# Funcion to create table in database
def create_table(cnx, table_name):
    cursor = cnx.cursor()

    create_table_query = """
    CREATE TABLE {} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    date DATE,
    type_event VARCHAR(255),
    recurrency BIT
    )
    """.format(table_name)

    cursor.execute(create_table_query)

    cnx.commit()
    cursor.close()

#Funcion to insert values
def insert_values(cnx, table_name, topic, name, date, type_event, recurrency):

    cursor = cnx.cursor()

    query = "INSERT INTO " + table_name + " (topic, name, date, type_event, recurrency) VALUES (%s, %s, %s, %s, %s)"
    data = (topic, name, date, type_event, recurrency) 
    print("Inserted line")
    cursor.execute(query, data)

    cnx.commit()
    cursor.close()

# Funcion to check if are entry with specific name
def check_topic_exists(cnx, topic_value):
    
    cursor = cnx.cursor()

    query = "SELECT EXISTS (SELECT 1 FROM topics WHERE topic = %s)"
    cursor.execute(query, (topic_value,))

    result = cursor.fetchone()[0]

    cursor.close()

    return bool(result)

# Funcion to update entry in database
def update_data(cnx, table_name, topic, new_name, new_date, new_type_event, new_recurrency):

    cursor = cnx.cursor()
    query = f"SELECT * FROM {table_name} WHERE topic = %s"
    cursor.execute(query, (topic,))
    row = cursor.fetchone()

    if row is not None:
        row_id, topic, name, date, type_event, recurrency = row

        if ((name == new_name) and (str(date) == new_date) and (type_event == new_type_event) and (recurrency == new_recurrency)):
            print("Same data")
            return
        if name != new_name:
            name = new_name
        if date != new_date:
            date = new_date
        if type_event != new_type_event:
            type_event = new_type_event
        if recurrency != new_recurrency:
            recurrency = new_recurrency

        update_query = f"UPDATE {table_name} SET name = %s, date = %s, type_event = %s, recurrency = %s WHERE id = %s"
        cursor.execute(update_query, (name, date, type_event, recurrency, row_id))
        cnx.commit()
        print("Updated!")
    else:
        print("Error")

    cursor.close()

# Callback to manage received messages
def on_message(client, userdata, msg):
    print("RECEIVED (" + msg.topic + ") -- " + msg.payload.decode())
    data = msg.payload.decode().split(", ")
    if check_topic_exists(connection, (data[0].split("/")[1])) == False:
        insert_values(connection, "topics", data[0].split("/")[1], data[1], data[2], data[3], int(data[4]))
    else:
        update_data(connection, "topics", data[0].split("/")[1], data[1], data[2], data[3], int(data[4]))

#### PROGRAM ####
connection = establish_connection()
if not table_exists(connection, "topics"):
    create_table(connection, "topics")

# Create MQTT client instance
cliente = mqtt.Client()

# Asign auth credentials
cliente.username_pw_set(emqx_user, emqx_pass)

# Asign callback for received message
cliente.on_message = on_message

# Connect to EMQX server
cliente.connect(broker, puerto)

# Subsribe
cliente.subscribe("events/+")

# Keep conextion ans precess received messages
cliente.loop_forever()