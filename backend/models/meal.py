from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class Meal(Base):
    __tablename__ = 'meals'
    
    meal_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    local_name = Column(String)
    description = Column(Text)
    
    meal_type = Column(String, nullable=False)  # BREAKFAST, LUNCH, DINNER, SNACK
    cuisine_region = Column(String)  # NORTH_INDIAN, SOUTH_INDIAN, WEST_INDIAN, EAST_INDIAN, CENTRAL_INDIAN, PAN_INDIAN
    food_type = Column(String)  # MAIN, SIDE, COMBO
    
    is_vegetarian = Column(Boolean, default=True)
    is_vegan = Column(Boolean, default=False)
    is_jain_friendly = Column(Boolean, default=False)
    is_egg_based = Column(Boolean, default=False)
    
    preparation_time_minutes = Column(Integer)
    difficulty = Column(String)  # EASY, MEDIUM, HARD
    serving_size_g = Column(Numeric(7, 1))
    serving_description = Column(String)  # e.g. "1 bowl (250g)", "2 rotis + 1 katori dal"
    
    # Macronutrients per serving
    calories = Column(Numeric(7, 1))
    protein_g = Column(Numeric(6, 1))
    carbohydrates_g = Column(Numeric(6, 1))
    fat_g = Column(Numeric(6, 1))
    fiber_g = Column(Numeric(6, 1))
    sugar_g = Column(Numeric(6, 1))
    
    # Micronutrients per serving
    sodium_mg = Column(Numeric(7, 1))
    calcium_mg = Column(Numeric(7, 1))
    iron_mg = Column(Numeric(6, 1))
    potassium_mg = Column(Numeric(7, 1))
    vitamin_a_mcg = Column(Numeric(7, 1))
    vitamin_c_mg = Column(Numeric(6, 1))
    vitamin_d_mcg = Column(Numeric(6, 1))
    vitamin_b12_mcg = Column(Numeric(6, 2))
    folate_mcg = Column(Numeric(7, 1))
    
    # Recipe
    recipe_text = Column(Text)
    preparation_steps = Column(JSON, default=list)  # ["Step 1...", "Step 2..."]
    
    # Media & Sources
    image_url = Column(String)
    video_url = Column(String)
    source_url = Column(String)
    source_name = Column(String)
    source_type = Column(String)  # NUTRITION_DATABASE, GOVERNMENT_SOURCE, DIETITIAN, RECIPE_SOURCE, CURATED_ADMIN
    
    # Metadata
    tags = Column(JSON, default=list)  # ["high_protein", "quick", "comfort_food", "everyday"]
    primary_protein_source = Column(String)  # dal, paneer, egg, chicken, rajma, chole, etc.
    primary_grain = Column(String)  # rice, roti, dosa, idli, etc.
    cooking_method = Column(String)  # steamed, fried, baked, boiled, sauteed, raw
    spice_level = Column(String)  # MILD, MEDIUM, SPICY
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    ingredients = relationship("MealIngredient", back_populates="meal", cascade="all, delete-orphan")
    allergens = relationship("MealAllergen", back_populates="meal", cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    ingredient_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    local_name = Column(String)
    category = Column(String)  # grain, legume, vegetable, fruit, dairy, spice, oil, nut, meat, egg
    
    # Link to existing Food model for safety checks
    food_id = Column(UUID(as_uuid=True), ForeignKey('foods.food_id'))
    
    # Dietary flags
    is_vegetarian = Column(Boolean, default=True)
    is_vegan = Column(Boolean, default=False)
    is_jain_friendly = Column(Boolean, default=False)
    
    # Nutrition per 100g
    calories_per_100g = Column(Numeric(7, 1))
    protein_per_100g = Column(Numeric(6, 1))
    carbs_per_100g = Column(Numeric(6, 1))
    fat_per_100g = Column(Numeric(6, 1))
    fiber_per_100g = Column(Numeric(6, 1))
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)


class MealIngredient(Base):
    __tablename__ = 'meal_ingredients'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_id = Column(UUID(as_uuid=True), ForeignKey('meals.meal_id', ondelete='CASCADE'), nullable=False)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey('ingredients.ingredient_id'), nullable=False)
    
    quantity = Column(Numeric(7, 1))
    unit = Column(String)  # g, ml, cup, tbsp, tsp, piece, katori
    is_optional = Column(Boolean, default=False)
    notes = Column(String)
    
    # Relationships
    meal = relationship("Meal", back_populates="ingredients")
    ingredient = relationship("Ingredient")


class MealAllergen(Base):
    __tablename__ = 'meal_allergens'
    
    meal_id = Column(UUID(as_uuid=True), ForeignKey('meals.meal_id', ondelete='CASCADE'), primary_key=True)
    allergen_id = Column(UUID(as_uuid=True), ForeignKey('allergies.allergen_id'), primary_key=True)
    is_primary = Column(Boolean, default=True)
    is_trace = Column(Boolean, default=False)
    
    # Relationships
    meal = relationship("Meal", back_populates="allergens")
    allergen = relationship("Allergen")
