from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

user_clicks = {
    "user_123": ["cooking", "cooking", "landscaping"],
    "user_456": ["tech", "sports", "gaming"],
}

category_recommendations = {
    "cooking": ["baking", "kitchen gadgets"],
    "landscaping": ["gardening", "outdoor tools"],
    "tech": ["smartphones", "laptops"],
    "sports": ["fitness equipment", "running gear"],
    "gaming": ["consoles", "PC games"]
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

    # If user_id does not exist in user_clicks, create a new set of clicks
    if user_id not in user_clicks:
        user_clicks[user_id] = []

    # Append the clicked category
    user_clicks[user_id].append(clicked_category)

    print(f"Updated click history for {user_id}: {user_clicks[user_id]}")

    return {"status": "success", "message": f"Click recorded for {clicked_category}"}

@app.get("/get-recommendations/{user_id}")
async def get_recommendations(user_id: str):
    if user_id not in user_clicks:
        return {"status": "error", "message": "User not found"}
    last_clicked_category = user_clicks[user_id][-1]
    recommendations = category_recommendations.get(last_clicked_category, [])
    return {
        "status": "success",
        "last_clicked_category": last_clicked_category,
        "recommendations": recommendations
    }
