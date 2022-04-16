import React, {useState, useEffect} from 'react'
import axios from 'axios';
import './Search.css';


export default function Search() {
    const [foods, setFoods] = useState([]);

    useEffect(() => {
        getAllFoods();
    }, [])

    const getAllFoods = async () => {
        const res = await axios.get("https://food-nutrition.canada.ca/api/canadian-nutrient-file/food/?lang=en&type=json");
        setFoods(res.data);
    }

    return (
        <div className="search-container">
            <p>search container</p>

            <div className="search-bar">
                <input />
            </div>
            <div className="search-picklist">
            {
                foods.map(food => (
                    <li className="food-item" key={food.food_code}>
                        {food.food_description}
                    </li>
                   
                ))
            }
            </div>
            
        </div>
    )
}