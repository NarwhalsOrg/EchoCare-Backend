from pydantic import BaseModel
from typing import List, Optional, Dict

class Meal(BaseModel):
    day: str
    breakfast: str
    lunch: str
    dinner: str

class DietPlanRequest(BaseModel):
    name: str
    veg_preference: bool  # True for vegetarian, False for non-veg


class FoodOption(BaseModel):
    foodname: List[str]
    calarys: str
    ingredents: List[str]
    eleragic: str
    article_link: Optional[str] = ""

class MealDetail(BaseModel):
    Nutrication: List[str]
    foodoption: FoodOption

class DayMeals(BaseModel):
    Breakfast: MealDetail
    Lunch: MealDetail
    Dinner: MealDetail

class DietPlanResponse(BaseModel):
    name: str
    veg_preference: bool
    week_plan: Dict[str, DayMeals]  # e.g., {"Monday": DayMeals, ...}
    pdf_url: Optional[str] = None
    message: Optional[str] = None
