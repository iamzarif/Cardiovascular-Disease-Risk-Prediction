import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="CVD Risk Assessment", page_icon="🫀", layout="centered")

# 2. Define the Pop-up Result Dialog (Defined here so it's globally available)
@st.dialog("Assessment Result")
def show_result(risk_label, color_emoji, explanation):
    st.write(f"### Prediction: {risk_label} {color_emoji}")
    st.write(explanation)
    st.info("💡 **Recommendation:** Please consult with your family doctor to discuss these results and get a professional screening.")
    if st.button("Close"):
        st.rerun()

# 3. Web App UI Header
st.title("🫀 Cardiovascular Disease Risk Assessment")
st.caption("MIA5100Z Machine Learning Project Demo")
st.markdown("<small><i>ACADEMIC PROOF OF CONCEPT: Form inputs use everyday language.</i></small>", unsafe_allow_html=True)
st.write("---")

# --- INPUTS ---
age = st.number_input("What is your Age?", min_value=1, max_value=120, value=25)
sex = st.selectbox("What is your Biological Sex?", ["Male", "Female"])

col_ft, col_in, col_w = st.columns(3)
with col_ft: ft = st.number_input("Height (ft)", min_value=3, max_value=8, value=5)
with col_in: inches = st.number_input("Height (in)", min_value=0, max_value=11, value=7)
with col_w: weight_kg = st.number_input("Weight (kg)", min_value=10.0, max_value=400.0, value=70.0, step=0.1)

# BMI Logic
height_m = ((ft * 12) + inches) * 0.0254
bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0.0
st.write(f"**Computed BMI:** {bmi:.1f}")

# BP Logic
bp_selection = st.selectbox("Typical Blood Pressure:", [
    "Normal (Below 120/80 mmHg)",
    "Elevated (Systolic 120-129)",
    "High Stage 1 (Systolic 130-139 or Diastolic 80-89)",
    "High Stage 2 (Systolic 140+ or Diastolic 90+)"
])

if "Normal" in bp_selection: sys_bp, dia_bp = 115, 75
elif "Elevated" in bp_selection: sys_bp, dia_bp = 125, 78
elif "Stage 1" in bp_selection: sys_bp, dia_bp = 135, 85
else: sys_bp, dia_bp = 150, 95

# Other inputs
chol_selection = st.selectbox("Typical Total Cholesterol:", ["Normal (<200)", "Borderline (200–239)", "High (240+)"])
hdl_selection = st.selectbox("Typical HDL ('Good') Cholesterol:", ["Optimal (60+)", "Normal (40-59)", "Low (<40)"])
sugar_selection = st.selectbox("Typical Fasting Blood Sugar:", ["Normal (<100)", "Pre-Diabetes (100–125)", "Diabetic (126+)"])

smoking = st.selectbox("Smoking Status:", ["Never Smoked", "Former Smoker", "Current Smoker"])
diabetes = st.checkbox("Clinically diagnosed with Diabetes?")
family_history = st.checkbox("Family history of heart disease?")

# --- PREDICTION LOGIC ---
if st.button("Submit Questionnaire & Calculate Risk", type="primary", key="submit_btn"):
    risk_score = 0
    high_risk_flag = False
    
    # Red Flag Check
    if sys_bp >= 160 or dia_bp >= 100: high_risk_flag = True
    if "Diabetic" in sugar_selection and diabetes: high_risk_flag = True
    
    # Additive Scoring
    if age > 55: risk_score += 2
    elif age > 40: risk_score += 1
    if bmi >= 30: risk_score += 2
    elif bmi >= 25: risk_score += 1
    if sys_bp >= 130 or dia_bp >= 80: risk_score += 2
    if "High" in chol_selection: risk_score += 2
    elif "Borderline" in chol_selection: risk_score += 1
    if "Low" in hdl_selection: risk_score += 2
    if "Diabetic" in sugar_selection or diabetes: risk_score += 2
    elif "Pre-Diabetes" in sugar_selection: risk_score += 1
    if smoking == "Current Smoker": risk_score += 2
    if family_history: risk_score += 2

    # Trigger Dialog based on risk
    if high_risk_flag or risk_score >= 8:
        show_result("HIGH RISK", "🔴", "Your profile shows critical indicators that require immediate medical attention.")
    elif risk_score >= 4:
        show_result("INTERMEDIARY RISK", "🟡", "Several risk factors identified. We recommend scheduling a screening with your doctor.")
    else:
        show_result("LOW RISK", "🟢", "Your health indicators currently align with lower-risk parameters.")
