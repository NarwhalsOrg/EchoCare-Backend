from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

def generate_structured_meal(recipe_row, meal_type):
    # recipe_row: a pandas Series from your dataset
    prompt = f"""
Given the following recipe from an Indian food dataset, format it as structured JSON for a {meal_type} meal:

Name: {recipe_row['TranslatedRecipeName']}
Diet: {recipe_row['Diet']}
Ingredients: {recipe_row['TranslatedIngredients']}
Instructions: {recipe_row['TranslatedInstructions']}
Course: {recipe_row['Course']}

Format:
{{
  "Nutrication": ["..."], 
  "foodoption": {{
    "foodname": ["Step 1...", "Step 2...", "..."],
    "calarys": "Estimated calories",
    "ingredents": ["item1", "item2", "..."],
    "eleragic": "e.g. peanuts, milk",
    "article_link": ""
  }}
}}

- Identify if it's high protein, diabetic-friendly, etc.
- Estimate calories.
- Split instructions into clear steps.
- Add common allergens if any.
- Leave article_link blank for now.
"""
    model = init_chat_model(model="gemini-2.0-flash", model_provider="google_genai")
    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful dietitian AI who structures meals for health plans."),
        ("human", prompt)
    ])
    response = model.invoke(template.format())
    return response.content  # Should be a JSON string
