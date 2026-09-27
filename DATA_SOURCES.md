# NutriGuard Data Sources, Attributions & Compliance

NutriGuard is engineered around authoritative, scientifically verified nutritional datasets. Nutritional figures and clinical interactions are **never fabricated or synthesized** by generative models.

This document details the primary institutions, publications, licenses, and specific usage of all nutritional and clinical datasets integrated into the platform.

---

## 1. Indian Food Composition Tables (IFCT 2017)

| Attribute | Details |
|---|---|
| **Authoritative Body** | National Institute of Nutrition (NIN), Indian Council of Medical Research (ICMR), Department of Health Research, Ministry of Health and Family Welfare, Government of India |
| **Authors** | T. Longvah, R. Ananthan, K. Bhaskarachary, and K. Venkaiah |
| **Publication Year** | 2017 |
| **Official URI** | [https://www.nin.res.in/downloads/IFCT2017.pdf](https://www.nin.res.in/downloads/IFCT2017.pdf) |
| **Coverage** | 528 key Indian raw foods across 151 nutritional parameters analyzed via modern analytical methods (ICP-MS, HPLC, GC-MS) |
| **NutriGuard Usage** | Primary dataset for raw Indian agricultural crops: cereals (wheat, rice, jowar, bajra, ragi), pulses (moong, chana, urad, toor, rajma), green leafy vegetables (palak, methi, sarson), dairy (paneer, dahi, cow/buffalo milk), and regional spices (turmeric, jeera, hing, dhania). |
| **Citation** | *Longvah T, Ananthan R, Bhaskarachary K, Venkaiah K. (2017). Indian Food Composition Tables. National Institute of Nutrition, Indian Council of Medical Research, Hyderabad, India.* |

---

## 2. ICMR Dietary Guidelines for Indians & Recommended Dietary Allowances (RDA 2020 / 2024)

| Attribute | Details |
|---|---|
| **Authoritative Body** | ICMR - National Institute of Nutrition Expert Committee on Nutrient Requirements for Indians |
| **Publication Years** | 2020 (Nutrient Requirements & RDA) & 2024 (Dietary Guidelines for Indians) |
| **Official URI** | [https://www.nin.res.in/](https://www.nin.res.in/) |
| **Coverage** | Reference body weights (65 kg adult male, 55 kg adult female), Estimated Average Requirements (EAR), Recommended Dietary Allowances (RDA), and Tolerable Upper Limits (TUL) for Indians across age brackets, physiological stages (pregnancy, lactation), and activity tiers. |
| **NutriGuard Usage** | Mathematical targets for daily macronutrient distribution (Carbohydrates 50–60%, Protein 0.83–1.0 g/kg body weight, Fats 20–25% of energy), micronutrient thresholds (Iron, Calcium, Vitamin D, Vitamin C, Vitamin B12, Folate), and cooking oil balance recommendations. |
| **Citation** | *ICMR-NIN. (2020). Nutrient Requirements for Indians - Recommended Dietary Allowances and Estimated Average Requirements. A Report of the Expert Group. National Institute of Nutrition, Hyderabad.* |

---

## 3. USDA FoodData Central (FDC)

| Attribute | Details |
|---|---|
| **Authoritative Body** | U.S. Department of Agriculture (USDA), Agricultural Research Service (ARS) |
| **Release Version** | FoodData Central (2024 Edition) |
| **Official URI** | [https://fdc.nal.usda.gov/](https://fdc.nal.usda.gov/) |
| **License** | U.S. Public Domain (17 U.S.C. § 105) |
| **NutriGuard Usage** | Supplementary micronutrient data where regional data requires cross-validation, specifically phylloquinone (Vitamin K1) mcg concentrations for anticoagulant safety and specialized trace amino acid profiles. |
| **Citation** | *U.S. Department of Agriculture, Agricultural Research Service. (2024). FoodData Central. fdc.nal.usda.gov.* |

---

## 4. Open Food Facts (India / Global Database)

| Attribute | Details |
|---|---|
| **Organization** | Open Food Facts Association (Non-profit) |
| **Database** | Open Food Facts - India (IN) Dataset |
| **Official URI** | [https://world.openfoodfacts.org/](https://world.openfoodfacts.org/) |
| **License** | Open Database License (ODbL) v1.0 / Database Contents License (DbCL) |
| **NutriGuard Usage** | Standardized packaged grocery item barcodes, ingredient declaration parsing, and commercial Indian nutritional label cross-referencing. |
| **Attribution** | *Open Food Facts contributors, openfoodfacts.org.* |

---

## 5. Clinical Pharmacology & Drug-Nutrient Rules

NutriGuard's clinical safety rules derive from published clinical pharmacology guidelines:
- **FDA Prescribing Information**: Warfarin sodium labeling regarding dietary phylloquinone stability.
- **National Kidney Foundation (NKF KDOQI Guidelines)**: Stage 3–5 Chronic Kidney Disease dietary potassium and protein management.
- **American Diabetes Association (ADA) / Research Society for the Study of Diabetes in India (RSSDI)**: Glycemic index classification and carbohydrate quality recommendations.
- **American College of Rheumatology (ACR)**: Gout management and dietary purine restriction thresholds.

---

## 6. Seed Data Integrity & Verification Process

1. **Deterministic Seeding**: Seed files reside in `backend/data/seeds/` (`foods_indian.json`, `medications.json`, `conditions.json`, `meals_indian.json`).
2. **Idempotence**: `migrate_and_seed.py` evaluates primary keys and entity aliases prior to insertion; repeated runs produce zero duplicate entries or index corruption.
3. **Continuous Validation**: Automated Pytest regression suites (`tests/regression/test_meal_pipeline.py`) continuously assert that nutrient totals computed from raw food constituents match verified composite values within a $\pm 3\%$ margin of error.
