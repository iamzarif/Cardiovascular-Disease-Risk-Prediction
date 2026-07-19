import streamlit as st
import pandas as pd

# 1. Page Configuration - Native design ensures clean UI
st.set_page_config(
    page_title="CVD Risk Assessment",
    page_icon="🫀",
    layout="centered"
)

# 2. Web App UI Header
st.title("Cardiovascular Disease Risk Assessment Project")
st.caption("MIA5100Z - Foundations & Applications of Machine Learning")

# Small warning as requested
st.markdown("<small><i>ACADEMIC PROOF OF CONCEPT: Form inputs use everyday language.</i></small>", unsafe_allow_html=True)

st.write("---")
st.write("### 📝 Quick Health Questionnaire")

st.markdown("""
    <style>
    /* Increase size of question labels */
    div[data-testid="stWidget"] label p {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

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
st.write(f"**Computed BMI:** {bmi:.1f}")

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
# 4. Handle Prediction Action
if st.button("Submit Questionnaire & Calculate Risk", type="primary"):
    risk_score = 0
    high_risk_flag = False
    
    # Red Flag Check (Clinical Danger Zones)
    # If any single critical metric is in a dangerous range, it overrides everything else
    if sys_bp >= 160 or dia_bp >= 100: high_risk_flag = True  # Hypertension Stage 2+
    if blood_sugar >= 126 and diabetes: high_risk_flag = True # Uncontrolled Diabetes
    
    # Additive Scoring
    if age > 55: risk_score += 2
    elif age > 40: risk_score += 1
        
    if bmi >= 30: risk_score += 2
    elif bmi >= 25: risk_score += 1
        
    if sys_bp >= 130 or dia_bp >= 80: risk_score += 2 # Elevated BP
    
    if cholesterol >= 240: risk_score += 2
    elif cholesterol >= 200: risk_score += 1
    
    if hdl < 40: risk_score += 2 # Low HDL is a significant independent risk factor
    
    if blood_sugar >= 100: risk_score += 2
        
    if smoking == "Current Smoker": risk_score += 2
    if family_history: risk_score += 2

    st.divider()
    
    # Classification logic
    if high_risk_flag or risk_score >= 8:
        st.error("### Prediction: HIGH RISK 🔴")
        st.write("Your profile shows critical indicators that require immediate medical attention.")
    elif risk_score >= 4:
        st.warning("### Prediction: INTERMEDIARY RISK 🟡")
        st.write("Several risk factors identified. We recommend scheduling a screening with your doctor.")
    else:
        st.success("### Prediction: LOW RISK 🟢")
        st.write("Your health indicators currently align with lower-risk parameters.")
