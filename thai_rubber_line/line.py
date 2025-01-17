from database import connect_database, initialize_db, register_user, change_user_address, have_user, get_lat_long_user, change_user_tel, change_user_area, change_user_land_type, change_user_soil_type, change_user_rubber_type, change_user_weather_station, change_user_weather_serial, get_user_data, hour_add_weather, get_notification
from line_flex_message import flex_message_function

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, ImageMessage, TextMessage, TextSendMessage
import os
import json
from upload_image import upload_image
from open_meteo import get_weather
from geocoding import get_geocode
from wunderground import get_wether_wunderground
import os
from dotenv import load_dotenv
import threading
import time
from function import check_have_weather_station
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

user_register_state = {}
registration_data = {}
user_edit_state = {}

user_flex_state = {}  # ติดตามสถานะ Flex Message
user_last_action = {}  # ติดตามการกระทำล่าสุดของผู้ใช้
disease = {}

is_register = False

# Store user data
disease_summary = {}  # Use dictionary to group by user_id
processing_count = {}  # Track number of images being processed
summary_timer = {}  # Store threading.Timer for each user

disease_flex_message = {}

disease_temp = {}
disease_user_data = {}
# Line bot setup
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ฟังก์ชันตั้งเวลา Timeout แบบ Loop 1 ชั่วโมง

mydb, mycursor = connect_database()


def set_timeout_loop():
    def timeout_action():
        hour_add_weather(mydb, mycursor)
        print("Update hour weather")
        set_timeout_loop()  # เรียกตัวเองซ้ำเพื่อ Loop
    threading.Timer(60*60, timeout_action).start()


set_timeout_loop()


@app.route("/webhook", methods=['POST'])
def webhook():
    # Get the signature from the request header
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # Handle the webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    global disease
    # Get the image content
    mydb, mycursor = connect_database()
    user_id = event.source.user_id

    is_register = have_user(mydb, mycursor, user_id)
    if not register_user:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="คุณยังไม่ได้ลงทะเบียน!"))

    message_content = line_bot_api.get_message_content(event.message.id)
    image_path = f"received_{event.message.id}.jpg"

    is_dicease, disease_json, predicted_class, class_data, confidence, data_json, text_predict_7days, text_predict_14days, text_disease = upload_image(
        mydb, mycursor, user_id, message_content)
    disease = json.loads(disease_json)

    # =========================================================

    disease_user_data[user_id] = []
    # =========================================================

    user_flex_state[user_id] = True
    user_last_action[user_id] = "image_uploaded"

    # =========================================================
    # Update disease summary
    if user_id not in disease_summary:
        disease_temp[user_id] = []
        disease_summary[user_id] = []
        processing_count[user_id] = 0

    disease_summary[user_id].append(
        {'class': predicted_class, 'name': class_data, 'confidence': confidence})
    processing_count[user_id] += 1
    # ==
    disease_temp[user_id].append(disease)
    # ==
    # Define function to send summary

    def send_summary():
        summary = {}
        disease_user_data[user_id].append(disease_temp[user_id])
        for entry in disease_summary[user_id]:
            key = f"{entry['name']}"
            if key not in summary:
                summary[key] = {'count': 0, 'confidence': []}
            summary[key]['count'] += 1
            summary[key]['confidence'].append(entry['confidence'])

        summary_text = "สรุปผลการวิเคราะห์:\n\n"
        for index, (name, details) in enumerate(summary.items()):
            avg_confidence = sum(details['confidence']) / details['count']
            if text_predict_7days == "" and text_predict_14days == "" and text_disease == "":
                summary_text += f"- {name} มี {details['count']} รูป"
            else:
                summary_text += f"- {name} มี {details['count']} รูป\n- {text_predict_7days}\n- {text_predict_14days}\n- {text_disease}"

            if index < len(summary) - 1:
                summary_text += "\n\n"

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=summary_text))
        # Clear summary after sending response
        disease_summary[user_id] = []
        disease_temp[user_id] = []
        processing_count[user_id] = 0
        summary_timer[user_id] = None

        items_array = [
            {"header": 'ลักษณะอาการของโรค', "action": 'ลักษณะอาการของโรค',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785695/symptom_hwlv8d.png"},
            {"header": 'ระยะของโรค', "action": 'ระยะของโรค',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785719/phase_qqrlfq.png"},
            {"header": 'สาเหตุการเกิดโรค', "action": 'สาเหตุการเกิดโรค',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785736/cause_vkg04q.png"},
            {"header": 'สภาพที่เหมาะสมต่อการระบาด', "action": 'สภาพที่เหมาะสมต่อการระบาด',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785744/scourge_plzzmj.png"},
            {"header": 'การป้องกัน', "action": 'การป้องกัน',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785749/protect_enmih6.png"},
            {"header": 'วิธีรักษา', "action": 'วิธีรักษา',
                "img_url": "https://res.cloudinary.com/djfkjbnnr/image/upload/v1734785755/treat_jrz1tf.png"},
        ]
        flex_message_function(user_id,
                              items_array, predicted_class)

    # Cancel previous timer if exists
    if user_id in summary_timer and summary_timer[user_id] is not None:
        summary_timer[user_id].cancel()

    # Start a new timer
    summary_timer[user_id] = threading.Timer(1.5, send_summary)
    summary_timer[user_id].start()


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # Acknowledge receipt
    print("Text received!")
    global is_register, user_flex_state, user_last_action, disease

    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    text = event.message.text
    mydb, mycursor = connect_database()

    # Check if user is already registered
    is_register = have_user(mydb, mycursor, user_id)
    
    if user_id not in user_register_state and text == "ลงทะเบียนเข้าใช้งาน":
        user_register_state[user_id] = "start"
        registration_data[user_id] = {
            "id": user_id, "line_name": profile.display_name}
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="กรุณากรอกเบอร์โทรติดต่อ"))
    elif user_id in user_register_state:
        state = user_register_state[user_id]
        print("state", state)
        if state == "start":
            print("wow")
            registration_data[user_id]['tel'] = text
            user_register_state[user_id] = "address"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ ต้องมี ตำบล อำเภอ และจังหวัด"))
        elif state == "address":
            address = text
            result = get_geocode(address)

            if result["status"] != 200:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="กรุณากรอก ตำบล อำเภอ และจังหวัดให้ครบถ้วน!"))
                return

            registration_data[user_id]['address'] = text
            registration_data[user_id]['address_format'] = result["formatted_address"]
            registration_data[user_id]['province'] = result["province"]
            registration_data[user_id]['district'] = result["district"]
            registration_data[user_id]['subdistrict'] = result["subdistrict"]
            registration_data[user_id]['latitude'] = float(
                result["latitude"])
            registration_data[user_id]['longitude'] = float(
                result["longitude"])
            user_register_state[user_id] = "area"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="กรุณากรอกขนาดพื้นที่ (ไร่)"))
        elif state == "area":
            registration_data[user_id]['area'] = text
            user_register_state[user_id] = "land_type"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="กรุณากรอกลักษณะพื้นที่ของคุณ"))

        elif state == "land_type":
            registration_data[user_id]['land_type'] = text
            user_register_state[user_id] = "soil_type"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="กรุณากรอกลักษณะดินของคุณ"))

        elif state == "soil_type":
            registration_data[user_id]['soil_type'] = text
            user_register_state[user_id] = "rubber_type"
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="กรุณากรอกพันธุ์ยางของคุณ"))

        elif state == "rubber_type":
            registration_data[user_id]['rubber_type'] = text
            user_register_state[user_id] = "weather_station"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="มีเครื่องวัดสภาพอากาศหรือไม่ (พิมพ์ 'มี' หรือ 'ไม่มี')"))

        elif state == "weather_station":
            if text == "มี":
                registration_data[user_id]['weather_station'] = True
                user_register_state[user_id] = "weather_serial"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text="กรุณากรอก Serial ของเครื่องวัดสภาพอากาศ"))
            else:
                registration_data[user_id]['weather_station'] = False
                registration_data[user_id]['weather_serial'] = None
                user_register_state.pop(user_id)
                register_user(mydb, mycursor, registration_data[user_id])
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

        elif state == "weather_serial":
            registration_data[user_id]['weather_serial'] = text
            user_register_state.pop(user_id)
            register_user(mydb, mycursor, registration_data[user_id])
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

            # Editing process
        elif state.startswith("edit_"):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=f"แก้ไข{field}เรียบร้อย!"))

        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))

    if is_register and text == "ลงทะเบียนเข้าใช้งาน":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="คุณได้ลงทะเบียนเรียบร้อยแล้ว!"))
        return

    # if user_id not in user_register_state and text == "ลงทะเบียนเข้าใช้งาน":
    #     user_register_state[user_id] = "start"
    #     registration_data[user_id] = {
    #         "id": user_id, "line_name": profile.display_name}
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text="กรุณากรอกเบอร์โทรติดต่อ"))
    # elif user_id in user_register_state:
    #     state = user_register_state[user_id]
    #     print("state", state)
    #     if state == "start":
    #         print("wow")
    #         registration_data[user_id]['tel'] = text
    #         user_register_state[user_id] = "address"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ"))
    #     elif state == "address":
    #         address = text
    #         result = get_geocode(address)
    #         registration_data[user_id]['address'] = text
    #         registration_data[user_id]['address_format'] = result["formatted_address"]
    #         registration_data[user_id]['latitude'] = float(
    #             result["latitude"])
    #         registration_data[user_id]['longitude'] = float(
    #             result["longitude"])
    #         user_register_state[user_id] = "area"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="กรุณากรอกขนาดพื้นที่ (ไร่)"))
    #     elif state == "area":
    #         registration_data[user_id]['area'] = text
    #         user_register_state[user_id] = "land_type"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="กรุณากรอกลักษณะพื้นที่ของคุณ"))

    #     elif state == "land_type":
    #         registration_data[user_id]['land_type'] = text
    #         user_register_state[user_id] = "soil_type"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกลักษณะดินของคุณ"))

    #     elif state == "soil_type":
    #         registration_data[user_id]['soil_type'] = text
    #         user_register_state[user_id] = "rubber_type"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกพันธุ์ยางของคุณ"))

    #     elif state == "rubber_type":
    #         registration_data[user_id]['rubber_type'] = text
    #         user_register_state[user_id] = "weather_station"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="มีเครื่องวัดสภาพอากาศหรือไม่ (พิมพ์ 'มี' หรือ 'ไม่มี')"))

    #     elif state == "weather_station":
    #         if text == "มี":
    #             registration_data[user_id]['weather_station'] = True
    #             user_register_state[user_id] = "weather_serial"
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #                 text="กรุณากรอก Serial ของเครื่องวัดสภาพอากาศ"))
    #         else:
    #             registration_data[user_id]['weather_station'] = False
    #             registration_data[user_id]['weather_serial'] = None
    #             user_register_state.pop(user_id)
    #             register_user(mydb, mycursor, registration_data[user_id])
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

    #     elif state == "weather_serial":
    #         registration_data[user_id]['weather_serial'] = text
    #         user_register_state.pop(user_id)
    #         register_user(mydb, mycursor, registration_data[user_id])
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

    #         # Editing process
    #     # elif state.startswith("edit_"):
    #     #     line_bot_api.reply_message(
    #     #         event.reply_token, TextSendMessage(text=f"แก้ไข{field}เรียบร้อย!"))

    #     else:
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))

    if (not is_register and text != "ลงทะเบียนเข้าใช้งาน") or (not is_register and user_id not in user_register_state):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="คุณยังไม่ได้ลงทะเบียน!"))

  # ตรวจสอบ State ของผู้ใช้
    if user_id in user_register_state:
        state = user_register_state[user_id]

        # กรณีที่อยู่ในสถานะแก้ไข
        if state == "edit_tel":
            tel = text
            data = {
                'id': user_id,
                'tel': tel
            }

            change_user_tel(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="แก้ไขเบอร์โทรเรียบร้อย!"))
        elif state == "edit_address":
            address = text
            result = get_geocode(address)

            if result["status"] != 200:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="กรุณากรอก ตำบล อำเภอ และจังหวัดให้ครบถ้วน!"))
                return

            data = {
                'id': user_id,
                'address': text,
                'address_format': result["formatted_address"],
                'province': result["province"],
                'district': result["district"],
                'subdistrict': result["subdistrict"],
                'latitude': float(result["latitude"]),
                'longitude': float(result["longitude"])
            }

            change_user_address(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="แก้ไขที่อยู่เรียบร้อย!"))
        elif state == "edit_area":
            area = text
            data = {
                'id': user_id,
                'area': area
            }

            change_user_area(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="แก้ไขขนาดพื้นที่เรียบร้อย!"))
        elif state == "edit_land_type":
            land_type = text
            data = {
                'id': user_id,
                'land_type': land_type
            }

            change_user_land_type(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="แก้ไขลักษณะพื้นที่เรียบร้อย!"))
        elif state == "edit_soil_type":
            soil_type = text
            data = {
                'id': user_id,
                'soil_type': soil_type
            }

            change_user_soil_type(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="แก้ไขลักษณะดินเรียบร้อย!"))
        elif state == "edit_rubber_type":
            rubber_type = text
            data = {
                'id': user_id,
                'rubber_type': rubber_type
            }

            change_user_rubber_type(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="แก้ไขพันธุ์ยางเรียบร้อย!"))
        elif state == "edit_weather_station":
            if text == "มี":
                weather_station = True
                user_register_state[user_id] = "edit_weather_serial"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text="กรุณากรอก Serial ของเครื่องวัดสภาพอากาศ"))
            else:
                weather_station = False
                data = {
                    'id': user_id,
                    'weather_station': weather_station
                }
                change_user_weather_station(mydb, mycursor, data)

                del user_register_state[user_id]

                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text="แก้ไขเครื่องวัดสภาพอากาศเรียบร้อย!"))
        elif state == "edit_weather_serial":
            weather_serial = text
            data = {
                'id': user_id,
                'weather_station': True,
                'weather_serial': weather_serial
            }

            change_user_weather_serial(mydb, mycursor, data)

            del user_register_state[user_id]

            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="แก้ไข Serial ของเครื่องวัดสภาพอากาศเรียบร้อย!"))

        # ลบ State หลังจากบันทึกข้อมูล
        return

    # ถ้าไม่มี State ให้ตรวจสอบคำสั่งแก้ไข
    editable_fields = {
        "แก้ไขเบอร์โทร": "edit_tel",
        "แก้ไขที่อยู่": "edit_address",
        "แก้ไขขนาดพื้นที่": "edit_area",
        "แก้ไขลักษณะพื้นที่": "edit_land_type",
        "แก้ไขลักษณะดิน": "edit_soil_type",
        "แก้ไขพันธุ์ยาง": "edit_rubber_type",
        "แก้ไขเครื่องวัดสภาพอากาศ": "edit_weather_station"
    }

    if text in editable_fields and is_register:
        user_register_state[user_id] = editable_fields[text]
        if text != "แก้ไขเครื่องวัดสภาพอากาศ":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text=f"กรุณากรอกข้อมูลใหม่สำหรับ {text.replace('แก้ไข', '')}"))
        elif text == "แก้ไขที่อยู่":
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text=f"กรุณากรอกข้อมูลใหม่สำหรับ {text.replace('แก้ไข', '')} (ตำบล อำเภอ จังหวัด)"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text=f"กรุณากรอกข้อมูลใหม่สำหรับ {text.replace('แก้ไข', '')} (พิมพ์ 'มี' หรือ 'ไม่มี')"))
        return
    elif text in editable_fields and not is_register:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="คุณยังไม่ได้ลงทะเบียน!"))
        return

    # if user_id not in user_register_state and text == "ลงทะเบียนเข้าใช้งาน":
    #     user_register_state[user_id] = "start"
    #     registration_data[user_id] = {
    #         "id": user_id, "line_name": profile.display_name}
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text="กรุณากรอกเบอร์โทรติดต่อ"))
    # elif user_id in user_register_state:
    #     state = user_register_state[user_id]
    #     print("state", state)
    #     if state == "start":
    #         print("wow")
    #         registration_data[user_id]['tel'] = text
    #         user_register_state[user_id] = "address"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ ต้องมี ตำบล อำเภอ และจังหวัด"))
    #     elif state == "address":
    #         address = text
    #         result = get_geocode(address)

    #         if result["status"] != 200:
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="กรุณากรอก ตำบล อำเภอ และจังหวัดให้ครบถ้วน!"))
    #             return

    #         registration_data[user_id]['address'] = text
    #         registration_data[user_id]['address_format'] = result["formatted_address"]
    #         registration_data[user_id]['province'] = result["province"]
    #         registration_data[user_id]['district'] = result["district"]
    #         registration_data[user_id]['subdistrict'] = result["subdistrict"]
    #         registration_data[user_id]['latitude'] = float(
    #             result["latitude"])
    #         registration_data[user_id]['longitude'] = float(
    #             result["longitude"])
    #         user_register_state[user_id] = "area"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="กรุณากรอกขนาดพื้นที่ (ไร่)"))
    #     elif state == "area":
    #         registration_data[user_id]['area'] = text
    #         user_register_state[user_id] = "land_type"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="กรุณากรอกลักษณะพื้นที่ของคุณ"))

    #     elif state == "land_type":
    #         registration_data[user_id]['land_type'] = text
    #         user_register_state[user_id] = "soil_type"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกลักษณะดินของคุณ"))

    #     elif state == "soil_type":
    #         registration_data[user_id]['soil_type'] = text
    #         user_register_state[user_id] = "rubber_type"
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="กรุณากรอกพันธุ์ยางของคุณ"))

    #     elif state == "rubber_type":
    #         registration_data[user_id]['rubber_type'] = text
    #         user_register_state[user_id] = "weather_station"
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="มีเครื่องวัดสภาพอากาศหรือไม่ (พิมพ์ 'มี' หรือ 'ไม่มี')"))

    #     elif state == "weather_station":
    #         if text == "มี":
    #             registration_data[user_id]['weather_station'] = True
    #             user_register_state[user_id] = "weather_serial"
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #                 text="กรุณากรอก Serial ของเครื่องวัดสภาพอากาศ"))
    #         else:
    #             registration_data[user_id]['weather_station'] = False
    #             registration_data[user_id]['weather_serial'] = None
    #             user_register_state.pop(user_id)
    #             register_user(mydb, mycursor, registration_data[user_id])
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

    #     elif state == "weather_serial":
    #         registration_data[user_id]['weather_serial'] = text
    #         user_register_state.pop(user_id)
    #         register_user(mydb, mycursor, registration_data[user_id])
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

    #         # Editing process
    #     elif state.startswith("edit_"):
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text=f"แก้ไข{field}เรียบร้อย!"))

    #     else:
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))

    if text == "สภาพอากาศ":
        # mycursor.execute("USE thai_rubber")
        # mycursor.execute(
        #     "SELECT weather_station, weather_serial FROM plantation WHERE id = %s", (user_id,))
        # result = mycursor.fetchone()
        # have_weather_station = result[0]
        have_weather_station = check_have_weather_station(mycursor, user_id)

        if (have_weather_station[0]):
            get_wether_wunderground(have_weather_station[1])

            format_text = (
                f"สภาพอากาศวันนี้\n"
                f"อุณหภูมิเฉลี่ย: {1}°C\n"
                f"ปริมาณน้ำฝน: {1} mm\n"
                f"ชั่วโมงที่มีฝน: {1} ชั่วโมง\n"
                f"ความเร็วลมสูงสุด: {1} m/s\n"
                f"ทิศทางลม: {1}°\n"
                f"รังสีแสงรวม: {1} W/m²\n"
                f"ความชื้นสัมพัทธ์: {1}%\n"
                f"ความชื้นในดิน: {1}%\n"
                f"ปุ๋ย: {1}"
            )

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=format_text))
        else:
            user_id = event.source.user_id
            latitude, longitude = get_lat_long_user(mydb, mycursor, user_id)

            daily_data = get_weather(latitude, longitude)
            temperature_2m_avg = daily_data["temperature_2m_avg"][0]
            precipitation_sum = daily_data["precipitation_sum"][0]
            wind_speed_10m_max = daily_data["wind_speed_10m_max"][0]
            wind_direction_10m_dominant = daily_data["wind_direction_10m_dominant"][0]
            shortwave_radiation_sum = daily_data["shortwave_radiation_sum"][0]
            relative_humidity_2m = daily_data["relative_humidity_2m"][0]
            soil_moisture_9_to_27cm = daily_data["soil_moisture_9_to_27cm"][0]

            temperature_2m_avg = round(float(temperature_2m_avg), 2)
            precipitation_sum = round(float(precipitation_sum), 2)
            wind_speed_10m_max = round(float(wind_speed_10m_max), 2)
            wind_direction_10m_dominant = round(
                float(wind_direction_10m_dominant), 2)
            shortwave_radiation_sum = round(float(shortwave_radiation_sum), 2)
            relative_humidity_2m = round(float(relative_humidity_2m), 2)
            soil_moisture_9_to_27cm = round(float(soil_moisture_9_to_27cm), 2)

            format_text = (
                f"สภาพอากาศวันนี้\n"
                f"อุณหภูมิเฉลี่ย: {temperature_2m_avg}°C\n"
                f"ปริมาณน้ำฝน: {precipitation_sum} mm\n"
                f"ความเร็วลมสูงสุด: {wind_speed_10m_max} m/s\n"
                f"ทิศทางลม: {wind_direction_10m_dominant}°\n"
                f"รังสีแสงรวม: {shortwave_radiation_sum} W/m²\n"
                f"ความชื้นสัมพัทธ์: {relative_humidity_2m}%\n"
                f"ความชื้นในดิน: {soil_moisture_9_to_27cm}%"
            )
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=format_text))

    if text == "ทำนายผล":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="ส่งรูปภาพที่ต้องการทำนายผล"))

    # if text in ["ลักษณะอาการของโรค", "ระยะของโรค", "สาเหตุการเกิดโรค", "สภาพที่เหมาะสมต่อการระบาด", "การป้องกัน", "วิธีรักษา"]:
    #     print("kutttttttttttttttt", text)
    #     if user_id in user_flex_state and user_flex_state[user_id]:
    #         # ตรวจสอบการกระทำล่าสุดว่าผู้ใช้เคยอัปโหลดรูปภาพหรือไม่
    #         if user_id in user_last_action and user_last_action[user_id] == "image_uploaded":
    #             header = {
    #                 'ลักษณะอาการของโรค': 'symptom',
    #                 'ระยะของโรค': 'phase',
    #                 'สาเหตุการเกิดโรค': 'cause',
    #                 'สภาพที่เหมาะสมต่อการระบาด': 'scourge',
    #                 'การป้องกัน': 'protect',
    #                 'วิธีรักษา': 'treat'
    #             }

    #             key = header.get(text)  # ตรวจสอบ key ที่แมปกับ text
    #             key = key.strip() if key else None  # ลบช่องว่าง (ถ้ามี)

    #             format_text = (f"{text}\n\n")

    #             # เก็บรายการชื่อโรคที่เคยแสดงแล้ว เพื่อลบข้อมูลซ้ำ
    #             displayed_diseases = set()

    #             # กรองข้อมูลที่ไม่ซ้ำลงในลิสต์ใหม่
    #             filtered_data = []
    #             for disease_test in disease_flex_message[user_id]:
    #                 disease_name = disease_test['name']
    #                 if disease_name not in displayed_diseases:  # ถ้าไม่ซ้ำให้เพิ่ม
    #                     filtered_data.append(disease_test)
    #                     displayed_diseases.add(disease_name)

    #             # วนลูปแสดงผลจากข้อมูลที่ผ่านการกรองแล้ว
    #             for index, disease_test in enumerate(filtered_data):
    #                 response_header = disease_test[key]['header']
    #                 response_text = disease_test[key]['text']
    #                 disease_name = disease_test['name']

    #                 # เพิ่มข้อมูลลงในข้อความตอบกลับ
    #                 format_text += f"{disease_name}\n{response_text}"

    #                 # เพิ่ม "\n\n" ถ้าไม่ใช่รายการสุดท้าย
    #                 if index < len(filtered_data) - 1:
    #                     format_text += "\n\n"

    #             # ส่งข้อความสรุปข้อมูลกลับให้ผู้ใช้
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(text=format_text))

    #         else:
    #             line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #                 text="กรุณาส่งรูปภาพก่อนเพื่อดูข้อมูลเพิ่มเติม"))
    #     else:
    #         user_flex_state[user_id] = False
    #         user_last_action[user_id] = None
    #         disease = {}
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(
    #             text="กรุณาส่งรูปภาพก่อนเพื่อดูข้อมูลเพิ่มเติม"))
    # else:
    #     user_flex_state[user_id] = False
    #     user_last_action[user_id] = None
    #     disease = {}

    # ตรวจสอบคำสั่งเกี่ยวกับ Flex Message
    if text in ["ลักษณะอาการของโรค", "ระยะของโรค", "สาเหตุการเกิดโรค", "สภาพที่เหมาะสมต่อการระบาด", "การป้องกัน", "วิธีรักษา"]:
        if user_id in user_flex_state and user_flex_state[user_id]:
            key_map = {
                "ลักษณะอาการของโรค": "symptom",
                "ระยะของโรค": "phase",
                "สาเหตุการเกิดโรค": "cause",
                "สภาพที่เหมาะสมต่อการระบาด": "scourge",
                "การป้องกัน": "protect",
                "วิธีรักษา": "treat"
            }
            key = key_map[text]

            # แสดงข้อมูลทุกโรคใน session ปัจจุบัน
            format_text = f"{text}\n\n"
            diseases = disease_user_data[user_id][0]

            for index, disease_data in enumerate(diseases):
                disease_name = disease_data['name']
                response_header = disease_data[key]['header']
                response_text = disease_data[key]['text']

                format_text += f"{disease_name}\n"
                format_text += f"{response_header}\n{response_text}"

                # เพิ่มบรรทัดใหม่ระหว่างโรค (ยกเว้นรายการสุดท้าย)
                if index < len(diseases) - 1:
                    format_text += "\n\n"

            # ส่งข้อความ Flex Message
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=format_text))
        else:
            # หากยังไม่มีการอัปโหลดภาพ
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="กรุณาส่งรูปภาพก่อนเพื่อดูข้อมูลเพิ่มเติม"))

    if text == "ดูข้อมูลที่ลงทะเบียน":
        data = get_user_data(mydb, mycursor, user_id)
        text_format = (
            f"เบอร์โทรศัพท์: {data['tel']}\n"
            f"ที่อยู่: {data['address']}\n"
            f"พื้นที่ (ไร่): {data['area']} ไร่\n"
            f"ลักษณะพื้นที่: {data['land_type']}\n"
            f"ลักษณะดิน: {data['soil_type']}\n"
            f"พันธุ์ยาง: {data['rubber_type']}\n"
            f"เครื่องวัดสภาพอากาศ: {data['weather_serial']}"
        )
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=text_format))

    if text == "ติดต่อเจ้าหน้าที่":
        data = get_notification(mydb, mycursor, user_id)
        print("data", data)
        status_array = {
            "request_not_accept": 'ยังไม่ได้รับคำร้อง',
            "process_of_contact": 'กำลังติดต่อ',
            "process": 'กำลังดำเนินการ',
            "explore": 'สำรวจ',
            "follow_watchout": 'ติดตาม/ระวัง',
            "heal": 'รักษา',
        }
        summary_text = "ข้อมูลโรค:\n\n"
        for index, (disease, status, create_at) in enumerate(data):
            disease_format = disease.replace("\n", "")
            
            # เพิ่ม 7 ชั่วโมงให้เวลา UTC
            thai_time = create_at + timedelta(hours=7)
        
            # แสดงเฉพาะปี เดือน วัน
            thai_date = thai_time.strftime("%Y-%m-%d")
            
            summary_text += f"- {disease} : {status_array[status]}\nวันที่พบ {thai_date}"
            
            
            if index < len(data) - 1:
                summary_text += "\n"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=summary_text))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
