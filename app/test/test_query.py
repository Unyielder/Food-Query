import asyncio

from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.main import app
from app.routers.service import *
import unittest

client = TestClient(app)


class FoodDescTest(unittest.TestCase):
    client = TestClient(app)

    def test_get_index(self):
        """View should return response as html with status_code 200"""
        response = self.client.get('/query')
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        self.assertEqual(response.status_code, 200)

    def test_empty_food_desc(self):
        """View should return error 404 if empty search"""
        response = self.client.post('/query', {"foodDescSearch": " "})
        self.assertEqual(response.status_code, 404)

    def test_non_empty_food_desc(self):
        """View should redirect to food select"""
        response = self.client.post('/query', {"foodDescSearch": 'banana'})
        self.assertEqual(response.status_code, 302)


class FoodSelectTest(unittest.TestCase):
    client = TestClient(app)

    def test_empty_food_select(self):
        """View should return 422 if no selection"""
        response = self.client.post('/query/banana', {"foodName": ""})
        self.assertEqual(response.status_code, 422)

    def test_non_empty_food_select(self):
        """View should redirect to serving_size view"""
        response = self.client.post('/query/banana', {"foodName": "1704;Banana"})
        self.assertEqual(response.status_code, 302)


class ServingsTest(unittest.TestCase):
    client = TestClient(app)

    def test_get_servings_valid_food_id(self):
        """View should display available serving sizes for food"""
        response = asyncio.run(get_food_servings("3086"))
        self.assertEqual(response, [
        {
            "conversion_factor_value": 0.86644,
            "food_code": 3086,
            "food_description": "Tuna salad",
            "measure_name": "100ml"
        },
        {
            "conversion_factor_value": 2.1661,
            "food_code": 3086,
            "food_description": "Tuna salad",
            "measure_name": "250ml"
        },
        {
            "conversion_factor_value": 0.0,
            "food_code": 3086,
            "food_description": "Tuna salad",
            "measure_name": "no serving specified"
        },
        {
            "conversion_factor_value": 1.08305,
            "food_code": 3086,
            "food_description": "Tuna salad",
            "measure_name": "125ml"
        }
    ])

    def test_get_servings_non_existent_food_id(self):
        response = asyncio.run(get_food_servings("99999099"))
        self.assertEqual(response, [])

    def test_get_servings_invalid_food_id(self):
        response = asyncio.run(get_food_servings("xxx"))
        self.assertEqual(response, {"Message": "The request is invalid."})

    def test_empty_serving_select(self):
        response = self.client.post('query/3086/Tuna salad/serving_size', {"ing_measure": ""})
        self.assertEqual(response.status_code, 422)

    def test_non_empty_serving_select(self):
        response = self.client.post('query/3086/Tuna salad/serving_size', {"ing_measure": "100ml"})
        self.assertEqual(response.status_code, 302)


class NutrientsTest(unittest.TestCase):
    client = TestClient(app)

    def test_get_nutrients_valid_data(self):
        """View should return response as html with status_code 200"""
        response = asyncio.run(self.get_good_response())
        self.assertEqual(response.headers["content-type"], "text/html; charset=utf-8")
        self.assertEqual(response.status_code, 200)

    async def get_good_response(self):
        async with AsyncClient(app=app, base_url='http://localhost:8000/query') as ac:
            return await ac.get("/3086/Tuna%20salad/250ml")

    def test_get_nutrients_invalid_data(self):
        """View should return response as html with status_code 200"""
        response = asyncio.run(self.get_bad_response())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail" : "Couldn't find specific food data"})

    async def get_bad_response(self):
        async with AsyncClient(app=app, base_url='http://localhost:8000/query') as ac:
            return await ac.get("/3086/Tuna%20salad/25ml")


