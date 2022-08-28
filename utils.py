from fuzzywuzzy import process, fuzz
import requests
import pandas as pd


def fuzzy_search(text: str):
    res = requests.get("https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json")
    all_foods = res.json()
    res = process.extract(text, [record['food_description'] for record in all_foods], scorer=fuzz.token_sort_ratio, limit=50)

    search_results = []
    for name in res:
        for mapp in all_foods:
            if name[0] == mapp['food_description']:
                search_results.append({'food_code': mapp['food_code'], 'food_description': name[0]})

    return search_results


async def get_servings(food_code):
    res = requests.get(f'https://food-nutrition.canada.ca/api/canadian-nutrient-file/servingsize/?id={food_code}&type'
                       f'=json&lang=en')

    servings = res.json()
    print(servings)
    return servings


async def get_food_data(url: str):
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data, index=[i for i in range(len(data))])
    return df