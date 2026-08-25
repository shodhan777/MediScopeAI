import { useState } from "react";
import API from "../services/api";
import RiskCard from "../components/RiskCard";
import DiseaseXAI from "../components/DiseaseXAI";
import HeartSimulator from "../components/HeartSimulator";
import "../styles/Form.css";

function HeartForm() {
  const [submittedData, setSubmittedData] = useState(null);
  const [form, setForm] = useState({
    age: "",
    sex: 1,
    cp: 0,
    trestbps: "",
    chol: "",
    fbs: 0,
    restecg: 0,
    thalach: "",
    exang: 0,
    oldpeak: "",
    slope: 1,
    ca: 0,
    thal: 2
  });

  const [result, setResult] = useState(null);
  const [showMore, setShowMore] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const change = (e) => {
    setForm({
      ...form,
      [e.target.name]: Number(e.target.value)
    });
  };

  const submit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setErrorMsg("");

    try {
      const finalData = {
        age: Number(form.age || 50),
        sex: Number(form.sex || 1),
        cp: Number(form.cp || 0),
        trestbps: Number(form.trestbps || 120),
        chol: Number(form.chol || 200),
        fbs: Number(form.fbs || 0),
        restecg: Number(form.restecg || 0),
        thalach: Number(form.thalach || 150),
        exang: Number(form.exang || 0),
        oldpeak: Number(form.oldpeak || 1),
        slope: Number(form.slope || 1),
        ca: Number(form.ca || 0),
        thal: Number(form.thal || 2)
      };

      const res = await API.post("/predict/heart", finalData);
      setSubmittedData(finalData);
      setResult(res.data);
    } catch (error) {
      console.error(error);
      if (error.response && error.response.status === 422) {
        setErrorMsg("Please enter valid input data.");
      } else {
        setErrorMsg("Prediction service is temporarily unavailable. Please try again.");
      }
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="form-card">
        <h1>Cardiovascular Risk Assessment</h1>
        <p className="subtitle">
          Please provide patient vitals and clinical history for cardiovascular risk assessment.
        </p>

        <form className="smart-form" onSubmit={submit}>
          {/* Essential Fields */}

          <h3>Patient Demographics and Vitals</h3>

          <div className="label-row">
            <label><strong>Age</strong> (Years)</label>
          </div>
          <input
            type="number"
            name="age"
            min="20"
            max="100"
            required
            onChange={change}
          />

          <div className="label-row">
            <label><strong>Gender</strong> </label>
          </div>
          <select name="sex" onChange={change}>
            <option value="1">Male</option>
            <option value="0">Female</option>
          </select>

          <div className="label-row">
            <label><strong>Chest Pain</strong> (Angina Characteristics)</label>
          </div>
          <select name="cp" onChange={change}>
            <option value="0">Typical Angina</option>
            <option value="1">Atypical Angina</option>
            <option value="2">Non-anginal Pain</option>
            <option value="3">Asymptomatic</option>
          </select>

          <div className="label-row">
            <label><strong>Resting Blood Pressure</strong> (Systolic, mmHg)</label>
            <span className="normal-range">Normal: 90 - 120</span>
          </div>
          <input
            type="number"
            name="trestbps"
            min="90"
            max="200"
            required
            onChange={change}
          />

          <div className="label-row">
            <label><strong>Cholesterol</strong> (Serum, mg/dL)</label>
            <span className="normal-range">Normal: &lt; 200</span>
          </div>
          <input
            type="number"
            name="chol"
            min="100"
            max="600"
            required
            onChange={change}
          />

          {/* Advanced Toggle */}

          <button
            type="button"
            className="secondary-btn"
            onClick={() => setShowMore(!showMore)}
          >
            {showMore ? "Hide Clinical Indicators" : "Enter Clinical Indicators"}
          </button>

          {/* Advanced Fields */}

          {showMore && (
            <>
              <h3>Clinical Indicators and Test Results</h3>

              <div className="label-row">
                <label><strong>Fasting Blood Sugar</strong> (&gt; 120 mg/dL)</label>
                <span className="normal-range">Normal: &lt; 100</span>
              </div>
              <select name="fbs" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <div className="label-row">
                <label><strong>Resting ECG</strong> (Electrocardiogram)</label>
              </div>
              <select name="restecg" onChange={change}>
                <option value="0">Normal</option>
                <option value="1">ST-T abnormality</option>
                <option value="2">Left ventricular hypertrophy</option>
              </select>

              <div className="label-row">
                <label><strong>Max Heart Rate</strong> (Achieved, bpm)</label>
              </div>
              <input
                type="number"
                name="thalach"
                min="70"
                max="220"
                onChange={change}
              />

              <div className="label-row">
                <label><strong>Exercise-Induced Angina</strong> (Angina Pectoris)</label>
              </div>
              <select name="exang" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <div className="label-row">
                <label><strong>ST Depression</strong> (Oldpeak)</label>
              </div>
              <input
                type="number"
                step="0.1"
                min="0"
                max="6"
                name="oldpeak"
                onChange={change}
              />

              <div className="label-row">
                <label><strong>ST Segment Slope</strong> (Peak Exercise)</label>
              </div>
              <select name="slope" onChange={change}>
                <option value="0">Upsloping</option>
                <option value="1">Flat</option>
                <option value="2">Downsloping</option>
              </select>

              <div className="label-row">
                <label><strong>Major Vessels</strong> (Fluoroscopy, 0-3)</label>
              </div>
              <select name="ca" onChange={change}>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>

              <div className="label-row">
                <label><strong>Thalassemia</strong> (Hemoglobin Disorder)</label>
              </div>
              <select name="thal" onChange={change}>
                <option value="1">Normal</option>
                <option value="2">Fixed Defect</option>
                <option value="3">Reversible Defect</option>
              </select>
            </>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Analyzing patient data..." : "Predict Risk"}
          </button>
        </form>

        {errorMsg && (
          <div className="error-message">
            {errorMsg}
          </div>
        )}

        {result && !loading && !errorMsg && (
          <>
            <RiskCard result={result} />
            <div className="confidence-box">
              <p><strong>Statistical Model Confidence:</strong> {result.confidence}</p>
            </div>
            
            <DiseaseXAI result={result} />
            
            <HeartSimulator result={result} initialData={submittedData} />
          </>
        )}
      </div>
    </div>
  );
}

export default HeartForm;