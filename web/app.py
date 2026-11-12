import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="ChronoRevive Horology Atelier API", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR, exist_ok=True)
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

SHOWCASE_MODELS = [
    {
        "id": "mdl-01",
        "brand": "Omega",
        "model": "Speedmaster Professional 'Pre-Moon'",
        "year": "1968",
        "caliber": "Calibre 321 (Column Wheel Chronograph)",
        "restoration_hours": 74,
        "tasks": "Разборка колонного колеса, восстановление англажа мостов, замена сломанного триба минутного счетчика, сохранение оригинального ступенчатого циферблата.",
        "accuracy_result": "+1.8 сек/сутки, амплитуда 295°"
    },
    {
        "id": "mdl-02",
        "brand": "Patek Philippe",
        "model": "Calatrava Automatic",
        "year": "1956",
        "caliber": "Calibre 12-600 AT (Ротор из 18K золота)",
        "restoration_hours": 92,
        "tasks": "Очистка эмалевого циферблата горячей сушкой, деликатная полировка золотого гильошированного ротора, регулировка спирали Breguet.",
        "accuracy_result": "+0.6 сек/сутки, амплитуда 310°"
    },
    {
        "id": "mdl-03",
        "brand": "Rolex",
        "model": "Submariner 'Meters First'",
        "year": "1972",
        "caliber": "Calibre 1520",
        "restoration_hours": 58,
        "tasks": "Восстановление заводных фасок корпуса, стабилизация оригинального тритиевого люминофора, замена прокладок и опрессовка до 200м.",
        "accuracy_result": "+2.1 сек/сутки, водозащита 20 BAR подтверждена"
    }
]

ORDERS_DATABASE = {
    "CR-8492": {
        "order_id": "CR-8492",
        "client_name": "Константин В.",
        "brand": "Omega Speedmaster 1968",
        "caliber": "Calibre 321",
        "current_stage": 4, # Stage 5 of 6 (0-indexed 4)
        "stages": [
            {"title": "Полная разборка и дефектовка", "status": "completed", "date": "02.11.2026"},
            {"title": "Ультразвуковая очистка камней и колес", "status": "completed", "date": "05.11.2026"},
            {"title": "Изготовление утраченной цапфы триба", "status": "completed", "date": "08.11.2026"},
            {"title": "Восстановление циферблата и люма", "status": "completed", "date": "10.11.2026"},
            {"title": "Юстировка точности (Witschi Chronoscope)", "status": "in_progress", "date": "Текущий этап"},
            {"title": "Тестирование герметичности в барокамере", "status": "pending", "date": "Ожидание"}
        ],
        "master_notes": "Амплитуда колебаний баланса доведена до 292°. Выкачка 0.1 мс. Финальная проверка изохронизма."
    }
}

APPRAISALS_LOG = []

class AppraisalRequest(BaseModel):
    client_name: str = Field(..., min_length=2)
    client_contact: str = Field(..., min_length=5)
    watch_brand: str = Field(..., min_length=2)
    caliber: Optional[str] = "Неизвестен / Требуется вскрытие"
    vintage_decade: str
    defect_description: str = Field(..., min_length=5)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "chronorevive_api", "version": "1.0.0"}

@app.get("/api/showcase-models")
def get_showcase():
    return {"status": "success", "models": SHOWCASE_MODELS}

@app.get("/api/track-order/{order_id}")
def track_order(order_id: str):
    order_id_clean = order_id.strip().upper()
    order = ORDERS_DATABASE.get(order_id_clean)
    if not order:
        # Fallback dynamic mock for any test ID
        return {
            "status": "success",
            "found": True,
            "order": {
                "order_id": order_id_clean,
                "client_name": "Клиент ателье",
                "brand": "Vintage Swiss Timepiece",
                "caliber": "Manual Mechanical",
                "current_stage": 2,
                "stages": [
                    {"title": "Полная разборка и дефектовка", "status": "completed", "date": "Завершено"},
                    {"title": "Ультразвуковая очистка камней и колес", "status": "completed", "date": "Завершено"},
                    {"title": "Полировка англажа и осей", "status": "in_progress", "date": "Текущий этап"},
                    {"title": "Реставрация циферблата", "status": "pending", "date": "Ожидание"},
                    {"title": "Юстировка точности хода", "status": "pending", "date": "Ожидание"},
                    {"title": "Финальный тест изохронизма", "status": "pending", "date": "Ожидание"}
                ],
                "master_notes": "Механизм очищен от застарелой смазки. Ведется ручная полировка мостов."
            }
        }
    return {"status": "success", "found": True, "order": order}

@app.post("/api/appraisal-request")
def create_appraisal(req: AppraisalRequest):
    ticket_id = f"AP-{len(APPRAISALS_LOG) + 201}"
    
    # Calculate estimated ballpark based on brand & defect
    est_min = 25000
    est_max = 65000
    if any(b in req.watch_brand.lower() for b in ["patek", "rolex", "vacheron", "lange"]):
        est_min += 20000
        est_max += 45000

    record = {
        "ticket_id": ticket_id,
        "client_name": req.client_name,
        "client_contact": req.client_contact,
        "watch_brand": req.watch_brand,
        "caliber": req.caliber,
        "vintage_decade": req.vintage_decade,
        "defect_description": req.defect_description,
        "estimate_range": f"{est_min:,} – {est_max:,} ₽".replace(",", " "),
        "status": "verdict_ready"
    }
    APPRAISALS_LOG.append(record)
    return {
        "status": "success",
        "message": f"Заявка на оценку #{ticket_id} принята. Предварительный расчет готов!",
        "appraisal": record
    }

@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(TEMPLATES_DIR, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>ChronoRevive Horology Atelier</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.app:app", host="0.0.0.0", port=3019, reload=True)
