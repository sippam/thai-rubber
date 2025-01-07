import mysql.connector
import os
import dotenv
from wunderground import get_wether_wunderground
from open_meteo import get_weather

dotenv.load_dotenv()


def connect_database():
    mydb = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        auth_plugin='mysql_native_password'
    )
    mycursor = mydb.cursor()
    return mydb, mycursor  # Return both connection and cursor


def initialize_db(mydb, mycursor):
    mycursor.execute("CREATE DATABASE IF NOT EXISTS thai_rubber")
    mycursor.execute("USE thai_rubber")
    mycursor.execute(
        "CREATE TABLE IF NOT EXISTS customers (id VARCHAR(255) PRIMARY KEY, line_name VARCHAR(255), address VARCHAR(255))")
    mydb.commit()  # Save changes to the database


def register_user(mydb, mycursor, data):
    print("data", data)
    id, line_name, tel, address, address_format, latitude, longitude, area, land_type, soil_type, rubber_type, weather_station, weather_serial = data.values()
    mycursor.execute("USE thai_rubber")
    sql = "INSERT INTO customers (id, line_name, tel) VALUES (%s, %s, %s)"
    value = (id, line_name, tel)
    mycursor.execute(sql, value)

    mycursor.execute("USE thai_rubber")
    sql = "INSERT INTO address (id, address, address_format, latitude, longitude) VALUES (%s, %s, %s, %s, %s)"
    value = (id, address, address_format, latitude, longitude)
    mycursor.execute(sql, value)

    mycursor.execute("USE thai_rubber")
    sql = "INSERT INTO plantation (id, area, land_type, soil_type, rubber_type, weather_station, weather_serial) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    value = (id, area, land_type, soil_type, rubber_type,
             weather_station, weather_serial)
    mycursor.execute(sql, value)

    mydb.commit()

# def change_user_address(mydb, mycursor, data):
#     print("data", data)
#     mycursor.execute("USE thai_rubber")
#     sql = """
#     UPDATE customers
#     SET address = %s, address_format = %s, latitude = %s, longitude = %s
#     WHERE id = %s
#     """
#     value = (data['address'], data['address_format'], data['latitude'], data['longitude'], data['id'])
#     mycursor.execute(sql, value)
#     mydb.commit()


def change_user_address(mydb, mycursor, data):
    print("data", data)
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM address WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE address 
        SET address = %s, address_format = %s, latitude = %s, longitude = %s 
        WHERE id = %s
        """
        value = (data['address'], data['address_format'],
                 data['latitude'], data['longitude'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user address.")
    else:  # ไม่มีข้อมูล -> ทำการ Insert
        sql = """
        INSERT INTO address (id, address, address_format, latitude, longitude) 
        VALUES (%s, %s, %s, %s, %s)
        """
        value = (data['id'], data['address'], data['address_format'],
                 data['latitude'], data['longitude'])
        mycursor.execute(sql, value)
        print("Inserted new user address.")

    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_tel(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM customers WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE customers 
        SET tel = %s
        WHERE id = %s
        """
        value = (data['tel'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user tel.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_area(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET area = %s
        WHERE id = %s
        """
        value = (data['area'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user area.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_land_type(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET land_type = %s
        WHERE id = %s
        """
        value = (data['land_type'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user land_type.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_soil_type(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET soil_type = %s
        WHERE id = %s
        """
        value = (data['soil_type'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user soil_type.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_rubber_type(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET rubber_type = %s
        WHERE id = %s
        """
        value = (data['rubber_type'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user rubber_type.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_weather_station(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET weather_station = %s
        WHERE id = %s
        """
        value = (data['weather_station'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user weather_station.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def change_user_weather_serial(mydb, mycursor, data):
    mycursor.execute("USE thai_rubber")

    # ตรวจสอบว่ามี ID ในฐานข้อมูลหรือไม่
    check_sql = "SELECT COUNT(*) FROM plantation WHERE id = %s"
    mycursor.execute(check_sql, (data['id'],))
    result = mycursor.fetchone()

    if result[0] > 0:  # มีข้อมูลอยู่แล้ว -> ทำการ Update
        sql = """
        UPDATE plantation 
        SET weather_station = %s, weather_serial = %s
        WHERE id = %s
        """
        value = (data['weather_station'], data['weather_serial'], data['id'])
        mycursor.execute(sql, value)
        print("Updated existing user weather_serial.")
    # Commit การเปลี่ยนแปลง
    mydb.commit()


def have_user(mydb, mycursor, id):
    mycursor.execute("USE thai_rubber")
    sql = "SELECT * FROM customers WHERE id = %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()
    if myresult:
        return True
    else:
        return False


def get_lat_long_user(mydb, mycursor, id):
    mycursor.execute("USE thai_rubber")
    sql = "SELECT latitude, longitude FROM address WHERE id = %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()[0]
    return myresult


def get_user_data(mydb, mycursor, id):
    myresult = {}
    mycursor.execute("USE thai_rubber")
    sql = "SELECT tel FROM customers WHERE id = %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult['tel'] = mycursor.fetchall()[0][0]

    sql = "SELECT address FROM address WHERE id = %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult['address'] = mycursor.fetchall()[0][0]

    sql = "SELECT area, land_type, soil_type, rubber_type, weather_station, weather_serial FROM plantation WHERE id = %s"
    value = (id,)
    mycursor.execute(sql, value)
    data = mycursor.fetchall()[0]
    weather_station = data[4]
    if weather_station:
        myresult['area'], myresult['land_type'], myresult['soil_type'], myresult[
            'rubber_type'], myresult['weather_serial'] = data[0], data[1], data[2], data[3], data[5]
    else:
        myresult['area'], myresult['land_type'], myresult['soil_type'], myresult['rubber_type'] = data[0], data[1], data[2], data[3]
        myresult['weather_serial'] = "-"
    return myresult


def hour_add_weather(mydb, mycursor):
    mycursor.execute("USE thai_rubber")
    sql = "SELECT id, weather_station, weather_serial FROM plantation"
    mycursor.execute(sql)
    myresult_array = mycursor.fetchall()

    for data in myresult_array:
        have_weather_station = data[1]
        id = str(data[0])
        if (have_weather_station):
            data = get_wether_wunderground(data[2])

            solarRadiationHigh = data["solarRadiationHigh"]
            uvHigh = data["uvHigh"]
            winddirAvg = data["winddirAvg"]
            humidityHigh = data["humidityHigh"]
            humidityLow = data["humidityLow"]
            humidityAvg = data["humidityAvg"]
            tempHigh = data["imperial"]["tempHigh"]
            tempLow = data["imperial"]["tempLow"]
            tempAvg = data["imperial"]["tempAvg"]
            windspeedHigh = data["imperial"]["windspeedHigh"]
            windspeedLow = data["imperial"]["windspeedLow"]
            windspeedAvg = data["imperial"]["windspeedAvg"]
            windgustHigh = data["imperial"]["windgustHigh"]
            windgustLow = data["imperial"]["windgustLow"]
            windgustAvg = data["imperial"]["windgustAvg"]
            dewptHigh = data["imperial"]["dewptHigh"]
            dewptLow = data["imperial"]["dewptLow"]
            dewptAvg = data["imperial"]["dewptAvg"]
            windchillHigh = data["imperial"]["windchillHigh"]
            windchillLow = data["imperial"]["windchillLow"]
            windchillAvg = data["imperial"]["windchillAvg"]
            heatindexHigh = data["imperial"]["heatindexHigh"]
            heatindexLow = data["imperial"]["heatindexLow"]
            heatindexAvg = data["imperial"]["heatindexAvg"]
            pressureMax = data["imperial"]["pressureMax"]
            pressureMin = data["imperial"]["pressureMin"]
            pressureTrend = data["imperial"]["pressureTrend"]
            precipRate = data["imperial"]["precipRate"]
            precipTotal = data["imperial"]["precipTotal"]

            sql = """
            INSERT INTO hours (
                id, temperature_max, temperature_min, temperature_avg, 
                windspeed_max, windspeed_min, windspeed_avg,
                windgust_max, windgust_min, windgust_avg,
                dewpt_max, dewpt_min, dewpt_avg,
                windchill_max, windchill_min, windchill_avg,
                heatindex_max, heatindex_min, heatindex_avg,
                pressure_max, pressure_min, pressure_trend,
                precipitation_total, precipitation_rate,
                shortwave_radiation, uv, wind_direction,
                humidity_max, humidity_min, humidity_avg,
                soil_moisture
            ) VALUES (
                %(id)s, %(tempHigh)s, %(tempLow)s, %(tempAvg)s, 
                %(windspeedHigh)s, %(windspeedLow)s, %(windspeedAvg)s, 
                %(windgustHigh)s, %(windgustLow)s, %(windgustAvg)s, 
                %(dewptHigh)s, %(dewptLow)s, %(dewptAvg)s, 
                %(windchillHigh)s, %(windchillLow)s, %(windchillAvg)s, 
                %(heatindexHigh)s, %(heatindexLow)s, %(heatindexAvg)s, 
                %(pressureMax)s, %(pressureMin)s, %(pressureTrend)s, 
                %(precipTotal)s, %(precipRate)s, 
                %(solarRadiationHigh)s, %(uvHigh)s, %(winddirAvg)s, 
                %(humidityHigh)s, %(humidityLow)s, %(humidityAvg)s,
                %(soil_moisture)s
            )
            """
            data = {
                "id": id,
                "tempHigh": tempHigh,
                "tempLow": tempLow,
                "tempAvg": tempAvg,
                "windspeedHigh": windspeedHigh,
                "windspeedLow": windspeedLow,
                "windspeedAvg": windspeedAvg,
                "windgustHigh": windgustHigh,
                "windgustLow": windgustLow,
                "windgustAvg": windgustAvg,
                "dewptHigh": dewptHigh,
                "dewptLow": dewptLow,
                "dewptAvg": dewptAvg,
                "windchillHigh": windchillHigh,
                "windchillLow": windchillLow,
                "windchillAvg": windchillAvg,
                "heatindexHigh": heatindexHigh,
                "heatindexLow": heatindexLow,
                "heatindexAvg": heatindexAvg,
                "pressureMax": pressureMax,
                "pressureMin": pressureMin,
                "pressureTrend": pressureTrend,
                "precipTotal": precipTotal,
                "precipRate": precipRate,
                "solarRadiationHigh": solarRadiationHigh,
                "uvHigh": uvHigh,
                "winddirAvg": winddirAvg,
                "humidityHigh": humidityHigh,
                "humidityLow": humidityLow,
                "humidityAvg": humidityAvg,
                "soil_moisture": 0
            }
            mycursor.execute(sql, data)
            mydb.commit()

        else:
            sql = "SELECT latitude, longitude FROM address WHERE id = %s"
            value = (data[0],)
            mycursor.execute(sql, value)
            lat_long = mycursor.fetchall()[0]

            daily_data = get_weather(lat_long[0], lat_long[1])
            temperature_2m_max = daily_data["temperature_2m_max"][0]
            temperature_2m_min = daily_data["temperature_2m_min"][0]
            temperature_2m_avg = daily_data["temperature_2m_avg"][0]
            precipitation_sum = daily_data["precipitation_sum"][0]
            wind_speed_10m_max = daily_data["wind_speed_10m_max"][0]
            wind_direction_10m_dominant = daily_data["wind_direction_10m_dominant"][0]
            wind_gusts_10m_max = daily_data["wind_gusts_10m_max"][0]
            shortwave_radiation_sum = daily_data["shortwave_radiation_sum"][0]
            relative_humidity_2m = daily_data["relative_humidity_2m"][0]
            soil_moisture_9_to_27cm = daily_data["soil_moisture_9_to_27cm"][0]

            temperature_2m_max = round(float(temperature_2m_max), 2)
            temperature_2m_min = round(float(temperature_2m_min), 2)
            temperature_2m_avg = round(float(temperature_2m_avg), 2)
            precipitation_sum = round(float(precipitation_sum), 2)
            wind_speed_10m_max = round(float(wind_speed_10m_max), 2)
            wind_direction_10m_dominant = round(
                float(wind_direction_10m_dominant), 2)
            wind_gusts_10m_max = round(float(wind_gusts_10m_max), 2)
            shortwave_radiation_sum = round(float(shortwave_radiation_sum), 2)
            relative_humidity_2m = round(float(relative_humidity_2m), 2)
            soil_moisture_9_to_27cm = round(float(soil_moisture_9_to_27cm), 2)

            sql = """
            INSERT INTO hours (
                id, temperature_max, temperature_min, temperature_avg, 
                windspeed_max, windspeed_min, windspeed_avg,
                windgust_max, windgust_min, windgust_avg,
                dewpt_max, dewpt_min, dewpt_avg,
                windchill_max, windchill_min, windchill_avg,
                heatindex_max, heatindex_min, heatindex_avg,
                pressure_max, pressure_min, pressure_trend,
                precipitation_total, precipitation_rate,
                shortwave_radiation, uv, wind_direction,
                humidity_max, humidity_min, humidity_avg,
                soil_moisture
            ) VALUES (
                %(id)s, %(temperature_2m_max)s, %(temperature_2m_min)s, %(temperature_2m_avg)s, 
                %(wind_speed_10m_max)s, 0, 0, -- windspeed_min, windspeed_avg
                %(wind_gusts_10m_max)s, 0, 0, -- windgust_min, windgust_avg
                0, 0, 0, -- dewpt_max, dewpt_min, dewpt_avg
                0, 0, 0, -- windchill_max, windchill_min, windchill_avg
                0, 0, 0, -- heatindex_max, heatindex_min, heatindex_avg
                0, 0, 0, -- pressure_max, pressure_min, pressure_trend
                %(precipitation_sum)s, 0, -- precipitation_rate
                %(shortwave_radiation_sum)s, 0, -- uv
                %(wind_direction_10m_dominant)s,
                0, 0, %(relative_humidity_2m)s, -- humidity_max, humidity_min, humidity_avg
                %(soil_moisture_9_to_27cm)s
            )
            """

            data = {
                "id": id,
                "temperature_2m_max": temperature_2m_max,
                "temperature_2m_min": temperature_2m_min,
                "temperature_2m_avg": temperature_2m_avg,
                "wind_speed_10m_max": wind_speed_10m_max,
                "wind_gusts_10m_max": wind_gusts_10m_max,
                "precipitation_sum": precipitation_sum,
                "shortwave_radiation_sum": shortwave_radiation_sum,
                "wind_direction_10m_dominant": wind_direction_10m_dominant,
                "relative_humidity_2m": relative_humidity_2m,
                "soil_moisture_9_to_27cm": soil_moisture_9_to_27cm
            }
            mycursor.execute(sql, data)
            mydb.commit()
    print("Inserted new hour weather data.")


def send_noti_first_time(mydb, mycursor, data):
    id = data["id"]
    disease = data["disease"]["name"]

    mycursor.execute("USE thai_rubber")
    sql = "SELECT COUNT(*) FROM uploads WHERE id = %s AND disease LIKE %s"
    value = (id, disease)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchall()[0][0]

    if myresult == 1:
        transaction_id = data["transaction_id"]
        disease_level = data["disease_level"]
        risk = data["risk"]
        sql = "INSERT INTO notifications (transaction_id, id, disease, disease_level, risk, create_at) VALUES (%s, %s, %s, %s, %s, NOW())"
        value = (transaction_id, id, disease, disease_level, risk)
        mycursor.execute(sql, value)
        print("Inserted new notification.")
