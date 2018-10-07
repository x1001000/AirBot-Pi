from requests import get
from datetime import datetime
from time import time


def upload(data):
    '''
    pock the RESTful API of LASS
    :param data: dict
    :return: requests.Response
    '''

    data.update(zip(("date", "time", "tick"), datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S").split() + [time()]))
    payload = ''.join(f"|{key}={value}"for key, value in data.items())

    return get("https://pm25.lass-net.org/api/v1/upload/{app}/{device_id}/{payload}".format(payload=payload, **data))


if __name__ == '__main__':

    latitude, longitude, temperature, humidity, PM1_0, PM2_5, PM10 = 25.045582, 121.531032, 1001000, 1001000, 1001000, 1001000, 1001000
    data = dict(app = "AirBot-Pi",
                device_id = "1001000",
                device = "1001000",
                ver_format = "3",
                fmt_opt = "0",
                FAKE_GPS = "1",
                gps_fix = "1",
                gps_num = "100",
                gps_lat = latitude,
                gps_lon = longitude,
                s_t0 = temperature,
                s_h0 = humidity,
                s_d2 = PM1_0,
                s_d0 = PM2_5,
                s_d1 = PM10)

    from time import sleep

    while True:
        upload(data)
        print("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "]" + " upload done!")
        sleep(60)