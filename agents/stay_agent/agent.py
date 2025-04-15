import asyncio

def generate_stay_plan(payload: dict) -> dict:
    hotels = payload.get("hotels", [])
    if hotels:
        # Chọn khách sạn có giá thấp nhất
        selected = sorted(hotels, key=lambda x: x.get("price_per_night", float('inf')))[0]
        stay = {
            "name": selected.get("name", "Khách sạn mặc định"),
            "price_per_night": selected.get("price_per_night", 0),
            "note": "Đề xuất dựa trên giá cả phù hợp và vị trí thuận tiện."
        }
    else:
        stay = {
            "name": "Khách sạn mặc định",
            "price_per_night": 500000,
            "note": "Đề xuất mặc định."
        }
    return {"stays": stay}

async def execute(payload: dict) -> dict:
    await asyncio.sleep(1)
    return generate_stay_plan(payload)
