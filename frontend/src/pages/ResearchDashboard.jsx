import { useState, useEffect } from "react";
import axios from "axios";
import "../styles/Form.css";

function ResearchDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [formData, setFormData] = useState({
    heart: {
      age: "", sex: "", cp: "", trestbps: "", chol: "",
      fbs: "", restecg: "", thalach: "", exang: "",
      oldpeak: "", slope: "", ca: "", thal: ""
    },
    diabetes: {
      Pregnancies: "", Glucose: "", BloodPressure: "", SkinThickness: "",
      Insulin: "", BMI: "", DiabetesPedigreeFunction: "", Age: ""
    },
    stroke: {
      gender: "", age: "", hypertension: "", heart_disease: "",
      ever_married: "", work_type: "", Residence_type: "",
      avg_glucose_level: "", bmi: "", smoking_status: ""
    }
  });
  
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch metrics
    axios.get("http://localhost:5001/api/research/metrics")
      .then(res => setMetrics(res.data))
      .catch(err => console.error("Metrics load error", err));
  }, []);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post("http://localhost:5001/api/predict/research/all", formData);
      setResults(res.data);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to fetch prediction");
    } finally {
      setLoading(false);
    }
  };

  const populateDummyData = () => {
    setFormData({
      heart: {
        age: 63, sex: 1, cp: 3, trestbps: 145, chol: 233,
        fbs: 1, restecg: 0, thalach: 150, exang: 0,
        oldpeak: 2.3, slope: 0, ca: 0, thal: 1
      },
      diabetes: {
        Pregnancies: 6, Glucose: 148, BloodPressure: 72, SkinThickness: 35,
        Insulin: 0, BMI: 33.6, DiabetesPedigreeFunction: 0.627, Age: 50
      },
      stroke: {
        gender: "Male", age: 67, hypertension: 0, heart_disease: 1,
        ever_married: "Yes", work_type: "Private", Residence_type: "Urban",
        avg_glucose_level: 228.69, bmi: 36.6, smoking_status: "formerly smoked"
      }
    });
  };

  return (
    <div className="form-container" style={{ maxWidth: '1000px', margin: '40px auto', padding: '30px', background: '#ffffff', borderRadius: '12px', boxShadow: '0 10px 25px rgba(0,0,0,0.05)' }}>
      <h2 style={{color: '#8b5cf6', fontSize: '2rem', marginBottom: '10px'}}>Smart Disease Risk Predictor</h2>
      <p style={{color: '#64748b', fontSize: '1.1rem', marginBottom: '30px'}}>
        Our advanced AI looks at your health data to predict the risk of Heart Disease, Diabetes, and Stroke all at once. 
        It explains exactly why it made its prediction and will let a human doctor know if it is unsure.
      </p>
      
      {metrics && (
        <div style={{ background: '#f8fafc', padding: '20px', borderRadius: '12px', marginBottom: '30px', border: '1px solid #e2e8f0' }}>
          <h3 style={{color: '#334155', marginTop: '0'}}>AI Accuracy Scores</h3>
          <p style={{color: '#64748b', fontSize: '0.9rem', marginBottom: '15px'}}>How well our AI performs compared to standard models.</p>
          <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
            {Object.keys(metrics).map(k => (
              <div key={k} style={{ border: '1px solid #e2e8f0', padding: '10px', borderRadius: '4px', minWidth: '200px' }}>
                <h4 style={{margin: '0 0 10px 0', color: '#0f172a'}}>{k}</h4>
                <div style={{color: '#475569'}}><strong>Overall Accuracy (ROC-AUC):</strong> {(metrics[k]["ROC-AUC"] * 100).toFixed(1)}%</div>
                <div style={{color: '#475569'}}><strong>Reliability Score (F1):</strong> {(metrics[k]["F1"] * 100).toFixed(1)}%</div>
                <div style={{color: '#475569'}}><strong>Error Rate (Brier):</strong> {(metrics[k]["Brier"]).toFixed(3)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'flex', gap: '15px', marginBottom: '30px' }}>
        <button className="btn" style={{ padding: '12px 24px', fontSize: '1rem', background: '#e2e8f0', color: '#0f172a' }} onClick={populateDummyData}>
          Load Example Patient
        </button>
        <button className="btn" style={{ padding: '12px 24px', fontSize: '1rem', background: '#8b5cf6', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', boxShadow: '0 4px 6px rgba(139, 92, 246, 0.25)' }} onClick={handlePredict} disabled={loading}>
          {loading ? "Analyzing Health Data..." : "Run AI Health Check"}
        </button>
      </div>

      {error && <div style={{ color: '#b91c1c', background: '#fef2f2', padding: '15px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #f87171' }}><strong>Error:</strong> {error} <br/>(Please make sure your Backend and AI servers are running)</div>}

      {results && (
        <div style={{ marginTop: '30px' }}>
          <h3 style={{color: '#1e293b', fontSize: '1.5rem', marginBottom: '20px'}}>Health Analysis Results</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
            {Object.keys(results).map(disease => (
              <div key={disease} style={{
                background: results[disease].abstained ? '#fee2e2' : '#ecfdf5',
                border: '1px solid #ccc', padding: '15px', borderRadius: '8px'
              }}>
                <h4 style={{ textTransform: 'capitalize', margin: '0 0 15px 0', fontSize: '1.25rem', color: '#1e293b', borderBottom: '1px solid #cbd5e1', paddingBottom: '10px' }}>{disease} Risk</h4>
                <div style={{ fontSize: '28px', fontWeight: 'bold', color: results[disease].risk_score > 0.5 ? '#b91c1c' : '#15803d' }}>
                  {(results[disease].risk_score * 100).toFixed(1)}%
                </div>
                
                <div style={{ margin: '15px 0', padding: '12px', background: 'white', borderRadius: '6px', border: '1px solid #e2e8f0' }}>
                  <strong style={{color: '#334155'}}>AI Confidence Level:</strong><br/>
                  <span style={{
                    color: results[disease].confidence === 'LOW' ? '#dc2626' : 
                           results[disease].confidence === 'MEDIUM' ? '#d97706' : '#16a34a',
                    fontWeight: 'bold',
                    fontSize: '1.1rem'
                  }}>{results[disease].confidence}</span>
                  <div style={{fontSize: '0.85rem', color: '#64748b', marginTop: '5px'}}>
                    (Uncertainty score: {results[disease].uncertainty_std.toFixed(3)})
                  </div>
                </div>

                {results[disease].abstained ? (
                  <div style={{ color: '#991b1b', fontWeight: 'bold', background: '#fee2e2', padding: '10px', borderRadius: '6px' }}>
                    ⚠️ The AI is not confident enough to make a prediction. A human doctor must review this.
                  </div>
                ) : (
                  <div>
                    <strong style={{ color: '#16a34a' }}>✅ The AI is confident in this prediction.</strong>
                    <div style={{ marginTop: '15px' }}>
                      <strong style={{color: '#334155'}}>Why did the AI predict this?</strong>
                      <ul style={{ paddingLeft: '20px', fontSize: '0.95rem', marginTop: '10px', color: '#475569' }}>
                        {results[disease].top_factors.map((f, i) => (
                          <li key={i} style={{marginBottom: '5px'}}>
                            <strong>{f.feature.replace(/_/g, ' ')}</strong> 
                            <span style={{ color: f.direction === 'increases_risk' ? '#dc2626' : '#16a34a', fontWeight: 'bold' }}>
                               {f.direction === 'increases_risk' ? ' increased the risk' : ' lowered the risk'}
                            </span>
                            <span style={{fontSize: '0.8rem', color: '#94a3b8'}}> (impact: {f.impact.toFixed(2)})</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default ResearchDashboard;
