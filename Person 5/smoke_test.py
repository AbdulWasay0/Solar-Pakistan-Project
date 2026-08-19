import json
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"


def post(path, data):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as res:
        return json.loads(res.read().decode("utf-8"))


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as res:
        return json.loads(res.read().decode("utf-8"))


if __name__ == "__main__":
    print("/health", get("/health"))
    print("/recommend", post("/recommend", {
        "monthly_units": 600,
        "city": "Lahore",
        "roof_area_sqft": 500,
        "backup_hours": 4,
        "battery_required": True,
        "major_loads": [{"name": "Fan", "watts": 80, "quantity": 3}],
        "system_preference": "auto",
        "grid_available": True,
        "panel_watt": 585
    }))
    print("/chat", post("/chat", {"message": "What is a hybrid solar system?"}))
