<html>
<head>
<title>app.py</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type="text/css">
.s0 { color: #cf8e6d;}
.s1 { color: #bcbec4;}
.s2 { color: #7a7e85;}
.s3 { color: #bcbec4;}
.s4 { color: #6aab73;}
.s5 { color: #2aacb8;}
</style>
</head>
<body bgcolor="#191a1c">
<table CELLSPACING=0 CELLPADDING=5 COLS=1 WIDTH="100%" BGCOLOR="#606060" >
<tr><td><center>
<font face="Arial, Helvetica" color="#000000">
app.py</font>
</center></td></tr></table>
<pre><span class="s0">import </span><span class="s1">streamlit </span><span class="s0">as </span><span class="s1">st</span>
<span class="s0">import </span><span class="s1">pandas </span><span class="s0">as </span><span class="s1">pd</span>
<span class="s0">import </span><span class="s1">joblib</span>

<span class="s2"># 1. Load the model</span>
<span class="s2"># (Make sure cvd_rf_model.pkl is in the same folder as this script)</span>
<span class="s1">model </span><span class="s3">= </span><span class="s1">joblib</span><span class="s3">.</span><span class="s1">load</span><span class="s3">(</span><span class="s4">'cvd_rf_model.pkl'</span><span class="s3">)</span>

<span class="s2"># 2. Build the Web App UI</span>
<span class="s1">st</span><span class="s3">.</span><span class="s1">title</span><span class="s3">(</span><span class="s4">&quot;🫀 CVD Risk Assessment&quot;</span><span class="s3">)</span>
<span class="s1">st</span><span class="s3">.</span><span class="s1">warning</span><span class="s3">(</span><span class="s4">&quot;PROOF OF CONCEPT ONLY. Not for real medical diagnosis.&quot;</span><span class="s3">)</span>

<span class="s1">st</span><span class="s3">.</span><span class="s1">write</span><span class="s3">(</span><span class="s4">&quot;Enter your clinical data below to see the model's prediction:&quot;</span><span class="s3">)</span>

<span class="s2"># Create input fields for the user</span>
<span class="s1">age </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;Age&quot;</span><span class="s3">, </span><span class="s5">18</span><span class="s3">, </span><span class="s5">100</span><span class="s3">, </span><span class="s5">45</span><span class="s3">)</span>
<span class="s1">bmi </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">number_input</span><span class="s3">(</span><span class="s4">&quot;BMI&quot;</span><span class="s3">, </span><span class="s5">10.0</span><span class="s3">, </span><span class="s5">50.0</span><span class="s3">, </span><span class="s5">26.5</span><span class="s3">)</span>
<span class="s1">sys_bp </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;Systolic Blood Pressure&quot;</span><span class="s3">, </span><span class="s5">80</span><span class="s3">, </span><span class="s5">200</span><span class="s3">, </span><span class="s5">125</span><span class="s3">)</span>
<span class="s1">dia_bp </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;Diastolic Blood Pressure&quot;</span><span class="s3">, </span><span class="s5">50</span><span class="s3">, </span><span class="s5">130</span><span class="s3">, </span><span class="s5">80</span><span class="s3">)</span>
<span class="s1">cholesterol </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;Total Cholesterol&quot;</span><span class="s3">, </span><span class="s5">100</span><span class="s3">, </span><span class="s5">400</span><span class="s3">, </span><span class="s5">180</span><span class="s3">)</span>
<span class="s1">hdl </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;HDL&quot;</span><span class="s3">, </span><span class="s5">20</span><span class="s3">, </span><span class="s5">100</span><span class="s3">, </span><span class="s5">50</span><span class="s3">)</span>
<span class="s1">blood_sugar </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">slider</span><span class="s3">(</span><span class="s4">&quot;Fasting Blood Sugar&quot;</span><span class="s3">, </span><span class="s5">50</span><span class="s3">, </span><span class="s5">300</span><span class="s3">, </span><span class="s5">95</span><span class="s3">)</span>

<span class="s2"># Categorical inputs</span>
<span class="s1">sex </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">selectbox</span><span class="s3">(</span><span class="s4">&quot;Sex&quot;</span><span class="s3">, [</span><span class="s4">&quot;Male&quot;</span><span class="s3">, </span><span class="s4">&quot;Female&quot;</span><span class="s3">])</span>
<span class="s1">smoking </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">selectbox</span><span class="s3">(</span><span class="s4">&quot;Smoking Status&quot;</span><span class="s3">, [</span><span class="s4">&quot;Never&quot;</span><span class="s3">, </span><span class="s4">&quot;Former&quot;</span><span class="s3">, </span><span class="s4">&quot;Current&quot;</span><span class="s3">])</span>
<span class="s1">diabetes </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">checkbox</span><span class="s3">(</span><span class="s4">&quot;Do you have Diabetes?&quot;</span><span class="s3">)</span>
<span class="s1">family_history </span><span class="s3">= </span><span class="s1">st</span><span class="s3">.</span><span class="s1">checkbox</span><span class="s3">(</span><span class="s4">&quot;Family History of CVD?&quot;</span><span class="s3">)</span>

<span class="s2"># 3. Format the input for the model</span>
<span class="s0">if </span><span class="s1">st</span><span class="s3">.</span><span class="s1">button</span><span class="s3">(</span><span class="s4">&quot;Predict Risk Level&quot;</span><span class="s3">):</span>
    <span class="s2"># Note: Ensure these column names and encodings exactly match </span>
    <span class="s2"># what your Random Forest model saw during training!</span>
    <span class="s1">input_data </span><span class="s3">= </span><span class="s1">pd</span><span class="s3">.</span><span class="s1">DataFrame</span><span class="s3">({</span>
        <span class="s4">'Age'</span><span class="s3">: [</span><span class="s1">age</span><span class="s3">],</span>
        <span class="s4">'BMI'</span><span class="s3">: [</span><span class="s1">bmi</span><span class="s3">],</span>
        <span class="s4">'Systolic_BP'</span><span class="s3">: [</span><span class="s1">sys_bp</span><span class="s3">],</span>
        <span class="s4">'Diastolic_BP'</span><span class="s3">: [</span><span class="s1">dia_bp</span><span class="s3">],</span>
        <span class="s4">'Total_Cholesterol'</span><span class="s3">: [</span><span class="s1">cholesterol</span><span class="s3">],</span>
        <span class="s4">'HDL'</span><span class="s3">: [</span><span class="s1">hdl</span><span class="s3">],</span>
        <span class="s4">'Fasting_Blood_Sugar'</span><span class="s3">: [</span><span class="s1">blood_sugar</span><span class="s3">],</span>
        <span class="s4">'Sex'</span><span class="s3">: [</span><span class="s5">1 </span><span class="s0">if </span><span class="s1">sex </span><span class="s3">== </span><span class="s4">&quot;Male&quot; </span><span class="s0">else </span><span class="s5">0</span><span class="s3">],</span>
        <span class="s4">'Smoking'</span><span class="s3">: [</span><span class="s5">0 </span><span class="s0">if </span><span class="s1">smoking </span><span class="s3">== </span><span class="s4">&quot;Never&quot; </span><span class="s0">else </span><span class="s3">(</span><span class="s5">1 </span><span class="s0">if </span><span class="s1">smoking </span><span class="s3">== </span><span class="s4">&quot;Former&quot; </span><span class="s0">else </span><span class="s5">2</span><span class="s3">)],</span>
        <span class="s4">'Diabetes'</span><span class="s3">: [</span><span class="s5">1 </span><span class="s0">if </span><span class="s1">diabetes </span><span class="s0">else </span><span class="s5">0</span><span class="s3">],</span>
        <span class="s4">'Family_History'</span><span class="s3">: [</span><span class="s5">1 </span><span class="s0">if </span><span class="s1">family_history </span><span class="s0">else </span><span class="s5">0</span><span class="s3">]</span>
    <span class="s3">})</span>

    <span class="s2"># 4. Make Prediction</span>
    <span class="s1">prediction </span><span class="s3">= </span><span class="s1">model</span><span class="s3">.</span><span class="s1">predict</span><span class="s3">(</span><span class="s1">input_data</span><span class="s3">)[</span><span class="s5">0</span><span class="s3">]</span>

    <span class="s1">st</span><span class="s3">.</span><span class="s1">divider</span><span class="s3">()</span>
    <span class="s0">if </span><span class="s1">prediction </span><span class="s3">== </span><span class="s4">&quot;LOW&quot;</span><span class="s3">:  </span><span class="s2"># Adjust based on your actual target labels</span>
        <span class="s1">st</span><span class="s3">.</span><span class="s1">success</span><span class="s3">(</span><span class="s4">&quot;### Prediction: LOW RISK 🟢&quot;</span><span class="s3">)</span>
    <span class="s0">elif </span><span class="s1">prediction </span><span class="s3">== </span><span class="s4">&quot;INTERMEDIARY&quot;</span><span class="s3">:</span>
        <span class="s1">st</span><span class="s3">.</span><span class="s1">warning</span><span class="s3">(</span><span class="s4">&quot;### Prediction: INTERMEDIARY RISK 🟡&quot;</span><span class="s3">)</span>
    <span class="s0">else</span><span class="s3">:</span>
        <span class="s1">st</span><span class="s3">.</span><span class="s1">error</span><span class="s3">(</span><span class="s4">&quot;### Prediction: HIGH RISK 🔴&quot;</span><span class="s3">)</span></pre>
</body>
</html>