import grovepi
import atexit
atexit.register(grovepi.dust_sensor_dis)
grovepi.dust_sensor_en()

import Adafruit_DHT as dht
humidity, temperature = dht.read_retry(dht.DHT22, 4)

if __name__ == '__main__':
    try:
        new_val, lowpulseoccupancy = grovepi.dustSensorRead()
        print('PM2.5=', lowpulseoccupancy)
    except:
        print('PPD42 ERROR')
    
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))