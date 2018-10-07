import Adafruit_DHT as dht
def t_h():
    return dht.read_retry(dht.DHT22, 4)

if __name__ == '__main__':
    t, h = t_h()
    print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, h))
