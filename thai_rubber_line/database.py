import mysql.connector
import os
import dotenv

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
    value = (id, area, land_type, soil_type, rubber_type, weather_station, weather_serial)
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
