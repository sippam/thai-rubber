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
        if (have_weather_station):
            get_wether_wunderground(data[2])
        else:
            sql = "SELECT latitude, longitude FROM address WHERE id = %s"
            value = (data[0],)
            mycursor.execute(sql, value)
            lat_long = mycursor.fetchall()[0]
            
            daily_data = get_weather(lat_long[0], lat_long[1])
            temperature_2m_avg = daily_data["temperature_2m_avg"][0]
            precipitation_sum = daily_data["precipitation_sum"][0]
            precipitation_hours = daily_data["precipitation_hours"][0]
            wind_speed_10m_max = daily_data["wind_speed_10m_max"][0]
            wind_direction_10m_dominant = daily_data["wind_direction_10m_dominant"][0]
            uv_index_max = daily_data["uv_index_max"][0]
            shortwave_radiation_sum = daily_data["shortwave_radiation_sum"][0]

            temperature_2m_avg = round(float(temperature_2m_avg), 2)
            precipitation_sum = round(float(precipitation_sum), 2)
            precipitation_hours = round(float(precipitation_hours), 2)
            wind_speed_10m_max = round(float(wind_speed_10m_max), 2)
            wind_direction_10m_dominant = round(
                float(wind_direction_10m_dominant), 2)
            uv_index_max = round(float(uv_index_max), 2)
            shortwave_radiation_sum = round(float(shortwave_radiation_sum), 2)
            
            print("temperature_2m_avg", temperature_2m_avg)
            print("precipitation_sum", precipitation_sum)
            print("precipitation_hours", precipitation_hours)
            print("wind_speed_10m_max", wind_speed_10m_max)
            print("wind_direction_10m_dominant", wind_direction_10m_dominant)
            print("uv_index_max", uv_index_max)
            print("shortwave_radiation_sum", shortwave_radiation_sum)