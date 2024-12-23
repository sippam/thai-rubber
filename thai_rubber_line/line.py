from database import connect_database, initialize_db, register_user, change_user_address, have_user, get_lat_long_user
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

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

user_register_state = {}
registration_data = {}

user_flex_state = {}  # ติดตามสถานะ Flex Message
user_last_action = {}  # ติดตามการกระทำล่าสุดของผู้ใช้
disease = {}

is_register = False

# Line bot setup
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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
    message_content = line_bot_api.get_message_content(event.message.id)
    image_path = f"received_{event.message.id}.jpg"

    mydb, mycursor = connect_database()
    is_dicease, disease_json, predicted_class, class_data, confidence, data_json = upload_image(
        mydb, mycursor, event.source.user_id, message_content)
    disease = json.loads(disease_json)

    user_flex_state[event.source.user_id] = True
    user_last_action[event.source.user_id] = "image_uploaded"

    # response_flex_message = ''
    if (is_dicease):
        response_flex_message = f"ผลการวิเคราะห์ : {class_data}\nความแม่นยำ : {confidence:.2f}"
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
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=response_flex_message))
        flex_message_function(event.source.user_id,
                              items_array, predicted_class)

    else:
        description = data_json[str(predicted_class)]["description"]
        response_message = f"ผลการวิเคราะห์ : {class_data}\nความแม่นยำ : {confidence:.2f}\n\n{description}"
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=response_flex_message))

    # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_flex_message))


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
    if is_register and text == "ลงทะเบียนเข้าใช้งาน":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="คุณได้ลงทะเบียนเรียบร้อยแล้ว!"))
        return

    editable_fields = {
        "แก้ไขเบอร์โทร": "edit_tel",
        "แก้ไขที่อยู่": "edit_address",
        "แก้ไขขนาดพื้นที่": "edit_area",
        "แก้ไขลักษณะพื้นที่": "edit_land_type",
        "แก้ไขลักษณะดิน": "edit_soil_type",
        "แก้ไขพันธุ์ยาง": "edit_rubber_type",
        "แก้ไขเครื่องวัดสภาพอากาศ": "edit_weather_station"
    }

    if text in editable_fields:
        user_register_state[user_id] = editable_fields[text]
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=f"กรุณากรอกข้อมูลใหม่สำหรับ {text.replace('แก้ไข', '')}"))
        return

    # if text == "ลงทะเบียนเข้าใช้งาน":
    #     # user_register_state[user_id] = "awaiting_tel"
    #     is_register = have_user(mydb, mycursor, user_id)
    #     if is_register:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="คุณได้ลงทะเบียนเรียบร้อยแล้ว!"))
    #     else:
    #         user_register_state[user_id] = "start"
    #         registration_data[user_id] = {"id": user_id, "line_name": profile.display_name}
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="กรุณากรอกเบอร์โทรติดต่อ"))

    #         state = user_register_state[user_id]
    if user_id not in user_register_state and text == "ลงทะเบียนเข้าใช้งาน":
        user_register_state[user_id] = "start"
        registration_data[user_id] = {
            "id": user_id, "line_name": profile.display_name}
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="กรุณากรอกเบอร์โทรติดต่อ"))
    elif user_id in user_register_state:
        state = user_register_state[user_id]
        if state == "start":
            registration_data[user_id]['tel'] = text
            user_register_state[user_id] = "address"

            # try:
            #     data = {
            #         'id': user_id,
            #         'line_name': profile.display_name,
            #         'tel': text
            #     }
            # register_user(mydb, mycursor, data)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ"))
            # except Exception as e:
            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))
        elif state == "address":
            address = text
            result = get_geocode(address)
            registration_data[user_id]['address'] = text
            registration_data[user_id]['address_format'] = result["formatted_address"]
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
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="มีเครื่องวัดสภาพอากาศหรือไม่ (พิมพ์ 'มี' หรือ 'ไม่มี')"))

        elif state == "weather_station":
            if text == "มี":
                registration_data[user_id]['weather_station'] = True
                user_register_state[user_id] = "weather_serial"
                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text="กรุณากรอก Serial ของเครื่องวัดสภาพอากาศ"))
            else:
                # registration_data[user_id]['weather_station'] = "ไม่มี"
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

            # field = state.replace("edit_", "")
            # mydb, mycursor = connect_database()
            # query = f"UPDATE users SET {field} = %s WHERE id = %s"
            # values = (text, user_id)
            # mycursor.execute(query, values)
            # mydb.commit()
            # user_register_state.pop(user_id)

            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=f"แก้ไข{field}เรียบร้อย!"))

        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))

            # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ"))

    # elif user_id in user_register_state and user_register_state[user_id] == "awaiting_tel" and not is_register:
    #     try:
    #         user_register_state[user_id] = "awaiting_address"
    #         data = {
    #             'id': user_id,
    #             'line_name': profile.display_name,
    #             'tel': text
    #         }
    #         register_user(mydb, mycursor, data)

    #         # address_format = get_geocode(text)
    #         # data = {
    #         #     'id': user_id,
    #         #     'address': text,
    #         #     'address_format': address_format["formatted_address"],
    #         #     'latitude': float(address_format["latitude"]),
    #         #     'longitude': float(address_format["longitude"])
    #         # }
    #         # change_user_address(mydb, mycursor, data)

    #         # user_register_state.pop(user_id)
    #         # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="กรุณากรอกที่อยู่ของคุณ"))

    #         # line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ลงทะเบียนเรียบร้อย!"))

    #     except Exception as e:
    #         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))
    # elif user_id in user_register_state and user_register_state[user_id] == "awaiting_address" and is_register:

    if text == "แก้ไขที่อยู่":
        user_register_state[user_id] = "awaiting_new_address"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text="กรุณากรอกที่อยู่ใหม่ของคุณ"))
    elif user_id in user_register_state and user_register_state[user_id] == "awaiting_new_address":
        try:
            address = text
            result = get_geocode(address)
            print("result", result)
            print("result[formatted_address]", result["formatted_address"])
            print("result[latitude]", result["latitude"])
            print("result[longitude]", result["longitude"])
            data = {
                'id': user_id,
                'address': text,
                'address_format': result["formatted_address"],
                'latitude': float(result["latitude"]),
                'longitude': float(result["longitude"])
            }
            mydb, mycursor = connect_database()
            change_user_address(mydb, mycursor, data)
            user_register_state.pop(user_id)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="แก้ไขที่อยู่เรียบร้อย!"))
        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="เกิดข้อผิดพลาด!"))

    if text == "สภาพอากาศ":
        user_id = event.source.user_id
        latitude, longitude = get_lat_long_user(mydb, mycursor, user_id)

        daily_data = get_weather(latitude, longitude)
        temperature_2m_avg = daily_data["temperature_2m_avg"][0]
        precipitation_sum = daily_data["precipitation_sum"][0]
        precipitation_hours = daily_data["precipitation_hours"][0]
        wind_speed_10m_max = daily_data["wind_speed_10m_max"][0]
        wind_direction_10m_dominant = daily_data["wind_direction_10m_dominant"][0]

        temperature_2m_avg = round(float(temperature_2m_avg), 2)
        precipitation_sum = round(float(precipitation_sum), 2)
        precipitation_hours = round(float(precipitation_hours), 2)
        wind_speed_10m_max = round(float(wind_speed_10m_max), 2)
        wind_direction_10m_dominant = round(
            float(wind_direction_10m_dominant), 2)

        format_text = (
            f"สภาพอากาศวันนี้\n"
            f"อุณหภูมิเฉลี่ย: {temperature_2m_avg}°C\n"
            f"ปริมาณน้ำฝน: {precipitation_sum} mm\n"
            f"ชั่วโมงที่มีฝน: {precipitation_hours} ชั่วโมง\n"
            f"ความเร็วลมสูงสุด: {wind_speed_10m_max} m/s\n"
            f"ทิศทางลม: {wind_direction_10m_dominant}°"
        )
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=format_text))

    if text in ["ลักษณะอาการของโรค", "ระยะของโรค", "สาเหตุการเกิดโรค", "สภาพที่เหมาะสมต่อการระบาด", "การป้องกัน", "วิธีรักษา"]:
        print("kutttttttttttttttt", text)
        if user_id in user_flex_state and user_flex_state[user_id]:
            # ตรวจสอบการกระทำล่าสุดว่าผู้ใช้เคยอัปโหลดรูปภาพหรือไม่
            if user_id in user_last_action and user_last_action[user_id] == "image_uploaded":

                header = {
                    'ลักษณะอาการของโรค': 'symptom',
                    'ระยะของโรค': 'phase',
                    'สาเหตุการเกิดโรค': 'cause',
                    'สภาพที่เหมาะสมต่อการระบาด': 'scourge',
                    'การป้องกัน': 'protect',
                    'วิธีรักษา': 'treat'
                }

                key = header.get(text)  # ตรวจสอบ key ที่แมปกับ text
                key = key.strip() if key else None  # ลบช่องว่าง (ถ้ามี)

                if key and key in disease:
                    response_header = disease[key]['header']
                    response_text = disease[key]['text']

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(
                            text=f"{response_header}\n\n{response_text}")
                    )
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="ไม่พบข้อมูลที่คุณต้องการ")
                    )

            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(
                    text="กรุณาส่งรูปภาพก่อนเพื่อดูข้อมูลเพิ่มเติม"))
        else:
            user_flex_state[user_id] = False
            user_last_action[user_id] = None
            disease = {}
            line_bot_api.reply_message(event.reply_token, TextSendMessage(
                text="กรุณาส่งรูปภาพก่อนเพื่อดูข้อมูลเพิ่มเติม"))
    else:
        user_flex_state[user_id] = False
        user_last_action[user_id] = None
        disease = {}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
