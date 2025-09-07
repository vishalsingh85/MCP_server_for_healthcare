from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import statistics

app = FastAPI(title="MCP Healthcare Server", version="1.0")

# -------------------------------
# 🗂 Fake DB Simulation
# -------------------------------
patients = {}

# -------------------------------
# 📌 Data Models
# -------------------------------
class Vitals(BaseModel):
    patient_id: str
    hr: int
    bp_sys: int
    bp_dia: int
    spo2: int
    steps: int
    sleep_hours: Optional[float] = None
    sugar: Optional[float] = None

class Alert(BaseModel):
    patient_id: str
    message: str

# -------------------------------
# 🧾 Save Vitals
# -------------------------------
@app.post("/save_vitals")
def save_vitals(data: Vitals):
    if data.patient_id not in patients:
        patients[data.patient_id] = []
    patients[data.patient_id].append(data.dict())
    return {"status": "success", "saved": data.dict()}

# -------------------------------
# 📊 Get Latest Vitals
# -------------------------------
@app.get("/get_vitals/{patient_id}")
def get_vitals(patient_id: str):
    if patient_id in patients:
        return {"status": "found", "latest": patients[patient_id][-1]}
    return {"status": "not_found"}

# -------------------------------
# 📈 Trend Analysis
# -------------------------------
@app.get("/trend/{patient_id}")
def vitals_trend(patient_id: str):
    if patient_id not in patients:
        return {"status": "not_found"}

    records = patients[patient_id]
    trends = {}

    for key in ["hr", "bp_sys", "bp_dia", "spo2", "steps", "sleep_hours", "sugar"]:
        values = [r[key] for r in records if r.get(key) is not None]
        if values:
            trends[key] = {
                "average": round(statistics.mean(values), 2),
                "min": min(values),
                "max": max(values),
                "last": values[-1]
            }

    return {"status": "ok", "trends": trends, "records": len(records)}

# -------------------------------
# 🚨 Health Risk Analysis
# -------------------------------
@app.get("/analyze/{patient_id}")
def analyze_health(patient_id: str):
    if patient_id not in patients:
        return {"status": "not_found"}

    latest = patients[patient_id][-1]
    risks = []

    if latest["bp_sys"] > 140 or latest["bp_dia"] > 90:
        risks.append("⚠️ Hypertension detected")
    if latest["spo2"] < 94:
        risks.append("⚠️ Possible Hypoxia (low oxygen)")
    if latest["hr"] > 100:
        risks.append("⚠️ Tachycardia (high heart rate)")
    if latest["sleep_hours"] and latest["sleep_hours"] < 6:
        risks.append("⚠️ Sleep deprivation risk")
    if latest["sugar"] and latest["sugar"] > 140:
        risks.append("⚠️ High blood sugar risk")

    return {"status": "ok", "latest": latest, "risks": risks or ["✅ No critical risks detected"]}

# -------------------------------
# 📩 SOS Alerts
# -------------------------------
@app.post("/send_alert")
def send_alert(data: Alert):
    # 🔥 Yahan real SMS/Email API (Twilio/SMTP) integrate kar sakte ho
    return {"status": "alert_sent", "to": data.patient_id, "message": data.message}

# -------------------------------
# 🧠 Mental Wellness Micro-Coach
# -------------------------------
@app.get("/wellness/{patient_id}")
def mental_wellness(patient_id: str):
    tips = [
        "🧘 Take 5 deep breaths — inhale 4 sec, hold 4 sec, exhale 6 sec.",
        "✍️ Write down one thing you’re grateful for today.",
        "🚶 Go for a 5-min walk to refresh your mood.",
        "📵 Take a 10-min break from screens and stretch.",
        "🎧 Listen to calming music for 3 minutes."
    ]
    return {"status": "ok", "patient": patient_id, "tip": statistics.choice(tips)}
