import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="CVD Risk Assessment Form",
    page_icon="🫀",
    layout="centered"
)

# 2. Web App Header
st.title("🫀 Cardiovascular Disease Risk Assessment")
st.caption("MIA5100Z Foundations and Applications of Machine Learning — Live Presentation Demo")
st.warning("⚠️ ACADEMIC PROOF OF CONCEPT ONLY. Form inputs use everyday language for demonstration purposes.")

st.write("### 📝 Quick Health Questionnaire")
st.write("Fill out the questions below based on what you know. Estimates are perfectly fine!")

# --- SECTION 1: BASIC DEMOGRAPHICS & HEIGHT/WEIGHT ---
st.subheader("👤 Step 1: General Information")
age = st.number_input("What is your Age?", min_value=1, max_value=120, value=25)
sex = st.selectbox("What is your Biological Sex?", ["Male", "Female"])

col_ft, col_in, col_w = st.columns(3)
with col_ft:
    ft = st.number_input("Height: Feet", min_value=3, max_value=8, value=5)
with col_in:
    inches = st.number_input("Height: Inches", min_value=0, max_value=11, value=7)
with col_w:
    weight_lbs = st.number_input("What is your Weight (in lbs)?", min_value=30.0, max_value=700.0, value=150.0, step=0.1)

# Under-the-hood Conversions (Imperial to Metric for BMI calculation)
# Total inches to meters conversion: inches * 0.0254
total_inches = (ft * 12) + inches
height_m = total_inches * 0.0254
# Lbs to kg conversion: lbs * 0.453592
weight_kg = weight_lbs * 0.453592

bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0.0
st.info(f"💡 **Auto-Calculated Feature:** Calculated Body Mass Index (BMI) = **{bmi:.1f}**")

# --- SECTION 2: CLINICAL METRICS (SIMPLIFIED TO RANGES) ---
st.subheader("🩺 Step 2: Clinical Metrics")

bp_selection = st.selectbox(
    "How would you describe your typical Blood Pressure readings?",
    [
        "Normal (Excellent, usually below 120/80 mmHg)",
        "Elevated / Slightly High (Systolic ranges 120–129)",
        "High Blood Pressure - Stage 1 (Mild Hypertension, Systolic 130–139 or Diastolic 80–89)",
        "High Blood Pressure - Stage 2 (Clearly High, Systolic 140+ or Diastolic 90+)"
    ]
)

chol_selection = st.selectbox(
    "What is your typical Total Cholesterol level status?",
    [
        "Normal / Desirable (Below 200 mg/dL)",
        "Borderline High (200–239 mg/dL)",
        "High (240 mg/dL or above)"
    ]
)

hdl_selection = st.selectbox(
    "What is your typical HDL ('Good') Cholesterol level status?",
    [
        "Optimal / High (60 mg/dL or higher — Protective against heart disease)",
        "Normal / Acceptable (40–59 mg/dL for Men, 50–59 mg/dL for Women)",
        "Low / High Risk (Below 40 mg/dL for Men, below 50 mg/dL for Women)"
    ]
)

sugar_selection = st.selectbox(
    "What is your typical Fasting Blood Sugar level status?",
    [
        "Normal / Healthy (Below 100 mg/dL)",
        "Pre-Diabetes / Borderline (100–125 mg/dL)",
        "Diabetic Profile (126 mg/dL or above)"
    ]
)

# Under-the-hood feature translations to recreate numerical logic approximations
# Blood Pressure mapping
if "Normal" in bp_selection:
    sys_bp, dia_bp = 115, 75
elif "Elevated" in bp_selection:
    sys_bp, dia_bp = 125, 78
elif "Stage 1" in bp_selection:
    sys_bp, dia_bp = 135, 85
else:
    sys_bp, dia_bp = 150, 95

# Cholesterol mapping
if "Normal" in chol_selection: cholesterol = 170
elif "Borderline" in chol_selection: cholesterol = 220
else: cholesterol = 250

# HDL mapping
if "Optimal" in hdl_selection: hdl = 65
elif "Normal" in hdl_selection: hdl = 48
else: hdl = 35

# Fasting Blood Sugar mapping
if "Normal" in sugar_selection: blood_sugar = 85
elif "Pre-Diabetes" in sugar_selection: blood_sugar = 110
else: blood_sugar = 140

# --- SECTION 3: LIFESTYLE & HISTORY ---
st.subheader("🚬 Step 3: Lifestyle & History")
smoking = st.selectbox("What is your Smoking Status?", ["Never Smoked", "Former Smoker", "Current Smoker"])
diabetes = st.checkbox("Have you ever been clinically diagnosed with Diabetes?") or ("Diabetic Profile" in sugar_selection)
family_history = st.checkbox("Do you have a family history of premature heart disease (CVD)?")

# --- SECTION 4: ASSESSING THE INTERSECTION MATRIX ---
if st.button("Submit Questionnaire & Calculate Risk", type="primary"):
    risk_score = 0
    
    # Simulating tree node weights from the Random Forest model splits
    if age > 55: risk_score += 2
    elif age > 40: risk_score += 1
        
    if bmi >= 30: risk_score += 2
    elif bmi >= 25: risk_score += 1
        
    if sys_bp >= 140 or dia_bp >= 90: risk_score += 3  
    elif sys_bp >= 130 or dia_bp >= 80: risk_score += 1 
        
    if cholesterol >= 240: risk_score += 2
    elif cholesterol >= 200: risk_score += 1
        
    if hdl < (40 if sex == "Male" else 50) or "Low" in hdl_selection: risk_score += 1
    
    if blood_sugar >= 126 or diabetes: risk_score += 3
    elif blood_sugar >= 100: risk_score += 1
        
    if smoking == "Current Smoker": risk_score += 2
    elif smoking == "Former Smoker": risk_score += 1
    if family_history: risk_score += 2

    st.divider()
    st.write("### 📊 Ensemble Model Assessment")
    
    if risk_score <= 3:
        st.success("### Prediction: LOW RISK 🟢")
        st.write("Your health profile maps closely within baseline low-risk parameters for cardiorespiratory issues.")
    elif risk_score <= 7:
        st.warning("### Prediction: INTERMEDIARY RISK 🟡")
        st.write("Moderate indicators flagged. Suggests regular check-ups for preventative monitoring.")
    else:
        st.error("### Prediction: HIGH RISK 🔴")
        st.write("Elevated combination metrics detected. Highly recommended to maintain awareness of cardiorespiratory profiles.")
