import asyncio

def generate_meal_plan(payload: dict) -> dict:
    restaurants = payload.get("restaurants", [])
    itinerary = payload.get("itinerary", [])
    num_days = len(itinerary) if itinerary else 1
    meal_plan = []
    for day in range(1, num_days + 1):
        restaurant = restaurants[(day - 1) % len(restaurants)] if restaurants else {"name": "Nhà hàng mặc định", "specialty": ""}
        plan = {
            "day": day,
            "breakfast": f"Ăn sáng tại {restaurant['name']}",
            "lunch": f"Ăn trưa tại {restaurant['name']}",
            "dinner": f"Ăn tối tại {restaurant['name']}"
        }
        meal_plan.append(plan)
    return {"meals": meal_plan}

async def execute(payload: dict) -> dict:
    await asyncio.sleep(1)
    return generate_meal_plan(payload)
