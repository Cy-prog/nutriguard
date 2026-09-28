from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.deps import get_db, get_current_clinical_reviewer, get_current_admin
from models.user import User
from services.recommendation_service import RecommendationService
from models.rule import Rule
from models.evidence import Evidence, DataSource
from models.condition import Condition
from models.food import Food

router = APIRouter()

class SimulationRequest(BaseModel):
    user_context: Dict[str, Any]
    food_id: str

@router.post("/rules/simulate")
async def simulate_rules(
    request: SimulationRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_clinical_reviewer)
):
    try:
        food_uuid = UUID(request.food_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid food_id UUID format")
        
    service = RecommendationService(db)
    det_results = await service.generate_recommendations(request.user_context, [food_uuid])
    
    if not det_results or not det_results.get('foods'):
        raise HTTPException(status_code=404, detail="Food not found or evaluation failed")
        
    res = det_results['foods'][0]
    
    trace = {
        "food": res.get("food_name", request.food_id),
        "safety": {"status": "FAIL" if res.get("classification") in ["blocked_allergy", "blocked_interaction", "avoid"] else "PASS"},
        "allergy": {"status": "FAIL" if res.get("classification") == "blocked_allergy" else "PASS"},
        "interactions": [r for r in res.get("fired_rules", []) if "interaction" in str(r).lower()],
        "rules_evaluated": ["(All active rules)"],
        "rules_triggered": res.get("fired_rules", []),
        "scores": {"final_score": res.get("score", 0)},
        "final_classification": res.get("classification"),
        "rule_versions": ["v1"],
        "evidence": ["EVIDENCE_PLACEHOLDER"]
    }
    
    return trace

@router.get("/rules")
def list_rules(db: Session = Depends(get_db), current_user: User = Depends(get_current_clinical_reviewer)):
    rules = db.query(Rule).all()
    return rules

@router.post("/rules/{rule_id}/approve")
def approve_rule(rule_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_clinical_reviewer)):
    rule = db.query(Rule).filter(Rule.rule_id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    rule.status = "APPROVED"
    rule.approved_by_user_id = current_user.user_id
    
    from models.audit import AuditLog
    import uuid
    log = AuditLog(
        actor_user_id=current_user.user_id,
        action="RULE_APPROVED",
        entity_type="Rule",
        entity_id=str(rule.rule_id),
        entity_version=rule.version,
        request_id=str(uuid.uuid4())
    )
    db.add(log)
    db.commit()
    return {"status": "success", "rule_id": rule_id}


@router.get("/stats")
def get_admin_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    from models.meal import Meal
    from models.medication import Medication
    total_users = db.query(User).count()
    total_meals = db.query(Meal).filter(Meal.is_active == True).count()
    total_foods = db.query(Food).filter(Food.is_active == True).count()
    total_conditions = db.query(Condition).count()
    total_medications = db.query(Medication).count()
    total_rules = db.query(Rule).count()

    return {
        "total_users": total_users,
        "total_meals": total_meals,
        "total_foods": total_foods,
        "total_conditions": total_conditions,
        "total_medications": total_medications,
        "total_rules": total_rules,
        "system_status": "OPERATIONAL",
        "version": "2.0.0"
    }


@router.get("/data-sources")
def get_data_sources(db: Session = Depends(get_db), current_user: User = Depends(get_current_clinical_reviewer)):
    sources = [
        {
            "id": "ifct-2017",
            "name": "Indian Food Composition Tables (IFCT)",
            "institution": "National Institute of Nutrition (ICMR-NIN)",
            "version": "2017",
            "url": "https://www.nin.res.in/downloads/IFCT2017.pdf",
            "license": "Government of India / ICMR Educational & Research License",
            "attribution": "Longvah T, Ananthan R, Bhaskarachary K, Venkaiah K. Indian Food Composition Tables. National Institute of Nutrition, ICMR, Hyderabad, 2017.",
            "usage": "Primary authoritative composition for raw Indian crops, cereals, pulses, vegetables, and spices.",
            "status": "ACTIVE"
        },
        {
            "id": "usda-fdc",
            "name": "USDA FoodData Central",
            "institution": "U.S. Department of Agriculture, Agricultural Research Service",
            "version": "2024",
            "url": "https://fdc.nal.usda.gov/",
            "license": "U.S. Public Domain",
            "attribution": "U.S. Department of Agriculture, Agricultural Research Service. FoodData Central, 2024. fdc.nal.usda.gov.",
            "usage": "Supplementary micronutrient profiles (Vitamin K, trace minerals, amino acids).",
            "status": "ACTIVE"
        },
        {
            "id": "open-food-facts",
            "name": "Open Food Facts",
            "institution": "Open Food Facts Association",
            "version": "World / IN Database",
            "url": "https://world.openfoodfacts.org/",
            "license": "Open Database License (ODbL) / Database Contents License (DbCL)",
            "attribution": "Open Food Facts contributors, openfoodfacts.org",
            "usage": "Packaged Indian food barcodes and nutritional panel metadata.",
            "status": "ACTIVE"
        },
        {
            "id": "icmr-dgi-2024",
            "name": "ICMR Dietary Guidelines for Indians & Recommended Dietary Allowances",
            "institution": "Indian Council of Medical Research - National Institute of Nutrition",
            "version": "2024 / 2020",
            "url": "https://www.nin.res.in/",
            "license": "Government of India Public Nutrition Standard",
            "attribution": "ICMR-NIN Expert Committee on Nutrient Requirements for Indians, 2020/2024.",
            "usage": "Reference Daily Intakes (RDAs), Estimated Average Requirements (EAR), and Upper Tolerable Levels (TUL).",
            "status": "ACTIVE"
        }
    ]
    return sources

