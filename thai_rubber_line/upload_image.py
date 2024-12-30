import os
from werkzeug.utils import secure_filename
import time
import json
from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms

from line_flex_message import flex_message_function

# Device configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the pre-trained ResNet18 model and adjust the final layer
num_classes = 10  # Ensure this matches the number of classes in your saved model weights
# model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
model.fc = nn.Linear(model.fc.in_features, num_classes)
# model.load_state_dict(torch.load('model_weights.pth', map_location=device))
state_dict = torch.load('model_weights.pth', map_location=device, weights_only=True)
model.load_state_dict(state_dict, strict=False)  # Allow partial match if necessary
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
    input_tensor = preprocess(image).unsqueeze(0).to(device)  # Add batch dimension and move to device

    # Make prediction
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = output.argmax(dim=1).item()  # Get the predicted class index
        confidence = torch.softmax(output, dim=1).max().item()  # Get the confidence score
    
    with open('test.json', 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        
    class_data = data_json[str(predicted_class)]["name"]
    is_dicease = data_json[str(predicted_class)]["disease"]
    
    disease = data_json[str(predicted_class)]
    disease_json = json.dumps(disease, ensure_ascii=False, indent=4)

    # บันทึก Path ลงฐานข้อมูล
    mycursor.execute("USE thai_rubber")
    sql = """
    INSERT INTO uploads (id, path, disease, disease_level, temperature_avg, precipitation_sum, precipitation_hours, wind_speed, wind_direction, uv_index, shortwave_radiation_sum, forecast_7days, risk, create_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    value = (user_id, file_path, class_data, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    mycursor.execute(sql, value)
    mydb.commit()
    print(f"Image saved at: {file_path}")
    return is_dicease, disease_json, predicted_class, class_data, confidence, data_json