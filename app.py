from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter

app = FastAPI()

user_clicks = {
    "user_123": ["tech", "landscaping", "landscaping", "landscaping", "tech", "sports", "sports", "gaming"],
    "user_456": ["tech", "sports", "gaming"],
}

category_recommendations = {
    "cooking": ["baking", "kitchen gadgets", "cooking classes", "healthy recipes"],
    "landscaping": ["gardening", "outdoor tools", "landscape design"],
    "tech": ["smartphones", "laptops", "tech accessories"],
    "sports": ["fitness equipment", "running gear", "sports apparel"],
    "gaming": ["consoles", "PC games", "gaming accessories"]
}

class ClickData(BaseModel):
    user_id: str
    clicked_category: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Recommendation API!"}

@app.post("/update-clicks")
async def update_clicks(click_data: ClickData):
    user_id = click_data.user_id
    clicked_category = click_data.clicked_category

    print(f"Received click from user: {user_id}, category: {clicked_category}")

    if user_id not in user_clicks:
        user_clicks[user_id] = []

    user_clicks[user_id].append(clicked_category)

    print(f"Updated click history for {user_id}: {user_clicks[user_id]}")

    return {"status": "success", "message": f"Click recorded for {clicked_category}"}

@app.get("/get-recommendations/{user_id}")
async def get_recommendations(user_id: str):
    if user_id not in user_clicks:
        return {"status": "error", "message": "User not found"}

    category_counts = Counter(user_clicks[user_id])
    most_common_categories = category_counts.most_common(3)

    recommendations = {}
    for category, _ in most_common_categories:
        recommendations_for_category = category_recommendations.get(category, [])
        if recommendations_for_category:
            recommendations[category] = recommendations_for_category
        else:
            recommendations[category] = ["No recommendations available"]

    return {
        "status": "success",
        "most_common_categories": [category for category, _ in most_common_categories],
        "recommendations": recommendations
    }
