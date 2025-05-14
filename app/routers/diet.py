from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.diet import DietPlanRequest, DietPlanResponse
from app.services.ml.diet_plan import generate_weekly_plan
import pandas as pd

router = APIRouter(tags=["Diet Plan"])

# Load dataset once at startup
df = pd.read_csv("app/data/IndianFoodDatasetCSV.csv")  # Adjust path as needed
# Assuming the dataset has columns like 'Recipe', 'Ingredients', 'Veg', etc.

@router.post("/diet/weekly", response_model=DietPlanResponse)
async def get_weekly_diet_plan(request: DietPlanRequest, background_tasks: BackgroundTasks):
    try:
        week_plan = generate_weekly_plan(request.name, request.veg_preference, df)
        # Optionally, generate PDF and set pdf_url here
        return DietPlanResponse(
            name=request.name,
            veg_preference=request.veg_preference,
            week_plan=week_plan
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diet plan error: {str(e)}")
