import streamlit as st
import pandas as pd
import joblib

# 1. Load the model
# (Make sure cvd_rf_model.pkl is uploaded to the same GitHub repository!)
model = joblib.load('cvd_rf_model.pkl')

# 2. Build the Web App UI
st.title("🫀 CVD Risk Assessment (MIA5100Z)")
st.warning("⚠️ ACADEMIC PROOF OF CONCEPT ONLY. Not for real medical diagnosis.")

st.write("Enter your clinical data below to see the model's prediction:")

# Create input fields for the user
age = st.slider("Age", 18, 100, 45)
bmi = st.number_input("BMI", 10.0, 50.0, 26.5)
sys_bp = st.slider("Systolic Blood Pressure", 80, 200, 125)
dia_bp = st.slider("Diastolic Blood Pressure", 50, 130, 80)
cholesterol = st.slider("Total Cholesterol", 100, 400, 180)
hdl = st.slider("HDL", 20, 100, 50)
blood_sugar = st.slider("Fasting Blood Sugar", 50, 300, 95)

# Categorical inputs
sex = st.selectbox("Sex", ["Male", "Female"])
smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
diabetes = st.checkbox("Do you have Diabetes?")
family_history = st.checkbox("Family History of CVD?")

# 3. Format the input for the model
if st.button("Predict Risk Level"):
    # Note: Ensure these column names and encodings exactly match 
    # what your Random Forest model saw during training!
    input_data = pd.DataFrame({
        'Age': [age],
        'BMI': [bmi],
        'Systolic_BP': [sys_bp],
        'Diastolic_BP': [dia_bp],
        'Total_Cholesterol': [cholesterol],
        'HDL': [hdl],
        'Fasting_Blood_Sugar': [blood_sugar],
        'Sex': [1 if sex == "Male" else 0],
        'Smoking': [0 if smoking=="Never" else (1 if smoking=="Former" else 2)],
        'Diabetes': [1 if diabetes else 0],
        'Family_History': [1 if family_history else 0]
    })
    
    # 4. Make Prediction
    prediction = model.predict(input_data)[0]
    
    st.divider()
    if prediction == "LOW": 
        st.success("### Prediction: LOW RISK 🟢")
    elif prediction == "INTERMEDIARY":
        st.warning("### Prediction: INTERMEDIARY RISK 🟡")
    else:
        st.error("### Prediction: HIGH RISK 🔴")