import requests


# Food names
url = r"https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json"
# Serving sizes
#url = r"https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?type=json&lang=en"
# Nutrient groups
#url = r"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientgroup/?lang=en&type=json"
# Nuttient names
#url = r"https://food-nutrition.canada.ca/api/canadian-nutrient-file/nutrientname/?lang=en&type=json"
# Nutrient amount
#url = r"https://food-nutrition.canada.ca/api/drug/nutrientamount/?type=json&lang=en"

data = requests.get(url)
data = data.json()

foodNames = [dd['food_description'] for dd in data]
print(foodNames)
