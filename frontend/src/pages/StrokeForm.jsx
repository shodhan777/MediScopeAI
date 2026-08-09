import { useState } from "react";
import API from "../services/api";
import RiskCard from "../components/RiskCard";
import DiseaseXAI from "../components/DiseaseXAI";
import "../styles/Form.css";

function StrokeForm() {
  const [form, setForm] = useState({
    gender: "Male",
    age: "",
    hypertension: 0,
    heart_disease: 0,
    ever_married: "Yes",
    work_type: "Private",
    Residence_type: "Urban",
    avg_glucose_level: "",
    bmi: "",
    smoking_status: "never smoked"
  });

  const [result, setResult] = useState(null);
  const [showMore, setShowMore] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const change = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    try {
      const finalData = {
        gender: form.gender || "Male",
        age: Number(form.age || 50),
        hypertension: Number(form.hypertension || 0),
        heart_disease: Number(form.heart_disease || 0),
        ever_married: form.ever_married || "Yes",
        work_type: form.work_type || "Private",
        Residence_type: form.Residence_type || "Urban",
        avg_glucose_level: Number(form.avg_glucose_level || 120),
        bmi: Number(form.bmi || 25),
        smoking_status: form.smoking_status || "never smoked"
      };

      const res = await API.post("/predict/stroke", finalData);
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
        <h1>🧠 Stroke Prediction</h1>
        <p className="subtitle">Basic details first. Add lifestyle info for better confidence.</p>

        <form className="smart-form" onSubmit={submit}>
          <h3>Basic Inputs</h3>

          <label>Age</label>
          <input type="number" name="age" required onChange={change} />

          <label>Gender</label>
          <select name="gender" onChange={change}>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>

          <label>Hypertension</label>
          <select name="hypertension" onChange={change}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>

          <label>Average Glucose Level</label>
          <input type="number" name="avg_glucose_level" required onChange={change} />

          <label>BMI</label>
          <input type="number" step="0.1" name="bmi" required onChange={change} />

          <button
            type="button"
            className="secondary-btn"
            onClick={() => setShowMore(!showMore)}
          >
            {showMore ? "Hide Advanced Fields" : "Add More Details"}
          </button>

          {showMore && (
            <>
              <h3>Advanced Inputs</h3>

              <label>Heart Disease</label>
              <select name="heart_disease" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <label>Ever Married</label>
              <select name="ever_married" onChange={change}>
                <option value="Yes">Yes</option>
                <option value="No">No</option>
              </select>

              <label>Work Type</label>
              <select name="work_type" onChange={change}>
                <option value="Private">Private</option>
                <option value="Self-employed">Self-employed</option>
                <option value="Govt_job">Government</option>
                <option value="children">Children</option>
              </select>

              <label>Residence Type</label>
              <select name="Residence_type" onChange={change}>
                <option value="Urban">Urban</option>
                <option value="Rural">Rural</option>
              </select>

              <label>Smoking Status</label>
              <select name="smoking_status" onChange={change}>
                <option value="never smoked">Never Smoked</option>
                <option value="formerly smoked">Formerly Smoked</option>
                <option value="smokes">Smokes</option>
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
          </>
        )}
      </div>
    </div>
  );
}

export default StrokeForm;