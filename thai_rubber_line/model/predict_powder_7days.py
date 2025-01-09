from pydantic import BaseModel
import dill
from river.tree import HoeffdingAdaptiveTreeClassifier
from river.drift import ADWIN
from river import metrics

# --- โหลดโมเดลและ Drift Detector ---
with open('model/powder_adaptive_7_model_with_drift.pkl', 'rb') as f:
    saved_data = dill.load(f)

model = saved_data['model']
drift_detector = saved_data['drift_detector']
accuracy = metrics.Accuracy()

# ตัวนับจำนวนการเรียนรู้
learn_counter = 0  # เริ่มต้นเป็น 0

# ข้อมูลอินพุต
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

def predict_powder_7days(data: InputDataForecast):
    global model, drift_detector, learn_counter

    # ดึงข้อมูลอินพุต
    x = data.dict()

    # ทำนายผล
    y_pred = model.predict_one(x)

    # ใช้การทำนายของโมเดลเองเป็น pseudo-labels สำหรับการเรียนรู้
    y_true = y_pred  # หรือใช้ค่าผลลัพธ์ที่ได้จากโมเดลก่อนหน้าเป็น pseudo-label

    # อัปเดต Metric และ Drift Detector
    if y_pred is not None:
        accuracy.update(y_true, y_pred)
        drift_detector.update(int(y_true != y_pred))

        # ตรวจจับ Drift
        if drift_detector.drift_detected:
            model = HoeffdingAdaptiveTreeClassifier()  # รีเซ็ตโมเดล
            print("Drift detected, resetting model...")

    # เรียนรู้ข้อมูลใหม่
    model.learn_one(x, y_true)  # เรียนรู้จากข้อมูลที่ไม่มี label
    learn_counter += 1  # เพิ่มตัวนับการเรียนรู้

    # บันทึกโมเดลเมื่อครบ 100 ครั้ง
    if learn_counter >= 100:
        with open('model/powder_adaptive_7_model_with_drift.pkl', 'wb') as f:
            dill.dump({'model': model, 'drift_detector': drift_detector}, f)
        print("Model saved after 100 updates.")
        learn_counter = 0  # รีเซ็ตตัวนับ
    
    return {
        "predicted_label": y_pred,
        "current_accuracy": accuracy.get(),
        "drift_detected": drift_detector.drift_detected
    }