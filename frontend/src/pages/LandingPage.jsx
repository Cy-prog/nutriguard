import React from 'react';
import { Link } from 'react-router-dom';
import { 
  ShieldCheck, 
  Utensils, 
  Sparkles, 
  HeartPulse, 
  Scale, 
  CheckCircle2, 
  ArrowRight,
  BookOpen,
  Wheat,
  Activity,
  Layers
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Navigation Bar */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-500/20">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-700 to-teal-600 bg-clip-text text-transparent">
                NutriGuard
              </span>
              <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
                Indian AI Nutrition
              </span>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <Link
              to="/login"
              className="text-sm font-semibold text-slate-700 hover:text-emerald-600 transition-colors"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-sm shadow-emerald-600/30 transition-all hover:scale-[1.02]"
            >
              Get Started Free
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
              <span>Backed by ICMR-NIN Indian Food Composition Tables (IFCT)</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 leading-[1.15]">
              AI Nutrition & Indian Meals,{' '}
              <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                Engineered for Health.
              </span>
            </h1>

            <p className="text-lg sm:text-xl text-slate-600 leading-relaxed">
              No generic western calorie counting. NutriGuard speaks Indian kitchens: rotis, katoris, dals, sabzis, and regional cuisines — with deterministic clinical safety against medications and medical conditions.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link
                to="/register"
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-lg shadow-emerald-600/30 transition-all hover:scale-[1.02]"
              >
                Build Your Indian Meal Plan
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
              <Link
                to="/login"
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 rounded-xl shadow-sm transition-all"
              >
                Explore Demo Dashboard
              </Link>
            </div>

            <div className="pt-8 flex flex-wrap items-center justify-center gap-8 text-xs text-slate-500 font-medium">
              <span className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-1.5" /> 100% Deterministic Nutrition Engine</span>
              <span className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-1.5" /> Medication-Food Interaction Guardrails</span>
              <span className="flex items-center"><CheckCircle2 className="w-4 h-4 text-emerald-500 mr-1.5" /> Household Measurements (Katori, Roti)</span>
            </div>
          </div>
        </div>
      </section>

      {/* Pillars Section */}
      <section className="py-16 bg-white border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-emerald-600 mb-2">Architected for India</h2>
            <h3 className="text-3xl font-extrabold text-slate-900">Why NutriGuard is Unlike Generic Diet Apps</h3>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-emerald-300 transition-all hover:shadow-md">
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-6">
                <Utensils className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-2">Authentic Indian Regional Cuisines</h4>
              <p className="text-slate-600 text-sm leading-relaxed">
                Spanning North, South, West, East, and Central India. Authentic preparations from Moong Dal Khichdi and Thepla to Sambar Rice, Idlis, Poha, Rajma, and Paneer Bhurji with regional spice and oil profiles.
              </p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-emerald-300 transition-all hover:shadow-md">
              <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-600 flex items-center justify-center mb-6">
                <HeartPulse className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-2">Clinical Medication & Condition Safety</h4>
              <p className="text-slate-600 text-sm leading-relaxed">
                Hard-coded deterministic safety vetoes. Prevents dangerous interactions such as Warfarin with high Vitamin K greens, restricts potassium for Stage 4+ CKD, flags Metformin B12 depletions, and blocks allergens.
              </p>
            </div>

            <div className="p-8 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-emerald-300 transition-all hover:shadow-md">
              <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center mb-6">
                <Scale className="w-6 h-6" />
              </div>
              <h4 className="text-xl font-bold text-slate-900 mb-2">Compositional Recipe Intelligence</h4>
              <p className="text-slate-600 text-sm leading-relaxed">
                Meals aren't static estimates. Every meal is calculated from raw ingredients, cooking methods, portion multipliers, and familiar household units (1 katori, 1 piece, 1 plate, 1 glass).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Showcase Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div className="space-y-6">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold">
                <Layers className="w-3.5 h-3.5" />
                <span>Deterministic Science + Generative Intelligence</span>
              </div>
              <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 leading-tight">
                AI that explains and personalizes — but never fabricates nutrition facts.
              </h3>
              <p className="text-slate-600 leading-relaxed">
                NutriGuard uses a hybrid AI architecture. While Gemini models help reason about preferences, substitutions, and natural language food questions, nutritional calculations are strictly governed by ICMR-NIN & USDA tables with verifiable mathematical equations.
              </p>

              <div className="space-y-4 pt-2">
                <div className="flex items-start space-x-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mt-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <h5 className="font-bold text-slate-900 text-sm">Smart Ingredient Substitutions</h5>
                    <p className="text-xs text-slate-500">Need to swap Paneer? NutriGuard suggests Tofu or Greek Yogurt with macro-matched portions and cuisine compatibility.</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mt-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <h5 className="font-bold text-slate-900 text-sm">Budget-Aware Meal Planning</h5>
                    <p className="text-xs text-slate-500">Prioritize nutrient-dense affordable staples from ₹100/day to ₹300+/day without compromising protein or micronutrients.</p>
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mt-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <h5 className="font-bold text-slate-900 text-sm">Aggregated Indian Grocery Lists</h5>
                    <p className="text-xs text-slate-500">Turn your 7-day meal plan into a neat consolidated shopping list with household quantities and estimated pantry costs.</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Visual Card Mockup */}
            <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-xl relative">
              <div className="flex items-center justify-between border-b pb-4 mb-6">
                <div>
                  <h4 className="font-bold text-slate-900 text-lg">Daily Nutrition Blueprint</h4>
                  <p className="text-xs text-slate-500">Mifflin-St Jeor TDEE target: 2,150 kcal</p>
                </div>
                <span className="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-bold rounded-full">
                  Health Score 94/100
                </span>
              </div>

              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-sm text-slate-800">Breakfast</span>
                    <span className="text-xs text-slate-500 font-medium">420 kcal • 14g Protein</span>
                  </div>
                  <p className="text-xs text-slate-600">Moong Dal Chilla (2 pcs) with Mint Chutney & 1 cup Masala Chai (skim milk)</p>
                  <div className="mt-2 flex gap-2">
                    <span className="text-[10px] px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded font-medium">High Fiber</span>
                    <span className="text-[10px] px-2 py-0.5 bg-blue-100 text-blue-800 rounded font-medium">Low GI</span>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-sm text-slate-800">Lunch</span>
                    <span className="text-xs text-slate-500 font-medium">680 kcal • 28g Protein</span>
                  </div>
                  <p className="text-xs text-slate-600">2 Phulkas + 1 katori Rajma Masala + 1 katori Cucumber Raita + Mixed Salad</p>
                  <div className="mt-2 flex gap-2">
                    <span className="text-[10px] px-2 py-0.5 bg-purple-100 text-purple-800 rounded font-medium">Complete Protein</span>
                    <span className="text-[10px] px-2 py-0.5 bg-amber-100 text-amber-800 rounded font-medium">Iron Rich</span>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-bold text-sm text-slate-800">Dinner</span>
                    <span className="text-xs text-slate-500 font-medium">550 kcal • 24g Protein</span>
                  </div>
                  <p className="text-xs text-slate-600">Paneer Bhurji (150g) with 2 Jowar Rotis & Steamed Beans Poriyal</p>
                  <div className="mt-2 flex gap-2">
                    <span className="text-[10px] px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded font-medium">Gluten-Free</span>
                    <span className="text-[10px] px-2 py-0.5 bg-teal-100 text-teal-800 rounded font-medium">Calcium Source</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Clinical Disclaimer Banner */}
      <section className="bg-amber-50 border-y border-amber-200 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-amber-900 leading-relaxed">
          <p className="font-bold mb-1">⚠️ Medical & Nutritional Disclaimer</p>
          <p className="max-w-4xl mx-auto">
            NutriGuard is designed as an educational nutrition planning tool and AI dietary assistant based on authoritative sources including the Indian Council of Medical Research (ICMR) and National Institute of Nutrition (NIN). It does not provide medical diagnoses, treatment prescriptions, or emergency healthcare services. Always consult a qualified physician or registered clinical dietitian before making significant dietary changes, especially if managing chronic illnesses, pregnancy, or prescription medications.
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-auto py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <span className="font-bold text-slate-900 text-lg">NutriGuard</span>
            <span className="text-xs text-slate-400">v2.0.0</span>
          </div>

          <div className="flex flex-wrap gap-6 text-sm text-slate-600 font-medium">
            <Link to="/meals" className="hover:text-emerald-600">Indian Food Explorer</Link>
            <Link to="/login" className="hover:text-emerald-600">Client Portal</Link>
            <Link to="/admin" className="hover:text-emerald-600">Clinical Reviewer</Link>
            <Link to="/system-health" className="hover:text-emerald-600">System Health</Link>
          </div>

          <p className="text-xs text-slate-400">
            © {new Date().getFullYear()} NutriGuard AI Platform. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
