# SIOT
Sensing and Internet of Things Coursework

Data_collection.py is part 1 of the coursework. 
It is run on a raspberry pi every 5 minutes using crontab scheduling. 
Every time it is run it writes to a google sheet information from a weather API, the nest API, and a temperature sensor. 

The temperature sensor is ds18b20 connected to the raspberry pi pins with a 4.7K Ohm resistor. 
