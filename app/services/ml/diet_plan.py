import pandas as pd
import json
from app.schemas.diet import DietPlanResponse, DayMeals, MealDetail, FoodOption

def get_random_meal(df, course, veg_preference):
    # Filter by course and diet preference
    filtered = df[df['Course'].str.contains(course, na=False)]
    if veg_preference:
        filtered = filtered[filtered['Diet'].str.lower().str.contains("vegetarian", na=False)]
    else:
        filtered = filtered[~filtered['Diet'].str.lower().str.contains("vegetarian", na=False)]
    return filtered.sample(1).iloc[0] if not filtered.empty else None

def generate_weekly_plan(name, veg_preference, df):
    week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    plan = {}
    for day in week_days:
        day_meals = {}
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            course = meal_type  # or map to your dataset's actual course values
            recipe_row = get_random_meal(df, course, veg_preference)
            if recipe_row is not None:
                meal_json = generate_structured_meal(recipe_row, meal_type)
                # Parse LLM output to dict
                meal_struct = json.loads(meal_json)
                # Validate with Pydantic
                meal_detail = MealDetail(**meal_struct)
                day_meals[meal_type] = meal_detail
            else:
                day_meals[meal_type] = None
        plan[day] = DayMeals(**day_meals)
    return plan
