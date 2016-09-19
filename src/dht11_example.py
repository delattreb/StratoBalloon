from lib import com_dht11
import time
import datetime


instance = com_dht11.DHT11(pin=25)

while True:
    result = instance.read()
    if result != None:
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)

        time.sleep(1)

