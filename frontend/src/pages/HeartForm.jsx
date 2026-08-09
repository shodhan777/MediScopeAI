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
        <h1>❤️ Heart Disease Prediction</h1>
        <p className="subtitle">
          Enter essential details first. Add advanced values for higher confidence.
        </p>

        <form className="smart-form" onSubmit={submit}>
          {/* Essential Fields */}

          <h3>Basic Information</h3>

          <label>Age (20 - 100)</label>
          <input
            type="number"
            name="age"
            min="20"
            max="100"
            required
            onChange={change}
          />

          <label>Gender</label>
          <select name="sex" onChange={change}>
            <option value="1">Male</option>
            <option value="0">Female</option>
          </select>

          <label>Chest Pain Type</label>
          <select name="cp" onChange={change}>
            <option value="0">Typical Angina</option>
            <option value="1">Atypical Angina</option>
            <option value="2">Non-anginal Pain</option>
            <option value="3">Asymptomatic</option>
          </select>

          <label>Resting Blood Pressure (90 - 200)</label>
          <input
            type="number"
            name="trestbps"
            min="90"
            max="200"
            required
            onChange={change}
          />

          <label>Cholesterol (100 - 600)</label>
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
            {showMore ? "Hide Advanced Fields" : "Add More Details"}
          </button>

          {/* Advanced Fields */}

          {showMore && (
            <>
              <h3>Advanced Cardiology Inputs</h3>

              <label>Fasting Blood Sugar `{'>'}` 120 mg/dl</label>
              <select name="fbs" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <label>Resting ECG</label>
              <select name="restecg" onChange={change}>
                <option value="0">Normal</option>
                <option value="1">ST-T abnormality</option>
                <option value="2">Left ventricular hypertrophy</option>
              </select>

              <label>Maximum Heart Rate (70 - 220)</label>
              <input
                type="number"
                name="thalach"
                min="70"
                max="220"
                onChange={change}
              />

              <label>Exercise Induced Angina</label>
              <select name="exang" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <label>Old Peak (0 - 6)</label>
              <input
                type="number"
                step="0.1"
                min="0"
                max="6"
                name="oldpeak"
                onChange={change}
              />

              <label>Slope</label>
              <select name="slope" onChange={change}>
                <option value="0">Upsloping</option>
                <option value="1">Flat</option>
                <option value="2">Downsloping</option>
              </select>

              <label>Major Vessels (0 - 3)</label>
              <select name="ca" onChange={change}>
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>

              <label>Thalassemia</label>
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