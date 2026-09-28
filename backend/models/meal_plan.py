import uuid
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, DateTime, JSON, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base

class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    plan_date = Column(Date, nullable=False, default=date.today)
    plan_type = Column(String, default="single_day")
    is_ai_generated = Column(Boolean, default=False)
    safety_validated = Column(Boolean, default=False)
    targets_snapshot = Column(JSON)    # NutrientTargets at generation time
    gap_report = Column(JSON)          # NutrientGapReport
    created_at = Column(DateTime(timezone=True), default=func.now())

    meals = relationship("MealPlanMeal", back_populates="plan", cascade="all, delete-orphan")
    user = relationship("User", back_populates="meal_plans")

class MealPlanMeal(Base):
    __tablename__ = "meal_plan_meals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_plans.id", ondelete="CASCADE"), nullable=False)
    meal_type = Column(String, nullable=False)
    day_number = Column(Integer, default=1)
    foods = Column(JSON, nullable=False)
    total_nutrition = Column(JSON)
    rationale = Column(JSON)

    plan = relationship("MealPlan", back_populates="meals")


class DailyMealPlan(Base):
    __tablename__ = 'daily_meal_plans'
    
    plan_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    date = Column(Date, nullable=False)
    
    # Targets for the day
    target_calories = Column(Numeric(7, 1))
    target_protein_g = Column(Numeric(6, 1))
    target_carbs_g = Column(Numeric(6, 1))
    target_fat_g = Column(Numeric(6, 1))
    target_fiber_g = Column(Numeric(6, 1))
    
    # Actual totals (computed from items)
    actual_calories = Column(Numeric(7, 1))
    actual_protein_g = Column(Numeric(6, 1))
    actual_carbs_g = Column(Numeric(6, 1))
    actual_fat_g = Column(Numeric(6, 1))
    actual_fiber_g = Column(Numeric(6, 1))
    
    # Plan quality scores (0-100)
    nutrition_score = Column(Numeric(5, 1))
    variety_score = Column(Numeric(5, 1))
    preference_score = Column(Numeric(5, 1))
    overall_score = Column(Numeric(5, 1))
    
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    items = relationship("DailyMealPlanItem", back_populates="plan", cascade="all, delete-orphan")


class DailyMealPlanItem(Base):
    __tablename__ = 'daily_meal_plan_items'
    
    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plan_id = Column(UUID(as_uuid=True), ForeignKey('daily_meal_plans.plan_id', ondelete='CASCADE'), nullable=False)
    meal_id = Column(UUID(as_uuid=True), ForeignKey('meals.meal_id'), nullable=False)
    
    meal_type = Column(String, nullable=False)  # BREAKFAST, LUNCH, DINNER
    servings = Column(Numeric(4, 2), default=1.0)
    portion_multiplier = Column(Numeric(4, 2), default=1.0)
    
    # Computed nutrition for this item (meal nutrition * portion_multiplier)
    calories = Column(Numeric(7, 1))
    protein_g = Column(Numeric(6, 1))
    carbs_g = Column(Numeric(6, 1))
    fat_g = Column(Numeric(6, 1))
    fiber_g = Column(Numeric(6, 1))
    
    # Recommendation metadata
    recommendation_score = Column(Numeric(5, 1))
    recommendation_reasons = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Relationships
    plan = relationship("DailyMealPlan", back_populates="items")
    meal = relationship("Meal")
