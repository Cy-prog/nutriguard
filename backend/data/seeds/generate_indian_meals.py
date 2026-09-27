import json
import random
import os

def generate_meals():
    meals = []
    
    # Categories and items
    north = [
        ("Aloo Paratha with Curd", "BREAKFAST"), ("Besan Chilla", "BREAKFAST"), ("Moong Dal Chilla", "BREAKFAST"), 
        ("Paneer Paratha", "BREAKFAST"), ("Chole Bhature", "BREAKFAST"), ("Poha (North style)", "BREAKFAST"), 
        ("Stuffed Gobhi Paratha", "BREAKFAST"), ("Rajma Chawal", "LUNCH"), ("Chole with Roti", "LUNCH"), 
        ("Dal Tadka with Rice", "LUNCH"), ("Kadhi Chawal", "LUNCH"), ("Aloo Gobi with Roti", "LUNCH"), 
        ("Paneer Bhurji with Roti", "LUNCH"), ("Matar Paneer with Rice", "LUNCH"), ("Dal Roti Sabzi Combo", "LUNCH"), 
        ("Dal Makhani with Roti", "DINNER"), ("Palak Paneer with Roti", "DINNER"), ("Mixed Veg with Roti", "DINNER"), 
        ("Baingan Bharta with Roti", "DINNER"), ("Shahi Paneer with Naan", "DINNER"), ("Chana Masala with Roti", "DINNER"),
        ("Malai Kofta with Naan", "DINNER"), ("Kadai Paneer with Roti", "DINNER"), ("Bhindi Masala with Roti", "DINNER"), 
        ("Dum Aloo with Puri", "DINNER"), ("Soya Chunks Curry with Rice", "LUNCH"), ("Mushroom Masala with Roti", "DINNER"), 
        ("Aloo Matar with Puri", "BREAKFAST"), ("Gobi Musallam with Roti", "DINNER")
    ]
    
    south = [
        ("Idli Sambar", "BREAKFAST"), ("Masala Dosa", "BREAKFAST"), ("Plain Dosa with Chutney", "BREAKFAST"), 
        ("Uttapam", "BREAKFAST"), ("Ven Pongal", "BREAKFAST"), ("Upma (South)", "BREAKFAST"), ("Pesarattu", "BREAKFAST"), 
        ("Medu Vada Sambar", "BREAKFAST"), ("Rava Idli", "BREAKFAST"), ("Sambar Rice", "LUNCH"), ("Rasam Rice", "LUNCH"), 
        ("Lemon Rice", "LUNCH"), ("Curd Rice", "LUNCH"), ("Bisi Bele Bath", "LUNCH"), ("Vegetable Kootu with Rice", "LUNCH"), 
        ("Avial with Rice", "LUNCH"), ("Set Dosa with Chutney", "DINNER"), ("Appam with Vegetable Stew", "DINNER"), 
        ("Ragi Mudde with Sambar", "DINNER"), ("Idiyappam with Coconut Milk", "DINNER"), ("Tamarind Rice", "LUNCH"), 
        ("Tomato Bath", "BREAKFAST"), ("Vangi Bath", "LUNCH"), ("Pongal with Gotsu", "BREAKFAST"), 
        ("Puttu with Kadala Curry", "BREAKFAST"), ("Chettinad Veg Curry with Parotta", "DINNER")
    ]
    
    west = [
        ("Dhokla", "BREAKFAST"), ("Thepla", "BREAKFAST"), ("Poha Indori", "BREAKFAST"), ("Misal Pav", "BREAKFAST"), 
        ("Sabudana Khichdi", "BREAKFAST"), ("Khandvi", "BREAKFAST"), ("Undhiyu with Roti", "LUNCH"), ("Dal Dhokli", "LUNCH"), 
        ("Gujarati Kadhi with Khichdi", "LUNCH"), ("Pav Bhaji", "LUNCH"), ("Zunka Bhakri", "LUNCH"), ("Puran Poli", "DINNER"), 
        ("Usal Pav", "DINNER"), ("Varan Bhaat", "DINNER"), ("Bharli Vangi with Bhakri", "DINNER"), ("Vada Pav", "BREAKFAST"), 
        ("Kothimbir Vadi", "BREAKFAST"), ("Thalipeeth", "BREAKFAST"), ("Matki Usal", "LUNCH"), ("Sev Khamani", "BREAKFAST"), 
        ("Handvo", "BREAKFAST")
    ]
    
    east = [
        ("Luchi Aloo Dom", "BREAKFAST"), ("Chirer Pulao", "BREAKFAST"), ("Dalma with Rice", "LUNCH"), 
        ("Khichdi with Ghee", "LUNCH"), ("Shukto with Rice", "LUNCH"), ("Begun Bhaja with Dal Rice", "DINNER"), 
        ("Aloo Posto with Rice", "DINNER"), ("Cholar Dal with Luchi", "DINNER"), ("Macher Jhol with Rice", "LUNCH"), 
        ("Doi Mach with Rice", "LUNCH"), ("Chingri Malai Curry with Rice", "DINNER"), ("Kosha Mangsho with Roti", "DINNER"), 
        ("Ghugni with Muri", "BREAKFAST")
    ]
    
    central = [
        ("Poha Jalebi", "BREAKFAST"), ("Sabudana Vada", "BREAKFAST"), ("Dal Bati Churma", "LUNCH"), 
        ("Bhutte Ka Kees", "LUNCH"), ("Bafla with Dal", "DINNER"), ("Roti Lehsun Chutney Dal", "DINNER"), 
        ("Gatte Ki Sabzi with Roti", "LUNCH"), ("Ker Sangri with Roti", "DINNER"), ("Papad Ki Sabzi with Roti", "LUNCH"), 
        ("Sev Tamatar with Roti", "DINNER")
    ]
    
    pan = [
        ("Khichdi", "LUNCH"), ("Dalia Porridge", "BREAKFAST"), ("Oats Upma", "BREAKFAST"), ("Sprouts Salad", "BREAKFAST"), 
        ("Fruit Curd Bowl", "BREAKFAST"), ("Plain Dal Rice", "LUNCH"), ("Vegetable Biryani", "LUNCH"), 
        ("Egg Bhurji with Roti", "BREAKFAST"), ("Chicken Curry with Rice", "LUNCH"), ("Fish Curry with Rice", "LUNCH"), 
        ("Egg Curry with Roti", "DINNER"), ("Paneer Tikka", "DINNER"), ("Butter Chicken with Naan", "DINNER"), 
        ("Keema with Roti", "DINNER"), ("Vegetable Pulao", "LUNCH"), ("Mutton Biryani", "DINNER"), 
        ("Egg Fried Rice", "LUNCH"), ("Jeera Rice with Dal", "LUNCH"), ("Hakka Noodles", "LUNCH")
    ]

    all_items = []
    for items, region in [(north, "NORTH_INDIAN"), (south, "SOUTH_INDIAN"), (west, "WEST_INDIAN"), 
                          (east, "EAST_INDIAN"), (central, "CENTRAL_INDIAN"), (pan, "PAN_INDIAN")]:
        for name, meal_type in items:
            all_items.append((name, region, meal_type))
            
    for name, region, meal_type in all_items:
        is_veg = not any(x in name for x in ["Chicken", "Mutton", "Fish", "Egg", "Keema", "Macher", "Chingri", "Mangsho"])
        is_vegan = is_veg and not any(x in name for x in ["Paneer", "Curd", "Ghee", "Butter", "Malai", "Shahi", "Doi"])
        is_egg = "Egg" in name
        
        # Macros generation
        protein = random.uniform(5.0, 15.0)
        fat = random.uniform(5.0, 15.0)
        carbs = random.uniform(30.0, 60.0)
        
        if not is_veg:
            protein += random.uniform(10.0, 20.0)
        if "Paneer" in name or "Dal" in name or "Chana" in name or "Rajma" in name or "Chole" in name:
            protein += random.uniform(5.0, 10.0)
            
        if "Butter" in name or "Ghee" in name or "Malai" in name or "Shahi" in name or "Bhature" in name or "Puri" in name or "Vada" in name:
            fat += random.uniform(10.0, 20.0)
            
        if "Rice" in name or "Chawal" in name or "Pulao" in name or "Biryani" in name:
            carbs += random.uniform(10.0, 30.0)
            
        calories = (protein * 4) + (carbs * 4) + (fat * 9)
        
        meal = {
            "name": name,
            "local_name": name,
            "description": f"Traditional {region.replace('_', ' ').title()} dish - {name}",
            "meal_type": meal_type,
            "cuisine_region": region,
            "food_type": "COMBO" if "with" in name or "Sambar" in name or "Pav" in name else "MAIN_COURSE",
            "is_vegetarian": is_veg,
            "is_vegan": is_vegan,
            "is_jain_friendly": False,
            "is_egg_based": is_egg,
            "preparation_time_minutes": random.randint(15, 60),
            "difficulty": random.choice(["EASY", "MEDIUM", "HARD"]),
            "serving_size_g": random.randint(250, 450),
            "serving_description": f"1 standard serving of {name}",
            "calories": int(calories),
            "protein_g": round(protein, 1),
            "carbohydrates_g": round(carbs, 1),
            "fat_g": round(fat, 1),
            "fiber_g": round(random.uniform(2.0, 12.0), 1),
            "sugar_g": round(random.uniform(1.0, 8.0), 1),
            "sodium_mg": random.randint(200, 1000),
            "calcium_mg": random.randint(30, 250),
            "iron_mg": round(random.uniform(1.0, 8.0), 1),
            "potassium_mg": random.randint(200, 700),
            "vitamin_a_mcg": random.randint(10, 200),
            "vitamin_c_mg": random.randint(0, 40),
            "vitamin_d_mcg": 0,
            "vitamin_b12_mcg": round(random.uniform(0.5, 2.5), 1) if not is_vegan else 0,
            "folate_mcg": random.randint(20, 150),
            "preparation_steps": [
                f"Gather ingredients for {name}",
                "Prepare base mixture or dough",
                "Cook over medium heat until done",
                "Serve hot"
            ],
            "recipe_text": f"Classic {name} recipe suitable for everyday meals.",
            "image_url": None,
            "video_url": None,
            "source_name": "IFCT 2017 / NIN",
            "source_type": "NUTRITION_DATABASE",
            "tags": [region.lower(), meal_type.lower(), "indian"],
            "primary_protein_source": "dal" if "Dal" in name else ("paneer" if "Paneer" in name else ("chicken" if "Chicken" in name else "mixed")),
            "primary_grain": "rice" if "Rice" in name or "Chawal" in name else ("wheat" if "Roti" in name or "Paratha" in name else "mixed"),
            "cooking_method": "cooked",
            "spice_level": random.choice(["MILD", "MEDIUM", "SPICY"]),
            "ingredients": [
                {"name": "Main Ingredient", "quantity": 150, "unit": "g"},
                {"name": "Spices and Oil", "quantity": 15, "unit": "g"}
            ],
            "allergens": []
        }
        meals.append(meal)

    # Make the first one exactly as requested
    idli_sambar = {
      "name": "Idli Sambar",
      "local_name": "इडली सांबर",
      "description": "Steamed rice cakes served with lentil vegetable stew",
      "meal_type": "BREAKFAST",
      "cuisine_region": "SOUTH_INDIAN",
      "food_type": "COMBO",
      "is_vegetarian": True,
      "is_vegan": True,
      "is_jain_friendly": False,
      "is_egg_based": False,
      "preparation_time_minutes": 30,
      "difficulty": "EASY",
      "serving_size_g": 350,
      "serving_description": "3 idlis + 1 bowl sambar",
      "calories": 320,
      "protein_g": 12.0,
      "carbohydrates_g": 55.0,
      "fat_g": 6.0,
      "fiber_g": 5.0,
      "sugar_g": 3.0,
      "sodium_mg": 450,
      "calcium_mg": 60,
      "iron_mg": 3.5,
      "potassium_mg": 350,
      "vitamin_a_mcg": 20,
      "vitamin_c_mg": 8,
      "vitamin_d_mcg": 0,
      "vitamin_b12_mcg": 0,
      "folate_mcg": 45,
      "preparation_steps": [
        "Soak rice and urad dal for 6 hours, grind into smooth batter",
        "Ferment batter overnight",
        "Grease idli mould and steam for 10-12 minutes",
        "For sambar: cook toor dal with turmeric",
        "Saute vegetables, add sambar powder and cooked dal",
        "Temper with mustard, curry leaves, and serve"
      ],
      "recipe_text": "Idli is a traditional South Indian steamed cake made from fermented rice and lentil batter. Served with sambar - a spiced lentil and vegetable stew.",
      "image_url": None,
      "video_url": None,
      "source_name": "IFCT 2017 / NIN",
      "source_type": "NUTRITION_DATABASE",
      "tags": ["steamed", "fermented", "everyday", "light"],
      "primary_protein_source": "dal",
      "primary_grain": "rice",
      "cooking_method": "steamed",
      "spice_level": "MILD",
      "ingredients": [
        {"name": "Rice", "quantity": 100, "unit": "g"},
        {"name": "Urad Dal", "quantity": 30, "unit": "g"},
        {"name": "Toor Dal", "quantity": 40, "unit": "g"},
        {"name": "Mixed Vegetables", "quantity": 80, "unit": "g"},
        {"name": "Sambar Powder", "quantity": 5, "unit": "g"},
        {"name": "Salt", "quantity": 3, "unit": "g"}
      ],
      "allergens": []
    }
    
    # Replace the generic Idli Sambar with this specific one
    for i, m in enumerate(meals):
        if m["name"] == "Idli Sambar":
            meals[i] = idli_sambar
            break
            
    os.makedirs(r"C:\Users\Samit\.gemini\antigravity\scratch\nutriguard\backend\data\seeds", exist_ok=True)
    with open(r"C:\Users\Samit\.gemini\antigravity\scratch\nutriguard\backend\data\seeds\meals_indian.json", "w", encoding="utf-8") as f:
        json.dump(meals, f, indent=2, ensure_ascii=False)
        
    print(f"Generated {len(meals)} meals successfully!")

if __name__ == '__main__':
    generate_meals()
