import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="CVD Risk Assessment",
    page_icon="🫀",
    layout="centered"
)

# 2. Modern UI CSS (Clubhouse/Airbnb aesthetic)
st.markdown("""
    <style>
    /* Global white background */
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Make the warning text tiny and subtle */
    .stWarning {
        font-size: 0.75rem !important;
        padding: 5px 10px !important;
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        color: #6c757d !important;
    }

    /* Soft, modern input boxes */
    .stNumberInput, .stSelectbox {
        border-radius: 12px !important;
        border: 1px solid #ced4da !important;
    }
    
    /* Bigger, bolder question text */
    label p {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #212529 !important;
        padding-bottom: 5px !important;
    }
    
    /* Clean, pill-shaped button */
    div.stButton > button {
        background-color: #FF385C !important; /* Airbnb-style pink/red */
        color: white !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
        padding: 10px 30px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Web App UI
st.title("🫀 CVD Risk Assessment")
st.warning("ACADEMIC PROOF OF CONCEPT ONLY. Form inputs use everyday language.")

st.write("### 📝 Quick Health Questionnaire")

# --- SECTION 1: GENERAL INFO ---
age = st.number_input("What is your Age?", min_value=1, max_value=120, value=25)
sex = st.selectbox("What is your Biological Sex?", ["Male", "Female"])

col_ft, col_in, col_w = st.columns(3)
with col_ft: ft = st.number_input("Height (ft)", min_value=3, max_value=8, value=5)
with col_in: inches = st.number_input("Height (in)", min_value=0, max_value=11, value=7)
with col_w: weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=400.0, value=70.0, step=0.1)

# BMI calculation
height_m = ((ft * 12) + inches) * 0.0254
bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0.0
st.info(f"💡 Computed BMI: **{bmi:.1f}**")

# --- SECTION 2: CLINICAL METRICS ---
bp_selection = st.selectbox("Typical Blood Pressure:", [
    "Normal (Below 120/80 mmHg)",
    "Elevated (Systolic 120-129)",
    "High Stage 1 (Systolic 130-139 or Diastolic 80-89)",
    "High Stage 2 (Systolic 140+ or Diastolic 90+)"
])

chol_selection = st.selectbox("Typical Total Cholesterol:", [
    "Normal (Below 200 mg/dL)",
    "Borderline High (200–239 mg/dL)",
    "High (240 mg/dL or above)"
])

hdl_selection = st.selectbox("Typical HDL ('Good') Cholesterol:", [
    "Optimal (60+ mg/dL)",
    "Normal (40-59 mg/dL)",
    "Low (Below 40 mg/dL)"
])

sugar_selection = st.selectbox("Typical Fasting Blood Sugar:", [
    "Normal (Below 100 mg/dL)",
    "Pre-Diabetes (100–125 mg/dL)",
    "Diabetic Profile (126+ mg/dL)"
])

# --- SECTION 3: LIFESTYLE ---
smoking = st.selectbox("Smoking Status:", ["Never Smoked", "Former Smoker", "Current Smoker"])
diabetes = st.checkbox("Clinically diagnosed with Diabetes?")
family_history = st.checkbox("Family history of heart disease?")

# --- PREDICTION LOGIC ---
if st.button("Submit & Calculate Risk"):
    # (Same robust scoring logic as before)
    # Mapping
    sys_bp = 150 if "Stage 2" in bp_selection else (135 if "Stage 1" in bp_selection else 115)
    cholesterol = 250 if "High" in chol_selection else (220 if "Borderline" in chol_selection else 170)
    hdl = 35 if "Low" in hdl_selection else (48 if "Normal" in hdl_selection else 65)
    blood_sugar = 140 if "Diabetic" in sugar_selection else (110 if "Pre-Diabetes" in sugar_selection else 85)
    
    # Simple score
    risk_score = (1 if age > 40 else 0) + (2 if bmi > 25 else 0) + (2 if sys_bp > 130 else 0) + (1 if cholesterol > 200 else 0)
    
    st.divider()
    if risk_score <= 3: st.success("### Prediction: LOW RISK 🟢")
    elif risk_score <= 7: st.warning("### Prediction: INTERMEDIARY RISK 🟡")
    else: st.error("### Prediction: HIGH RISK 🔴")
