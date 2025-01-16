import os
from werkzeug.utils import secure_filename
import time
import json
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms
from database import send_noti_first_time, get_lat_long_user
from open_meteo import get_weather
from function import check_have_weather_station
from wunderground import get_wether_wunderground

from line_flex_message import flex_message_function
from pydantic import BaseModel
from model.powder.predict_powder_risk import predict_powder_risk
from model.powder.predict_powder_7days import predict_powder_7days
from model.powder.predict_powder_14days import predict_powder_14days

from model.newfall.predict_newfall_risk import predict_newfall_risk
from model.newfall.predict_newfall_7days import predict_newfall_7days
from model.newfall.predict_newfall_14days import predict_newfall_14days

from predict_enum import PREDICT_POWDER_DISEASE_TEXT, PREDICT_POWDER_7_14DAYS_TEXT, PREDICT_NEWFALL_DISEASE_TEXT, PREDICT_NEWFALL_7_14DAYS_TEXT
# ข้อมูลอินพุต


class InputDataRisk(BaseModel):
    temperature_max: float
    temperature_min: float
    temperature_mean: float
    precipitation_sum: float
    wind_speed: float
    wind_gusts: float
    wind_direction: float
    shortwave_radiation_sum: float
    humidity: float
    soil_moisture: float

class InputDataForecast(BaseModel):
    temperature_max: float
    temperature_min: float
    temperature_mean: float
    precipitation_sum: float
    wind_speed: float
    wind_gusts: float
    wind_direction: float
    shortwave_radiation_sum: float
    humidity: float
    soil_moisture: float
    sevirity: int

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained ResNet18 model and adjust the final layer
num_classes = 10  # Ensure this matches the number of classes in your saved model weights
# model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Linear(model.fc.in_features, num_classes)
# model.load_state_dict(torch.load('model_weights.pth', map_location=device))
state_dict = torch.load('model_weights.pth',
                        map_location=device, weights_only=True)
# Allow partial match if necessary
model.load_state_dict(state_dict, strict=False)
model = model.to(device)
model.eval()  # Set the model to evaluation mode

data_json = {}
# Image preprocessing transformations
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def upload_image(mydb, mycursor, user_id, message_content):
    folder = 'uploads'

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    if not os.path.exists(folder):
        os.makedirs(folder)

    # กำหนดชื่อไฟล์แบบไม่ซ้ำ
    filename = f"{user_id}_{int(time.time())}.jpg"
    file_path = os.path.join(folder, filename)

    # บันทึกไฟล์จาก message_content
    with open(file_path, 'wb') as f:
        for chunk in message_content.iter_content():
            f.write(chunk)

    # Preprocess the image
    image = Image.open(file_path).convert("RGB")
    input_tensor = preprocess(image).unsqueeze(0).to(
        device)  # Add batch dimension and move to device

    # Make prediction
    with torch.no_grad():
        output = model(input_tensor)
        # Get the predicted class index
        predicted_class = output.argmax(dim=1).item()
        # Get the confidence score
        confidence = torch.softmax(output, dim=1).max().item()

    with open('test.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)

    class_data = data_json[str(predicted_class)]["name"]
    disease_level = data_json[str(predicted_class)]["level"]
    is_dicease = data_json[str(predicted_class)]["disease"]

    disease = data_json[str(predicted_class)]
    disease_json = json.dumps(disease, ensure_ascii=False, indent=4)

    temperature_2m_max = None
    temperature_2m_min = None
    temperature_2m_avg = None
    precipitation_sum = None
    wind_speed_10m_max = None
    wind_gusts_10m_max = None
    wind_direction_10m_dominant = None
    shortwave_radiation_sum = None
    relative_humidity_2m = None
    soil_moisture_9_to_27cm = None
    # Wether data
    have_weather_station = check_have_weather_station(mycursor, user_id)
    if (have_weather_station[0]):
        data = get_wether_wunderground(have_weather_station[1])

        temperature_2m_max = data["imperial"]["tempHigh"]
        temperature_2m_min = data["imperial"]["tempLow"]
        temperature_2m_avg = data["imperial"]["tempAvg"]
        precipitation_sum = data["imperial"]["precipTotal"]
        wind_speed_10m_max = data["imperial"]["windspeedHigh"]
        wind_gusts_10m_max = data["imperial"]["windgustHigh"]
        wind_direction_10m_dominant = data["winddirAvg"]
        shortwave_radiation_sum = data["solarRadiationHigh"]
        relative_humidity_2m = data["humidityAvg"]
        soil_moisture_9_to_27cm = 0
    else:
        latitude, longitude = get_lat_long_user(mydb, mycursor, user_id)
        daily_data = get_weather(latitude, longitude)
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
    # บันทึก Path ลงฐานข้อมูล
    mycursor.execute("USE thai_rubber")
    sql = """
    INSERT INTO uploads (id, path, create_at) VALUES (%s, %s, NOW())
    """
    value = (user_id, file_path)
    mycursor.execute(sql, value)
    
    last_inserted_id = mycursor.lastrowid

    data_risk = {
        "temperature_max": temperature_2m_max,
        "temperature_min": temperature_2m_min,
        "temperature_mean": temperature_2m_avg,
        "precipitation_sum": precipitation_sum,
        "wind_speed": wind_speed_10m_max,
        "wind_gusts": wind_gusts_10m_max,
        "wind_direction": wind_direction_10m_dominant,
        "shortwave_radiation_sum": shortwave_radiation_sum,
        "humidity": relative_humidity_2m,
        "soil_moisture": soil_moisture_9_to_27cm,
    }

    data_predict = data_risk
    data_predict["sevirity"] = disease_level

    data_predict_7days = {
        "predicted_label": 0,
        "current_accuracy": 0,
        "drift_detected": False
    }
    data_predict_14days = {
        "predicted_label": 0,
        "current_accuracy": 0,
        "drift_detected": False
    }
    data_predict_risk = {
        "predicted_label": 0,
        "current_accuracy": 0,
        "drift_detected": False
    }
    print("data_predict", data_predict)
    text_predict_7days = ""
    text_predict_14days = ""
    text_predict_risk = ""
    text_disease = ""
    if (str(predicted_class) == "6" or str(predicted_class) == "7" or str(predicted_class) == "8"):
        data_predict_7days = predict_powder_7days(InputDataForecast(**data_predict))
        data_predict_14days = predict_powder_14days(InputDataForecast(**data_predict))
        data_predict_risk = predict_powder_risk(InputDataRisk(**data_risk))
        
        text_predict_7days = f"ระดับความรุนแรงในอีก 7 วันข้างหน้า: {PREDICT_POWDER_7_14DAYS_TEXT[data_predict_7days['predicted_label']]}"
        text_predict_14days = f"ระดับความรุนแรงในอีก 14 วันข้างหน้า: {PREDICT_POWDER_7_14DAYS_TEXT[data_predict_14days['predicted_label']]}"
        text_disease = f"ความเสี่ยงในการระบาด: {PREDICT_POWDER_DISEASE_TEXT[data_predict_risk['predicted_label']]}"
    elif (str(predicted_class) == "0" or str(predicted_class) == "1" or str(predicted_class) == "2"):
        data_predict_7days = predict_newfall_7days(InputDataForecast(**data_predict))
        data_predict_14days = predict_newfall_14days(InputDataForecast(**data_predict))
        data_predict_risk = predict_newfall_risk(InputDataRisk(**data_risk))
        
        text_predict_7days = f"ระดับความรุนแรงในอีก 7 วันข้างหน้า: {PREDICT_NEWFALL_7_14DAYS_TEXT[data_predict_7days['predicted_label']]}"
        text_predict_14days = f"ระดับความรุนแรงในอีก 14 วันข้างหน้า: {PREDICT_NEWFALL_7_14DAYS_TEXT[data_predict_14days['predicted_label']]}"
        text_disease = f"ความเสี่ยงในการระบาด: {PREDICT_NEWFALL_DISEASE_TEXT[data_predict_risk['predicted_label']]}"
    sql = """
    INSERT INTO weather_disease (transaction_id, disease, temperature_max, temperature_min, temperature_avg, precipitation_sum, wind_speed, wind_direction, wind_gust, shortwave_radiation_sum, relative_humidity, soil_moisture, sevirity, forecast_7days, forecast_14days, risk, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    value = (last_inserted_id, class_data, temperature_2m_max, temperature_2m_min, temperature_2m_avg, precipitation_sum, wind_speed_10m_max,
             wind_direction_10m_dominant, wind_gusts_10m_max, shortwave_radiation_sum, relative_humidity_2m, soil_moisture_9_to_27cm, disease_level, data_predict_7days["predicted_label"], data_predict_14days["predicted_label"], data_predict_risk["predicted_label"])
    mycursor.execute(sql, value)
    mydb.commit()
    # ส่งข้อความแจ้งเตือน
    data = {
        "transaction_id": last_inserted_id,
        "id": user_id,
        "disease": disease,
        "disease_level": disease_level,
        "risk": data_predict_risk["predicted_label"],
    }
    send_noti_first_time(mydb, mycursor, data)
    mydb.commit()
    
    print(f"Image saved at: {file_path}")
    return is_dicease, disease_json, predicted_class, class_data, confidence, data_json, text_predict_7days, text_predict_14days, text_disease
