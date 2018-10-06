import grovepi
new_val, lowpulseoccupancy = grovepi.dustSensorRead()

import Adafruit_DHT as dht
humidity, temperature = dht.read_retry(dht.DHT22, 4)

if __name__ == '__main__':
    print('PM2.5=', lowpulseoccupancy)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))