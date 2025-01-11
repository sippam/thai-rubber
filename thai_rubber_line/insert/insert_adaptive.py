import csv
import mysql.connector
import dotenv
import os
from datetime import datetime
dotenv.load_dotenv()
# เชื่อมต่อกับฐานข้อมูล
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    auth_plugin='mysql_native_password'
)
mycursor = mydb.cursor()
mycursor.execute("USE thai_rubber")

def powder_for_adaptive():
    # อ่าน CSV และเพิ่มค่า disease
    with open("powder_for_adaptive_table.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # เพิ่มค่า disease
            row["disease"] = "powder"

            # เตรียมคำสั่ง SQL สำหรับ INSERT
            sql = """
            INSERT INTO adaptive (
                disease, sevirity, true_label_7_day, predicted_label_7_day, accuracy_7_day,
                true_label_14_day, predicted_label_14_day, accuracy_14_day,
                true_label_outbreak, predicted_label_outbreak, accuracy_outbreak
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                row["disease"], row["sevirity"], row["true_label_7_day"], row["predicted_label_7_day"],
                row["accuracy_7_day"], row["true_label_14_day"], row["predicted_label_14_day"],
                row["accuracy_14_day"], row["true_label_outbreak"], row["predicted_label_outbreak"],
                row["accuracy_outbreak"]
            )
            mycursor.execute(sql, values)

    # Commit การเปลี่ยนแปลง
    mydb.commit()
    print("Data inserted successfully!")

def newfall_for_adaptive():
    # อ่าน CSV และเพิ่มค่า disease
    with open("newfall_for_adaptive_table.csv", "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # เพิ่มค่า disease
            row["disease"] = "newfall"
            
            # แปลงรูปแบบวันที่
            original_date = row["date-time"]  # ชื่อคอลัมน์ใน CSV
            try:
                formatted_date = datetime.strptime(original_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            except ValueError:
                print(f"Invalid date format: {original_date}")
                continue

            # เตรียมคำสั่ง SQL สำหรับ INSERT
            sql = """
            INSERT INTO adaptive (
                disease, sevirity, true_label_7_day, predicted_label_7_day, accuracy_7_day,
                true_label_14_day, predicted_label_14_day, accuracy_14_day,
                true_label_outbreak, predicted_label_outbreak, accuracy_outbreak, create_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                row["disease"], row["sevirity"], row["true_label_7_day"], row["predicted_label_7_day"],
                row["accuracy_7_day"], row["true_label_14_day"], row["predicted_label_14_day"],
                row["accuracy_14_day"], row["true_label_outbreak"], row["predicted_label_outbreak"],
                row["accuracy_outbreak"], formatted_date
            )
            mycursor.execute(sql, values)

    # Commit การเปลี่ยนแปลง
    mydb.commit()
    print("Data inserted successfully!")
    
newfall_for_adaptive()