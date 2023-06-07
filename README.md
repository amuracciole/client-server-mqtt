# RemindMe APP (MQTT)
Program that allows customers to subscribe to topics to receive calendar notifications.
1- Execute server.py on the server side where EMQX is located.
2- Execute client_sent.py on the client side.

![Diagram](https://github.com/amuracciole/remindme_app/blob/main/Diagram.png)

## server.py
It runs on the server where EMQX is located. It is in charge of listening for incoming packets and updating the database. When a message arrives, if it contains the same data of the database, then it does not execute any action. If the data has a non-existent topic, then it saves it in the database as a new one. If the data comes from an existing topic but is different from the last one saved in the database, then it updates the database.

## client_sent.py
It has an interactive menu that allows you to post a message by pre-selecting a topic, subscribe to a particular topic and/or view the topics to which you are currently subscribed.
At the same time, in parallel, it is always listening if a message arrives for one of the topics to which the client is subscribed.

## update_send.py
In case the EMQX server goes down for any reason, this script allows to create default topics important for the application and obtains the information from tables previously created in the database. As an example, tables were created with the dates of public holidays in Spain, Uruguay and dates of the catholic calendar.

## docker-compose
Contains the necessary configuration to raise the EMQX, MYSQL and ADMINER containers to manage the database tables in an interactive way.

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/amuracciole)

**Note: Please take into account that this repository is still in progress of improvements**
