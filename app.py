import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="CVD Risk Assessment",
    page_icon="🫀",
    layout="centered"
)

# 2. Web App Header
st.title("🫀 MIA5100: Cardiovascular Disease Risk Assessment")
st.caption("MIA5100")
st.warning("PROOF OF CONCEPT ONLY. Form inputs use everyday language for demonstration purposes.")

st.write("### 📝 Patient Questionnaire")
st.write("Please fill out the form below. Medical parameters will be auto-calculated for the model underlying.")

# --- SECTION 1: BASIC DEMOGRAPHICS & ANTHROPOMETRICS ---
st.subheader("👤 Step 1: General Information")
age = st.number_input("What is your Age?", min_value=1, max_value=120, value=25)
sex = st.selectbox("What is your Biological Sex?", ["Male", "Female"])

col_w, col_h = st.columns(2)
with col_w:
    weight = st.number_input("What is your Weight (in kg)?", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
with col_h:
    height_cm = st.number_input("What is your Height (in cm)?", min_value=50.0, max_value=250.0, value=175.0, step=0.1)

# Under-the-hood BMI conversion logic
height_m = height_cm / 100.0
bmi = weight / (height_m ** 2)
st.info(f"💡 **Auto-Calculated Feature:** Your computed Body Mass Index (BMI) is **{bmi:.1f}**")

# --- SECTION 2: MEDICAL ATTRIBUTES TRANSLATED ---
st.subheader("🩺 Step 2: Clinical Metrics")

bp_selection = st.selectbox(
    "How would you describe your typical Blood Pressure readings?",
    [
        "Normal (Less than 120/80 mmHg)",
        "Elevated / Slightly High (Systolic 120-129 AND Diastolic less than 80)",
        "High Blood Pressure - Stage 1 (Systolic 130-139 OR Diastolic 80-89)",
        "High Blood Pressure - Stage 2 (Systolic 140+ OR Diastolic 90+)"
    ]
)

# Translate simplified category choices back to numeric baseline features for the system model
if "Normal" in bp_selection:
    sys_bp, dia_bp = 115, 75
elif "Elevated" in bp_selection:
    sys_bp, dia_bp = 125, 78
elif "Stage 1" in bp_selection:
    sys_bp, dia_bp = 135, 85
else:
    sys_bp, dia_bp = 150, 95

# Simplified lab default parameters (or allow custom overrides if users know them)
st.write("**🩸 Blood Panel Profiles** (Leave as default if you don't have recent lab numbers)")
col_c, col_hdl, col_s = st.columns(3)
with col_c:
    cholesterol = st.number_input("Total Cholesterol (mg/dL)", value=180)
with col_hdl:
    hdl = st.number_input("HDL 'Good' Cholesterol (mg/dL)", value=50)
with col_s:
    blood_sugar = st.number_input("Fasting Blood Sugar (mg/dL)", value=95)

# --- SECTION 3: LIFESTYLE & HISTORY ---
st.subheader("🚬 Step 3: Lifestyle & History")
smoking = st.selectbox("What is your Smoking Status?", ["Never Smoked", "Former Smoker", "Current Smoker"])
diabetes = st.checkbox("Have you ever been diagnosed with Diabetes?")
family_history = st.checkbox("Do you have a family history of heart disease (CVD)?")

# 4. Handle Prediction Logic Matrix
if st.button("Submit Questionnaire & Calculate Risk", type="primary"):
    risk_score = 0
    
    # Process inputs through tree-node feature approximations
    if age > 55: risk_score += 2
    elif age > 40: risk_score += 1
        
    if bmi >= 30: risk_score += 2
    elif bmi >= 25: risk_score += 1
        
    if sys_bp >= 140 or dia_bp >= 90: risk_score += 3  
    elif sys_bp >= 130 or dia_bp >= 80: risk_score += 1 
        
    if cholesterol > 240: risk_score += 2
    elif cholesterol > 200: risk_score += 1
    if hdl < (40 if sex == "Male" else 50): risk_score += 1
    if blood_sugar >= 126 or diabetes: risk_score += 3
    elif blood_sugar >= 100: risk_score += 1
        
    if smoking == "Current Smoker": risk_score += 2
    elif smoking == "Former Smoker": risk_score += 1
    if family_history: risk_score += 2

    st.divider()
    st.write("### 📊 System Assessment Dashboard")
    
    # Map target output buckets cleanly
    if risk_score <= 3:
        st.success("### Prediction: LOW RISK 🟢")
        st.write("Your health profile maps closely within baseline low-risk parameters for cardiorespiratory issues.")
    elif risk_score <= 7:
        st.warning("### Prediction: INTERMEDIARY RISK 🟡")
        st.write("Moderate indicators flagged. Suggests regular check-ups for preventative monitoring.")
    else:
        st.error("### Prediction: HIGH RISK 🔴")
        st.write("Elevated combination metrics detected. Highly recommended to maintain awareness of cardiorespiratory profiles.")
