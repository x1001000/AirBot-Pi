from sensors import DHT22, PPD42NS
from upload_data import upload
from datetime import datetime
from time import sleep

latitude, longitude, temperature, humidity, PM1_0, PM2_5, PM10 = '25.045582', '121.531032', '', '', '', '', ''

data = dict(app="AirBot-Pi",
            device_id="1001000",
            device="AirBot Pi",
            ver_format="3",
            fmt_opt="0",
            FAKE_GPS="1",
            gps_fix="1",
            gps_num="100",
            gps_lat=latitude,
            gps_lon=longitude,
            s_t0=temperature,
            s_h0=humidity,
            s_d2=PM1_0,
            s_d0=PM2_5,
            s_d1=PM10)





while True:
    data['s_h0'], data['s_t0'] = DHT22.t_h()
    data['s_d0'] = PPD42NS.pm25()

    upload(data)
    print("[" + datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "]" + " upload done!")
    print(data)
    sleep(60)