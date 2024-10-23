from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import Counter

app = FastAPI()

# User click history mock data
user_clicks = {
    "user_123": ["cooking", "home_cleaning", "laundry", "grocery_shopping", "management_tasks"],
    "user_456": ["cooking", "school_work", "grocery_shopping"],
}

# Updated category recommendations
category_recommendations = {
    "cooking": [
        "Home Style Cooking",
        "Specialty Cooking",
        "Baking and Pastry"
    ],
    "home_cleaning": [
        "Regular House Cleaning",
        "Deep Cleaning"
    ],
    "grocery_shopping": [
        "Light Purchasing",
        "Bulk Purchasing"
    ],
    "laundry": [
        "Dry Cleaning",
        "Wash and Hang to Dry",
        "Laundry Pick up"
    ],
    "management_tasks": [
        "Schedule Management",
        "Task Delegation",
        "Budgeting"
    ],
    "school_work": [
        "Homework Assistance",
        "Study Sessions"
    ]
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
async def get_recommendations(user_id: str, window_size: int = 5):
    if user_id not in user_clicks:
        return {"status": "error", "message": "User not found"}

    user_click_history = user_clicks[user_id]
    recent_clicks = user_click_history[-window_size:]

    category_counts = Counter(recent_clicks)
    most_common_categories = category_counts.most_common(3)

    recommendations = {}
    for category, _ in most_common_categories:
        recommendations[category] = category_recommendations.get(category, [])

    return {
        "status": "success",
        "most_common_categories": [category for category, _ in most_common_categories],
        "recommendations": recommendations,
        "recent_clicks": recent_clicks
    }

@app.delete("/reset-clicks/{user_id}")
async def reset_clicks(user_id: str):
    if user_id in user_clicks:
        del user_clicks[user_id]  # Remove the user's click history
        return {"status": "success", "message": f"Click history for {user_id} has been reset."}
    else:
        raise HTTPException(status_code=404, detail="User not found")

