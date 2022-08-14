from fuzzywuzzy import process, fuzz
import requests


def fuzzy_search(text):
    res = requests.get("https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json")
    all_foods = res.json()
    res = process.extract(text, [record['food_description'] for record in all_foods], scorer=fuzz.token_sort_ratio, limit=50)
    print(res)
    search_results = []

    for name in res:
        for mapp in all_foods:
            if name[0] == mapp['food_description']:
                search_results.append({'food_code': mapp['food_code'], 'food_description': name[0]})

    return search_results
