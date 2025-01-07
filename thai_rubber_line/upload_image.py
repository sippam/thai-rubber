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

    temperature_2m_avg = None
    precipitation_sum = None
    precipitation_hours = None
    wind_speed_10m_max = None
    wind_direction_10m_dominant = None
    shortwave_radiation_sum = None
    relative_humidity_2m = None
    soil_moisture_9_to_27cm = None
    # Wether data
    have_weather_station = check_have_weather_station(mycursor, user_id)
    if (have_weather_station[0]):
        get_wether_wunderground(have_weather_station[1])
        # print("data", data)
    else:
        latitude, longitude = get_lat_long_user(mydb, mycursor, user_id)
        daily_data = get_weather(latitude, longitude)
        temperature_2m_avg = daily_data["temperature_2m_avg"][0]
        precipitation_sum = daily_data["precipitation_sum"][0]
        precipitation_hours = daily_data["precipitation_hours"][0]
        wind_speed_10m_max = daily_data["wind_speed_10m_max"][0]
        wind_direction_10m_dominant = daily_data["wind_direction_10m_dominant"][0]
        shortwave_radiation_sum = daily_data["shortwave_radiation_sum"][0]
        relative_humidity_2m = daily_data["relative_humidity_2m"][0]
        soil_moisture_9_to_27cm = daily_data["soil_moisture_9_to_27cm"][0]

        temperature_2m_avg = round(float(temperature_2m_avg), 2)
        precipitation_sum = round(float(precipitation_sum), 2)
        precipitation_hours = round(float(precipitation_hours), 2)
        wind_speed_10m_max = round(float(wind_speed_10m_max), 2)
        wind_direction_10m_dominant = round(
            float(wind_direction_10m_dominant), 2)
        shortwave_radiation_sum = round(float(shortwave_radiation_sum), 2)
        relative_humidity_2m = round(float(relative_humidity_2m), 2)
        soil_moisture_9_to_27cm = round(float(soil_moisture_9_to_27cm), 2)
    # บันทึก Path ลงฐานข้อมูล
    mycursor.execute("USE thai_rubber")
    sql = """
    INSERT INTO uploads (id, path, disease, disease_level, temperature_avg, precipitation_sum, precipitation_hours, wind_speed, wind_direction, shortwave_radiation_sum, relative_humidity, soil_moisture, forecast_7days, risk, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    value = (user_id, file_path, class_data, disease_level, temperature_2m_avg, precipitation_sum, precipitation_hours, wind_speed_10m_max,
             wind_direction_10m_dominant, shortwave_radiation_sum, relative_humidity_2m, soil_moisture_9_to_27cm, 0, 0)
    mycursor.execute(sql, value)
    mydb.commit()
    last_inserted_id = mycursor.lastrowid

    data = {
        "transaction_id": last_inserted_id,
        "id": user_id,
        "disease": disease,
        "disease_level": disease_level,
        "risk": 0,
    }
    send_noti_first_time(mydb, mycursor, data)

    mydb.commit()
    print(f"Image saved at: {file_path}")
    return is_dicease, disease_json, predicted_class, class_data, confidence, data_json
