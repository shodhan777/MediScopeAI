import { useState } from "react";
import API from "../services/api";
import "../styles/Form.css";

function PredictAll() {
  const [form, setForm] = useState({
    age: "",
    sex: "1",
    trestbps: "",
    chol: "",
    glucose: "",
    bmi: "",
    hypertension: "0"
  });

  const [showMore, setShowMore] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const change = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = {
        heart: {
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
        },

        diabetes: {
          Pregnancies: Number(form.Pregnancies || 0),
          Glucose: Number(form.glucose || 120),
          BloodPressure: Number(form.trestbps || 80),
          SkinThickness: Number(form.SkinThickness || 20),
          Insulin: Number(form.Insulin || 80),
          BMI: Number(form.bmi || 25),
          DiabetesPedigreeFunction: Number(
            form.DiabetesPedigreeFunction || 0.5
          ),
          Age: Number(form.age || 50)
        },

        stroke: {
          gender: form.sex === "1" ? "Male" : "Female",
          age: Number(form.age || 50),
          hypertension: Number(form.hypertension || 0),
          heart_disease: Number(form.heart_disease || 0),
          ever_married: form.ever_married || "Yes",
          work_type: form.work_type || "Private",
          Residence_type: form.Residence_type || "Urban",
          avg_glucose_level: Number(form.glucose || 120),
          bmi: Number(form.bmi || 25),
          smoking_status: form.smoking_status || "never smoked"
        }
      };

      const res = await API.post("/predict/all", payload);

      let filled = 0;
      Object.keys(form).forEach((key) => {
        if (form[key] !== "") filled++;
      });

      let confidence = "Medium";

      if (filled >= 12) confidence = "High";
      else if (filled <= 7) confidence = "Low";

      setResult({
        ...res.data,
        confidence
      });
    } catch (error) {
      alert("Prediction failed. Please try again.");
      console.log(error);
    }

    setLoading(false);
  };

  const ResultCard = ({ title, icon, data }) => (
    <div className="result-card">
      <h2>{icon} {title}</h2>
      <p>
        <strong>Risk Score:</strong>{" "}
        {(data.risk_score * 100).toFixed(0)}%
      </p>
      <p>
        <strong>Risk Level:</strong> {data.risk_level}
      </p>
    </div>
  );

  return (
    <div className="page">
      <div className="form-card">
        <h1>🩺 Full Body Health Screening</h1>

        <p className="subtitle">
          One form predicts Heart Disease, Diabetes, and Stroke.
        </p>

        <form className="smart-form" onSubmit={submit}>
          <h3>Basic Inputs</h3>

          <label>Age</label>
          <input
            type="number"
            name="age"
            required
            onChange={change}
          />

          <label>Gender</label>
          <select name="sex" onChange={change}>
            <option value="1">Male</option>
            <option value="0">Female</option>
          </select>

          <label>Blood Pressure</label>
          <input
            type="number"
            name="trestbps"
            required
            onChange={change}
          />

          <label>Cholesterol</label>
          <input
            type="number"
            name="chol"
            required
            onChange={change}
          />

          <label>Glucose Level</label>
          <input
            type="number"
            name="glucose"
            required
            onChange={change}
          />

          <label>BMI</label>
          <input
            type="number"
            step="0.1"
            name="bmi"
            required
            onChange={change}
          />

          <label>Hypertension</label>
          <select name="hypertension" onChange={change}>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>

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

              <label>Chest Pain Type</label>
              <select name="cp" onChange={change}>
                <option value="0">Typical Angina</option>
                <option value="1">Atypical</option>
                <option value="2">Non-anginal</option>
                <option value="3">Asymptomatic</option>
              </select>

              <label>Heart Disease History</label>
              <select name="heart_disease" onChange={change}>
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>

              <label>Smoking Status</label>
              <select name="smoking_status" onChange={change}>
                <option value="never smoked">Never Smoked</option>
                <option value="formerly smoked">Formerly Smoked</option>
                <option value="smokes">Smokes</option>
              </select>

              <label>Pregnancies</label>
              <input
                type="number"
                name="Pregnancies"
                onChange={change}
              />

              <label>Insulin</label>
              <input
                type="number"
                name="Insulin"
                onChange={change}
              />

              <label>Maximum Heart Rate</label>
              <input
                type="number"
                name="thalach"
                onChange={change}
              />
            </>
          )}

          <button type="submit" disabled={loading}>
            {loading ? "Running Full Analysis..." : "Run Full Screening"}
          </button>
        </form>

        {result && (
          <>
            <div className="dashboard-grid">
              <ResultCard
                title="Heart Disease"
                icon="❤️"
                data={result.heart}
              />

              <ResultCard
                title="Diabetes"
                icon="🩸"
                data={result.diabetes}
              />

              <ResultCard
                title="Stroke"
                icon="🧠"
                data={result.stroke}
              />
            </div>

            <div className="confidence-box">
              <p>
                <strong>Prediction Confidence:</strong>{" "}
                {result.confidence}
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default PredictAll;