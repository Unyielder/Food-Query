import requests


def get_foods(text):
    res = requests.get("https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json")
    foods = res.json()
    return foods
