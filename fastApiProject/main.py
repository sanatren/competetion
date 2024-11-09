from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import predict_sentiment

app = FastAPI()
#run this command to start the api    fastapi dev main.py

# Define the data model for feedback input
class FeedbackInput(BaseModel):
    feedback: str
    vendor_id: int


# In-memory storage for feedback scores by vendor (for demonstration) migrate it to a db for prod.
vendor_feedback_scores = {}


@app.post("/analyze-feedback/")
async def analyze_feedback(feedback: FeedbackInput):
    sentiment = predict_sentiment(feedback.feedback)
    vendor_id = feedback.vendor_id

    # Update vendor feedback scores
    if vendor_id not in vendor_feedback_scores:
        vendor_feedback_scores[vendor_id] = {"positive": 0, "total": 0}

    # Increment feedback scores based on sentiment
    if sentiment == "Good":
        vendor_feedback_scores[vendor_id]["positive"] += 1
    vendor_feedback_scores[vendor_id]["total"] += 1

    return {
        "vendor_id": vendor_id,
        "feedback": feedback.feedback,
        "sentiment": sentiment
    }


@app.get("/top-vendors/")
async def get_top_vendors():
    # Calculate positive feedback ratio for each vendor
    vendor_ranking = {
        vendor_id: scores["positive"] / scores["total"]
        for vendor_id, scores in vendor_feedback_scores.items()
        if scores["total"] > 0
    }

    # Sort vendors by positive feedback ratio
    ranked_vendors = sorted(vendor_ranking.items(), key=lambda x: x[1], reverse=True)
    return ranked_vendors

