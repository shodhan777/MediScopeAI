import { useState } from "react";
import API from "../services/api";
import RiskCard from "../components/RiskCard";
import DiseaseXAI from "../components/DiseaseXAI";
import "../styles/Form.css";

function DiabetesForm() {
  const [form, setForm] = useState({
    Pregnancies: "",
    Glucose: "",
    BloodPressure: "",
    SkinThickness: "",
    Insulin: "",
    BMI: "",
    DiabetesPedigreeFunction: "",
    Age: ""
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
        Pregnancies: Number(form.Pregnancies || 0),
        Glucose: Number(form.Glucose || 120),
        BloodPressure: Number(form.BloodPressure || 80),
        SkinThickness: Number(form.SkinThickness || 20),
        Insulin: Number(form.Insulin || 80),
        BMI: Number(form.BMI || 25),
        DiabetesPedigreeFunction: Number(form.DiabetesPedigreeFunction || 0.5),
        Age: Number(form.Age || 40)
      };

      const res = await API.post("/predict/diabetes", finalData);
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
        <h1>🩸 Diabetes Prediction</h1>
        <p className="subtitle">Enter basic values first. Add more for better confidence.</p>

        <form className="smart-form" onSubmit={submit}>
          <h3>Basic Inputs</h3>

          <label>Glucose Level (70 - 250)</label>
          <input type="number" name="Glucose" required onChange={change} />

          <label>Blood Pressure</label>
          <input type="number" name="BloodPressure" required onChange={change} />

          <label>BMI (15 - 60)</label>
          <input type="number" step="0.1" name="BMI" required onChange={change} />

          <label>Age</label>
          <input type="number" name="Age" required onChange={change} />

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

              <label>Pregnancies</label>
              <input type="number" name="Pregnancies" onChange={change} />

              <label>Skin Thickness</label>
              <input type="number" name="SkinThickness" onChange={change} />

              <label>Insulin</label>
              <input type="number" name="Insulin" onChange={change} />

              <label>Diabetes Pedigree Function</label>
              <input type="number" step="0.01" name="DiabetesPedigreeFunction" onChange={change} />
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

export default DiabetesForm;