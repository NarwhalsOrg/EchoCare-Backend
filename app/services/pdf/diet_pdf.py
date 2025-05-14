from fpdf import FPDF
import os

def generate_diet_pdf(week_plan: dict, filename: str):
    """
    week_plan: Dictionary with days as keys and values as DayMeals (dict with Breakfast, Lunch, Dinner).
    filename: Output PDF filename (should include path, e.g., 'static/username_diet.pdf')
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 12, "1-Week Personalized Diet Plan", ln=True, align='C')
    pdf.ln(6)

    days = list(week_plan.keys())
    meals = ['Breakfast', 'Lunch', 'Dinner']

    for day in days:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, day, ln=True, align='L')
        pdf.set_font("Arial", '', 12)

        # Table header
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(35, 8, "Meal", border=1, fill=True)
        pdf.cell(40, 8, "Nutrition", border=1, fill=True)
        pdf.cell(40, 8, "Calories", border=1, fill=True)
        pdf.cell(40, 8, "Allergens", border=1, fill=True)
        pdf.cell(0, 8, "Ingredients", border=1, ln=True, fill=True)

        for meal in meals:
            meal_detail = getattr(week_plan[day], meal, None) if not isinstance(week_plan[day], dict) else week_plan[day].get(meal)
            if meal_detail:
                nutrition = ", ".join(meal_detail.Nutrication) if hasattr(meal_detail, 'Nutrication') else ", ".join(meal_detail.get('Nutrication', []))
                foodoption = meal_detail.foodoption if hasattr(meal_detail, 'foodoption') else meal_detail.get('foodoption', {})
                calories = foodoption.calarys if hasattr(foodoption, 'calarys') else foodoption.get('calarys', '')
                allergens = foodoption.eleragic if hasattr(foodoption, 'eleragic') else foodoption.get('eleragic', '')
                ingredients = ", ".join(foodoption.ingredents) if hasattr(foodoption, 'ingredents') else ", ".join(foodoption.get('ingredents', []))

                pdf.cell(35, 8, meal, border=1)
                pdf.cell(40, 8, nutrition, border=1)
                pdf.cell(40, 8, calories, border=1)
                pdf.cell(40, 8, allergens, border=1)
                pdf.cell(0, 8, ingredients, border=1, ln=True)
                
                # Steps (multi-cell for readability)
                pdf.set_font("Arial", 'I', 11)
                steps = foodoption.foodname if hasattr(foodoption, 'foodname') else foodoption.get('foodname', [])
                pdf.multi_cell(0, 7, f"Steps: {' | '.join(steps)}", border=0)
                pdf.set_font("Arial", '', 12)
                pdf.ln(1)
        pdf.ln(2)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
