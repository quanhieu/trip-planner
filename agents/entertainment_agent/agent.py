import asyncio
from datetime import datetime

def generate_itinerary(payload: dict) -> dict:
    start_date = payload.get("start_date")
    end_date = payload.get("end_date")
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        num_days = (end - start).days + 1
    except Exception:
        num_days = 1

    attractions = payload.get("attractions", [])
    if not attractions:
        attractions = [{"name": "Điểm tham quan mặc định", "description": "Mô tả mặc định"}]

    itinerary = []
    for day in range(1, num_days+1):
        day_plan = {
            "day": day,
            "activities": []
        }
        # Chọn 1 điểm tham quan theo vòng lặp (round robin)
        attraction = attractions[(day - 1) % len(attractions)]
        day_plan["activities"].append({
            "time": "Sáng",
            "activity": f"Tham quan {attraction['name']}"
        })
        day_plan["activities"].append({
            "time": "Chiều",
            "activity": "Tự do tham quan khu vực lân cận"
        })
        day_plan["activities"].append({
            "time": "Tối",
            "activity": "Dạo phố và khám phá ẩm thực địa phương"
        })
        itinerary.append(day_plan)
    return {"itinerary": itinerary}

async def execute(payload: dict) -> dict:
    await asyncio.sleep(1)
    return generate_itinerary(payload)
