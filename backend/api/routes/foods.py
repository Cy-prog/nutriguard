from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from api.deps import get_db, get_current_user, get_current_admin
from models.user import User
from models.food import Food, FoodNutrition, Nutrient, Allergen, FoodAllergen, FoodServingSize

router = APIRouter()

class FoodCreateRequest(BaseModel):
    name: str
    category: str
    subcategory: Optional[str] = None
    aliases: List[str] = []
    cuisine_origin: List[str] = ["Indian"]
    description: Optional[str] = None
    is_vegetarian: bool = True
    is_vegan: bool = False
    is_jain: bool = False
    is_gluten_free: bool = False
    is_lactose_free: bool = False
    glycemic_index: Optional[int] = None
    purine_level: Optional[str] = None
    vitamin_k_mcg: Optional[float] = None
    nutrient_source: Optional[str] = "ICMR_NIN"
    nutrients: Optional[List[Dict[str, Any]]] = []

@router.get("/")
def list_foods(
    search: Optional[str] = None,
    category: Optional[str] = None,
    cuisine: Optional[str] = None,
    is_veg: Optional[bool] = None,
    is_vegan: Optional[bool] = None,
    is_jain: Optional[bool] = None,
    is_gluten_free: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Food).filter(Food.is_active == True)
    
    if category and category.lower() != "all":
        query = query.filter(Food.category.ilike(f"%{category}%"))
    if is_veg is not None:
        query = query.filter(Food.is_vegetarian == is_veg)
    if is_vegan is not None:
        query = query.filter(Food.is_vegan == is_vegan)
    if is_jain is not None:
        query = query.filter(Food.is_jain == is_jain)
    if is_gluten_free is not None:
        query = query.filter(Food.is_gluten_free == is_gluten_free)
        
    if search:
        s = f"%{search}%"
        query = query.filter(or_(
            Food.name.ilike(s),
            Food.description.ilike(s),
            Food.subcategory.ilike(s)
        ))
        
    total = query.count()
    foods = query.offset((page - 1) * page_size).limit(page_size).all()
    
    result = []
    for f in foods:
        nutr_entries = db.query(FoodNutrition, Nutrient).join(
            Nutrient, FoodNutrition.nutrient_id == Nutrient.nutrient_id
        ).filter(FoodNutrition.food_id == f.food_id).all()
        
        nutrients_list = [
            {
                "name": n.name,
                "amount": float(fn.amount),
                "unit": fn.unit,
                "per_quantity": float(fn.per_quantity or 100),
                "per_unit": fn.per_unit or "g"
            }
            for fn, n in nutr_entries
        ]
        
        result.append({
            "food_id": str(f.food_id),
            "id": str(f.food_id),
            "name": f.name,
            "aliases": f.aliases or [],
            "category": f.category,
            "subcategory": f.subcategory,
            "description": f.description,
            "cuisine_origin": f.cuisine_origin or ["Indian"],
            "is_vegetarian": f.is_vegetarian,
            "is_vegan": f.is_vegan,
            "is_jain": f.is_jain,
            "is_gluten_free": f.is_gluten_free,
            "glycemic_index": f.glycemic_index,
            "purine_level": f.purine_level,
            "vitamin_k_mcg": float(f.vitamin_k_mcg) if f.vitamin_k_mcg is not None else None,
            "nutrient_source": f.nutrient_source or "ICMR_NIN",
            "nutrients": nutrients_list
        })
        
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "foods": result
    }

@router.get("/substitutions")
def get_food_substitutions(
    food: str = Query(..., description="Food name or query to find smart substitutions for"),
    db: Session = Depends(get_db)
):
    food_query = food.strip().lower()
    
    # Pre-calibrated high-utility Indian food substitution mapping
    KNOWLEDGE_SUBSTITUTIONS = {
        "paneer": [
            {"name": "Organic Tofu", "reason": "High protein, lower saturated fat, dairy-free & lactose-safe", "cuisine": "Pan-Indian / Indo-Chinese", "macro_profile": "High Protein, Low Carb"},
            {"name": "Hung Curd / Greek Yogurt", "reason": "Probiotic-rich dairy protein alternative with lower whey lactose", "cuisine": "North & West Indian", "macro_profile": "High Protein, Moderate Fat"},
            {"name": "Boiled Chickpeas (Kabuli Chana)", "reason": "Plant-based high fiber protein alternative", "cuisine": "North Indian", "macro_profile": "High Fiber, Moderate Protein"},
            {"name": "Nutrela Soya Chunks", "reason": "Dense vegetarian protein alternative (52g protein per 100g)", "cuisine": "Pan-Indian", "macro_profile": "Very High Protein"}
        ],
        "white rice": [
            {"name": "Brown Rice", "reason": "Higher dietary fiber and lower glycemic load", "cuisine": "Pan-Indian", "macro_profile": "High Fiber, Complex Carbs"},
            {"name": "Foxtail Millet (Kangni)", "reason": "Ancient grain with low glycemic index (GI < 55) for glycemic stability", "cuisine": "South & Central Indian", "macro_profile": "Low GI, High Micronutrients"},
            {"name": "Quinoa", "reason": "Complete protein grain with all 9 essential amino acids", "cuisine": "Modern Indian Fusion", "macro_profile": "High Protein, Gluten-Free"},
            {"name": "Cauliflower Rice", "reason": "Ultra-low calorie, low-carb keto-friendly grain alternative", "cuisine": "Modern Wellness", "macro_profile": "Very Low Calorie"}
        ],
        "milk": [
            {"name": "Unsweetened Soy Milk", "reason": "Comparable protein content (7g/cup) with zero lactose and zero cholesterol", "cuisine": "Pan-Indian", "macro_profile": "High Protein, Lactose-Free"},
            {"name": "Almond Milk", "reason": "Light, low-calorie alternative rich in Vitamin E", "cuisine": "Pan-Indian", "macro_profile": "Low Calorie, Dairy-Free"},
            {"name": "Oat Milk", "reason": "Creamy texture ideal for Indian tea and spiced golden milk", "cuisine": "Modern Indian", "macro_profile": "High Fiber, Naturally Sweet"}
        ],
        "wheat roti": [
            {"name": "Jowar Roti (Sorghum)", "reason": "Naturally gluten-free, rich in iron, zinc, and resistant starch", "cuisine": "Maharashtrian / Central Indian", "macro_profile": "Gluten-Free, High Fiber"},
            {"name": "Bajra Roti (Pearl Millet)", "reason": "Warming winter millet high in magnesium and iron", "cuisine": "Rajasthani / Gujarati", "macro_profile": "High Energy, High Iron"},
            {"name": "Ragi Roti (Finger Millet)", "reason": "Highest calcium grain in Indian agriculture (344mg/100g)", "cuisine": "South Indian / Karnataka", "macro_profile": "High Calcium, Low GI"}
        ]
    }
    
    # Check knowledge base
    matched_key = next((k for k in KNOWLEDGE_SUBSTITUTIONS if k in food_query or food_query in k), None)
    if matched_key:
        return {
            "query": food,
            "target_food": matched_key.title(),
            "substitutions": KNOWLEDGE_SUBSTITUTIONS[matched_key],
            "source": "ICMR-NIN & NutriGuard Clinical Rules"
        }
        
    # Database category fallback
    matched_food = db.query(Food).filter(
        or_(Food.name.ilike(f"%{food_query}%"), Food.category.ilike(f"%{food_query}%"))
    ).first()
    
    if matched_food:
        alts = db.query(Food).filter(
            Food.category == matched_food.category,
            Food.food_id != matched_food.food_id
        ).limit(4).all()
        
        subs = [
            {
                "name": a.name,
                "reason": f"Same nutritional category ({a.category}) with comparable Indian culinary use.",
                "cuisine": "Indian",
                "macro_profile": "Balanced"
            }
            for a in alts
        ]
        return {
            "query": food,
            "target_food": matched_food.name,
            "substitutions": subs,
            "source": "NutriGuard Composition Engine"
        }
        
    return {
        "query": food,
        "target_food": food,
        "substitutions": [
            {"name": "Moong Dal Sprouts", "reason": "Universal high-protein clean nutrition substitute", "cuisine": "Pan-Indian", "macro_profile": "High Protein, High Enzymes"},
            {"name": "Roasted Chana", "reason": "Convenient high-fiber snack staple with low glycemic index", "cuisine": "Pan-Indian", "macro_profile": "High Fiber, Low GI"}
        ],
        "source": "NutriGuard General Guidance"
    }

@router.get("/{food_id}")
def get_food(food_id: str, db: Session = Depends(get_db)):
    try:
        f_uuid = UUID(food_id)
        food = db.query(Food).filter(Food.food_id == f_uuid).first()
    except ValueError:
        food = db.query(Food).filter(Food.name.ilike(food_id)).first()
        
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")
        
    nutr_entries = db.query(FoodNutrition, Nutrient).join(
        Nutrient, FoodNutrition.nutrient_id == Nutrient.nutrient_id
    ).filter(FoodNutrition.food_id == food.food_id).all()
    
    servings = db.query(FoodServingSize).filter(FoodServingSize.food_id == food.food_id).all()
    allergens = db.query(FoodAllergen, Allergen).join(
        Allergen, FoodAllergen.allergen_id == Allergen.allergen_id
    ).filter(FoodAllergen.food_id == food.food_id).all()
    
    return {
        "food_id": str(food.food_id),
        "name": food.name,
        "aliases": food.aliases or [],
        "category": food.category,
        "subcategory": food.subcategory,
        "cuisine_origin": food.cuisine_origin or ["Indian"],
        "description": food.description,
        "is_vegetarian": food.is_vegetarian,
        "is_vegan": food.is_vegan,
        "is_jain": food.is_jain,
        "is_gluten_free": food.is_gluten_free,
        "is_lactose_free": food.is_lactose_free,
        "glycemic_index": food.glycemic_index,
        "purine_level": food.purine_level,
        "vitamin_k_mcg": float(food.vitamin_k_mcg) if food.vitamin_k_mcg is not None else None,
        "nutrient_source": food.nutrient_source or "ICMR_NIN",
        "nutrients": [
            {
                "name": n.name,
                "amount": float(fn.amount),
                "unit": fn.unit,
                "per_quantity": float(fn.per_quantity or 100),
                "per_unit": fn.per_unit or "g"
            }
            for fn, n in nutr_entries
        ],
        "serving_sizes": [
            {
                "description": s.description,
                "amount_g": float(s.amount_g),
                "is_default": s.is_default
            }
            for s in servings
        ] or [
            {"description": "1 Standard Katori (Cooked)", "amount_g": 150.0, "is_default": True},
            {"description": "1 Medium Serving / Piece", "amount_g": 100.0, "is_default": False}
        ],
        "allergens": [a.name for _, a in allergens]
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_food(
    food_in: FoodCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    existing = db.query(Food).filter(Food.name.ilike(food_in.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Food item with this name already exists.")
        
    new_food = Food(
        name=food_in.name,
        category=food_in.category,
        subcategory=food_in.subcategory,
        aliases=food_in.aliases,
        cuisine_origin=food_in.cuisine_origin,
        description=food_in.description,
        is_vegetarian=food_in.is_vegetarian,
        is_vegan=food_in.is_vegan,
        is_jain=food_in.is_jain,
        is_gluten_free=food_in.is_gluten_free,
        is_lactose_free=food_in.is_lactose_free,
        glycemic_index=food_in.glycemic_index,
        purine_level=food_in.purine_level,
        vitamin_k_mcg=food_in.vitamin_k_mcg,
        nutrient_source=food_in.nutrient_source or "ICMR_NIN"
    )
    db.add(new_food)
    db.flush()
    
    # Process nutrients
    for n in food_in.nutrients:
        nutrient = db.query(Nutrient).filter_by(name=n["name"]).first()
        if not nutrient:
            nutrient = Nutrient(name=n["name"], unit=n.get("unit", "g"))
            db.add(nutrient)
            db.flush()
            
        fn = FoodNutrition(
            food_id=new_food.food_id,
            nutrient_id=nutrient.nutrient_id,
            amount=n.get("amount", 0.0),
            unit=n.get("unit", "g"),
            per_quantity=n.get("per_quantity", 100),
            per_unit=n.get("per_unit", "g")
        )
        db.add(fn)
        
    db.commit()
    db.refresh(new_food)
    return {"message": "Food created successfully", "food_id": str(new_food.food_id), "name": new_food.name}
