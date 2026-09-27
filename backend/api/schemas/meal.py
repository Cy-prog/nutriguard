from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime, date
from decimal import Decimal


# ─── Profile Schemas ────────────────────────────────────────────

class ProfileUpdate(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120)
    sex: Optional[str] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=20, le=500)
    activity_level: Optional[str] = None
    dietary_pattern: Optional[str] = None
    fitness_goal: Optional[str] = None
    diet_type: Optional[str] = None
    regional_preference: Optional[str] = None
    favorite_foods: Optional[List[str]] = None
    disliked_foods: Optional[List[str]] = None
    preferred_meal_spice_level: Optional[str] = None
    preferred_cuisine: Optional[str] = None
    nutritional_goals: Optional[List[str]] = None
    cuisine_preferences: Optional[List[str]] = None
    cooking_time_max_minutes: Optional[int] = None
    budget_level: Optional[str] = None
    lifestyle_notes: Optional[str] = None
    onboarding_completed: Optional[bool] = None
    # Health data
    allergies: Optional[List[str]] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    medications: Optional[List[Dict[str, Any]]] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    profile_id: UUID
    user_id: UUID
    version: int
    is_current: bool
    age: Optional[int] = None
    sex: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    dietary_pattern: Optional[str] = None
    fitness_goal: Optional[str] = None
    diet_type: Optional[str] = None
    regional_preference: Optional[str] = None
    favorite_foods: List[str] = []
    disliked_foods: List[str] = []
    preferred_meal_spice_level: Optional[str] = None
    preferred_cuisine: Optional[str] = None
    nutritional_goals: List[str] = []
    cuisine_preferences: List[str] = []
    cooking_time_max_minutes: Optional[int] = None
    budget_level: Optional[str] = None
    lifestyle_notes: Optional[str] = None
    onboarding_completed: bool = False
    created_at: datetime


class NutritionTargetsResponse(BaseModel):
    bmi: float
    bmr: float
    tdee: float
    target_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    water_ml: float
    calcium_mg: float
    iron_mg: float
    vitamin_c_mg: float
    vitamin_d_mcg: float
    vitamin_b12_mcg: float
    folate_mcg: float
    meal_distribution: Dict[str, float]
    disclaimer: str
    # Aliases for UI flexibility
    daily_calories: Optional[float] = None
    daily_protein_g: Optional[float] = None
    daily_carbs_g: Optional[float] = None
    daily_fat_g: Optional[float] = None
    daily_fiber_g: Optional[float] = None


# ─── Meal Schemas ────────────────────────────────────────────

class MealIngredientResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    local_name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    is_optional: bool = False
    notes: Optional[str] = None


class MealSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    meal_id: UUID
    name: str
    local_name: Optional[str] = None
    description: Optional[str] = None
    meal_type: str
    cuisine_region: Optional[str] = None
    is_vegetarian: bool = True
    is_vegan: bool = False
    is_jain_friendly: bool = False
    preparation_time_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbohydrates_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    image_url: Optional[str] = None
    tags: List[str] = []
    spice_level: Optional[str] = None
    primary_protein_source: Optional[str] = None


class MealDetail(MealSummary):
    food_type: Optional[str] = None
    is_egg_based: bool = False
    serving_size_g: Optional[float] = None
    serving_description: Optional[str] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    calcium_mg: Optional[float] = None
    iron_mg: Optional[float] = None
    potassium_mg: Optional[float] = None
    vitamin_a_mcg: Optional[float] = None
    vitamin_c_mg: Optional[float] = None
    vitamin_d_mcg: Optional[float] = None
    vitamin_b12_mcg: Optional[float] = None
    folate_mcg: Optional[float] = None
    recipe_text: Optional[str] = None
    preparation_steps: List[str] = []
    video_url: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    primary_grain: Optional[str] = None
    cooking_method: Optional[str] = None
    ingredients: List[MealIngredientResponse] = []
    allergen_warnings: List[str] = []


class MealNutritionResponse(BaseModel):
    meal_id: UUID
    name: str
    serving_size_g: Optional[float] = None
    serving_description: Optional[str] = None
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbohydrates_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    calcium_mg: Optional[float] = None
    iron_mg: Optional[float] = None
    potassium_mg: Optional[float] = None
    vitamin_a_mcg: Optional[float] = None
    vitamin_c_mg: Optional[float] = None
    vitamin_d_mcg: Optional[float] = None
    vitamin_b12_mcg: Optional[float] = None
    folate_mcg: Optional[float] = None
    source_name: Optional[str] = None


class MealVideoResponse(BaseModel):
    meal_id: UUID
    name: str
    video_url: Optional[str] = None
    embed_url: Optional[str] = None
    available: bool = False


class MealListResponse(BaseModel):
    meals: List[MealSummary]
    total: int
    page: int
    page_size: int


# ─── Meal Plan Schemas ────────────────────────────────────────

class MealPlanItemResponse(BaseModel):
    meal_type: str
    meal: MealSummary
    portion_multiplier: float = 1.0
    servings: float = 1.0
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    recommendation_score: Optional[float] = None
    recommendation_reasons: List[str] = []


class DailyMealPlanResponse(BaseModel):
    plan_id: Optional[UUID] = None
    date: date
    target_calories: Optional[float] = None
    target_protein_g: Optional[float] = None
    target_carbs_g: Optional[float] = None
    target_fat_g: Optional[float] = None
    target_fiber_g: Optional[float] = None
    actual_calories: Optional[float] = None
    actual_protein_g: Optional[float] = None
    actual_carbs_g: Optional[float] = None
    actual_fat_g: Optional[float] = None
    actual_fiber_g: Optional[float] = None
    # Aliases for frontend flexibility
    total_calories: Optional[float] = None
    total_protein: Optional[float] = None
    total_carbs: Optional[float] = None
    total_fat: Optional[float] = None
    health_score: Optional[float] = None
    nutrition_score: Optional[float] = None
    variety_score: Optional[float] = None
    preference_score: Optional[float] = None
    overall_score: Optional[float] = None
    meals: List[MealPlanItemResponse] = []


class WeeklyMealPlanResponse(BaseModel):
    start_date: date
    end_date: date
    daily_plans: List[DailyMealPlanResponse]
    days: Optional[List[DailyMealPlanResponse]] = None
    weekly_nutrition_score: Optional[float] = None
    weekly_variety_score: Optional[float] = None


class MealPlanGenerateRequest(BaseModel):
    date: Optional[date] = None


class WeeklyPlanGenerateRequest(BaseModel):
    start_date: Optional[date] = None


class RandomizeMealRequest(BaseModel):
    exclude_meal_ids: List[UUID] = []


class ReplaceMealRequest(BaseModel):
    current_meal_id: Optional[UUID] = None
    count: int = Field(5, ge=1, le=10)


class ReplaceMealResponse(BaseModel):
    alternatives: List[MealPlanItemResponse]


class MealExplanationResponse(BaseModel):
    meal_id: UUID
    meal_name: str
    score: Optional[float] = None
    reasons: List[str] = []
    explanation: Optional[str] = None


# ─── Grocery Schemas ──────────────────────────────────────────

class GroceryItem(BaseModel):
    ingredient_name: str
    local_name: Optional[str] = None
    total_quantity: float
    unit: str
    category: Optional[str] = None


class GroceryListResponse(BaseModel):
    period: str  # "daily" or "weekly"
    date_range: str
    items: List[GroceryItem]
    total_items: int


# ─── Admin Meal Schemas ──────────────────────────────────────

class MealCreateRequest(BaseModel):
    name: str
    local_name: Optional[str] = None
    description: Optional[str] = None
    meal_type: str
    cuisine_region: Optional[str] = None
    food_type: Optional[str] = None
    is_vegetarian: bool = True
    is_vegan: bool = False
    is_jain_friendly: bool = False
    is_egg_based: bool = False
    preparation_time_minutes: Optional[int] = None
    difficulty: Optional[str] = None
    serving_size_g: Optional[float] = None
    serving_description: Optional[str] = None
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbohydrates_g: Optional[float] = None
    fat_g: Optional[float] = None
    fiber_g: Optional[float] = None
    sugar_g: Optional[float] = None
    sodium_mg: Optional[float] = None
    calcium_mg: Optional[float] = None
    iron_mg: Optional[float] = None
    potassium_mg: Optional[float] = None
    recipe_text: Optional[str] = None
    preparation_steps: List[str] = []
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    tags: List[str] = []
    primary_protein_source: Optional[str] = None
    primary_grain: Optional[str] = None
    cooking_method: Optional[str] = None
    spice_level: Optional[str] = None


class MealUpdateRequest(MealCreateRequest):
    pass
