"""Add meal planning models

Revision ID: a7b2c3d4e5f6
Revises: 1efabd3beb36
Create Date: 2026-08-23 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '1efabd3beb36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add meal planning tables and user profile meal fields."""
    
    # Add new columns to user_profiles
    op.add_column('user_profiles', sa.Column('fitness_goal', sa.String(), nullable=True))
    op.add_column('user_profiles', sa.Column('diet_type', sa.String(), nullable=True))
    op.add_column('user_profiles', sa.Column('regional_preference', sa.String(), nullable=True))
    op.add_column('user_profiles', sa.Column('favorite_foods', sa.JSON(), nullable=True))
    op.add_column('user_profiles', sa.Column('disliked_foods', sa.JSON(), nullable=True))
    op.add_column('user_profiles', sa.Column('preferred_meal_spice_level', sa.String(), nullable=True))
    op.add_column('user_profiles', sa.Column('preferred_cuisine', sa.String(), nullable=True))
    op.add_column('user_profiles', sa.Column('onboarding_completed', sa.Boolean(), nullable=True))
    
    # Create ingredients table
    op.create_table('ingredients',
        sa.Column('ingredient_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('local_name', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('food_id', sa.UUID(), nullable=True),
        sa.Column('is_vegetarian', sa.Boolean(), nullable=True),
        sa.Column('is_vegan', sa.Boolean(), nullable=True),
        sa.Column('is_jain_friendly', sa.Boolean(), nullable=True),
        sa.Column('calories_per_100g', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('protein_per_100g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('carbs_per_100g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fat_per_100g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fiber_per_100g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['food_id'], ['foods.food_id'], ),
        sa.PrimaryKeyConstraint('ingredient_id'),
        sa.UniqueConstraint('name')
    )
    
    # Create meals table
    op.create_table('meals',
        sa.Column('meal_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('local_name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('meal_type', sa.String(), nullable=False),
        sa.Column('cuisine_region', sa.String(), nullable=True),
        sa.Column('food_type', sa.String(), nullable=True),
        sa.Column('is_vegetarian', sa.Boolean(), nullable=True),
        sa.Column('is_vegan', sa.Boolean(), nullable=True),
        sa.Column('is_jain_friendly', sa.Boolean(), nullable=True),
        sa.Column('is_egg_based', sa.Boolean(), nullable=True),
        sa.Column('preparation_time_minutes', sa.Integer(), nullable=True),
        sa.Column('difficulty', sa.String(), nullable=True),
        sa.Column('serving_size_g', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('serving_description', sa.String(), nullable=True),
        sa.Column('calories', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('protein_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('carbohydrates_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fat_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fiber_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('sugar_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('sodium_mg', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('calcium_mg', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('iron_mg', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('potassium_mg', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('vitamin_a_mcg', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('vitamin_c_mg', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('vitamin_d_mcg', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('vitamin_b12_mcg', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('folate_mcg', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('recipe_text', sa.Text(), nullable=True),
        sa.Column('preparation_steps', sa.JSON(), nullable=True),
        sa.Column('image_url', sa.String(), nullable=True),
        sa.Column('video_url', sa.String(), nullable=True),
        sa.Column('source_url', sa.String(), nullable=True),
        sa.Column('source_name', sa.String(), nullable=True),
        sa.Column('source_type', sa.String(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('primary_protein_source', sa.String(), nullable=True),
        sa.Column('primary_grain', sa.String(), nullable=True),
        sa.Column('cooking_method', sa.String(), nullable=True),
        sa.Column('spice_level', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('meal_id')
    )
    
    # Create meal_ingredients table
    op.create_table('meal_ingredients',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('meal_id', sa.UUID(), nullable=False),
        sa.Column('ingredient_id', sa.UUID(), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('is_optional', sa.Boolean(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.ingredient_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create meal_allergens table
    op.create_table('meal_allergens',
        sa.Column('meal_id', sa.UUID(), nullable=False),
        sa.Column('allergen_id', sa.UUID(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('is_trace', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['allergen_id'], ['allergies.allergen_id'], ),
        sa.PrimaryKeyConstraint('meal_id', 'allergen_id')
    )
    
    # Create daily_meal_plans table
    op.create_table('daily_meal_plans',
        sa.Column('plan_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('target_calories', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('target_protein_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('target_carbs_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('target_fat_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('target_fiber_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('actual_calories', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('actual_protein_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('actual_carbs_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('actual_fat_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('actual_fiber_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('nutrition_score', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('variety_score', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('preference_score', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('overall_score', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('plan_id')
    )
    
    # Create daily_meal_plan_items table
    op.create_table('daily_meal_plan_items',
        sa.Column('item_id', sa.UUID(), nullable=False),
        sa.Column('plan_id', sa.UUID(), nullable=False),
        sa.Column('meal_id', sa.UUID(), nullable=False),
        sa.Column('meal_type', sa.String(), nullable=False),
        sa.Column('servings', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('portion_multiplier', sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column('calories', sa.Numeric(precision=7, scale=1), nullable=True),
        sa.Column('protein_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('carbs_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fat_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('fiber_g', sa.Numeric(precision=6, scale=1), nullable=True),
        sa.Column('recommendation_score', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('recommendation_reasons', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['daily_meal_plans.plan_id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['meal_id'], ['meals.meal_id'], ),
        sa.PrimaryKeyConstraint('item_id')
    )


def downgrade() -> None:
    """Remove meal planning tables and user profile meal fields."""
    op.drop_table('daily_meal_plan_items')
    op.drop_table('daily_meal_plans')
    op.drop_table('meal_allergens')
    op.drop_table('meal_ingredients')
    op.drop_table('meals')
    op.drop_table('ingredients')
    
    op.drop_column('user_profiles', 'onboarding_completed')
    op.drop_column('user_profiles', 'preferred_cuisine')
    op.drop_column('user_profiles', 'preferred_meal_spice_level')
    op.drop_column('user_profiles', 'disliked_foods')
    op.drop_column('user_profiles', 'favorite_foods')
    op.drop_column('user_profiles', 'regional_preference')
    op.drop_column('user_profiles', 'diet_type')
    op.drop_column('user_profiles', 'fitness_goal')
