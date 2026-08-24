import React, { useState, useRef } from "react";
import API from "../services/api";
import "../styles/AdvancedFeatures.css";

function HeartSimulator({ result, initialData }) {
  const [simData, setSimData] = useState({
    trestbps: initialData?.trestbps || 120,
    chol: initialData?.chol || 200,
    thalach: initialData?.thalach || 150,
  });

  const [liveResult, setLiveResult] = useState({
    risk_score: result?.risk_score || 0,
    risk_level: result?.risk_level || "Low",
  });
  const [loadingSim, setLoadingSim] = useState(false);
  const timeoutRef = useRef(null);

  if (!result || !result.simulation || !initialData) {
    return null;
  }

  const handleSliderChange = (e) => {
    const { name, value } = e.target;
    const numVal = Number(value);
    const updatedData = { ...simData, [name]: numVal };
    setSimData(updatedData);

    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    timeoutRef.current = setTimeout(async () => {
      try {
        setLoadingSim(true);
        const payload = { ...initialData, ...updatedData };
        const res = await API.post("/predict/heart", payload);
        if (res.data) {
          setLiveResult({
            risk_score: res.data.risk_score,
            risk_level: res.data.risk_level,
          });
        }
      } catch (err) {
        console.error("Live simulation error:", err);
      } finally {
        setLoadingSim(false);
      }
    }, 500);
  };

  const getColor = (level) => {
    if (level === "High") return "red";
    if (level === "Medium") return "orange";
    return "green";
  };

  const untreated = result.simulation.untreated;
  const treated = result.simulation.treated;
  const livePercent = (liveResult.risk_score * 100).toFixed(0);

  return (
    <div className="simulator-container">
      <h2>🔥 Core Innovation: Real-Time Risk Evolution & Patient Simulation</h2>
      <p className="sim-intro">
        Explore clinical prognostic projections and adjust vital signs in real
        time to evaluate therapeutic impacts.
      </p>

      {/* Scenario Simulation Section */}
      <div className="scenarios-grid">
        <div className="scenario-card untreated">
          <div className="scenario-header">
            <h4>⚠️ Untreated / Worsening Trajectory</h4>
            <span className={`badge ${getColor(untreated.risk_level)}`}>
              {untreated.risk_level} Risk
            </span>
          </div>
          <p className="scenario-score">
            <strong>Projected Risk Score:</strong>{" "}
            {(untreated.risk_score * 100).toFixed(0)}%
          </p>
          <div className="progress">
            <div
              className={`progress-fill ${getColor(untreated.risk_level)}`}
              style={{ width: `${(untreated.risk_score * 100).toFixed(0)}%` }}
            ></div>
          </div>
          <p className="scenario-details">{untreated.details}</p>
        </div>

        <div className="scenario-card treated">
          <div className="scenario-header">
            <h4>🌿 Optimal Treatment & Lifestyle Intervention</h4>
            <span className={`badge ${getColor(treated.risk_level)}`}>
              {treated.risk_level} Risk
            </span>
          </div>
          <p className="scenario-score">
            <strong>Target Risk Score:</strong>{" "}
            {(treated.risk_score * 100).toFixed(0)}%
          </p>
          <div className="progress">
            <div
              className={`progress-fill ${getColor(treated.risk_level)}`}
              style={{ width: `${(treated.risk_score * 100).toFixed(0)}%` }}
            ></div>
          </div>
          <p className="scenario-details">{treated.details}</p>
        </div>
      </div>

      {/* Live Interactive Sandbox */}
      <div className="sandbox-section">
        <h3>⚡ Real-Time Interactive Risk Sandbox</h3>
        <p className="sandbox-subtitle">
          Adjust the patient's simulated parameters below using the interactive
          sliders to observe immediate dynamic shifts in cardiovascular risk:
        </p>

        <div className="sandbox-content">
          <div className="sliders-column">
            <div className="slider-group">
              <label>
                Resting Blood Pressure:{" "}
                <span className="slider-val">{simData.trestbps} mmHg</span>
              </label>
              <input
                type="range"
                name="trestbps"
                min="90"
                max="200"
                step="2"
                value={simData.trestbps}
                onChange={handleSliderChange}
              />
              <div className="slider-labels">
                <span>90 (Normal)</span>
                <span>140 (Borderline)</span>
                <span>200 (Severe)</span>
              </div>
            </div>

            <div className="slider-group">
              <label>
                Serum Cholesterol:{" "}
                <span className="slider-val">{simData.chol} mg/dL</span>
              </label>
              <input
                type="range"
                name="chol"
                min="120"
                max="450"
                step="5"
                value={simData.chol}
                onChange={handleSliderChange}
              />
              <div className="slider-labels">
                <span>120 (Optimal)</span>
                <span>200 (Borderline)</span>
                <span>450 (High Risk)</span>
              </div>
            </div>

            <div className="slider-group">
              <label>
                Max Heart Rate on Exertion:{" "}
                <span className="slider-val">{simData.thalach} bpm</span>
              </label>
              <input
                type="range"
                name="thalach"
                min="80"
                max="210"
                step="5"
                value={simData.thalach}
                onChange={handleSliderChange}
              />
              <div className="slider-labels">
                <span>80 (Low Reserve)</span>
                <span>150 (Average)</span>
                <span>210 (High Capacity)</span>
              </div>
            </div>
          </div>

          <div className="live-meter-column">
            <div
              className={`live-meter-card ${getColor(liveResult.risk_level)}`}
            >
              <h4>Dynamic Simulated Risk</h4>
              <div className="live-percentage">
                {loadingSim ? "..." : `${livePercent}%`}
              </div>
              <div className={`badge ${getColor(liveResult.risk_level)}`}>
                {liveResult.risk_level} Risk Level
              </div>
              <div className="progress live-progress">
                <div
                  className={`progress-fill ${getColor(liveResult.risk_level)}`}
                  style={{ width: `${livePercent}%` }}
                ></div>
              </div>
              <p className="meter-note">
                Powered by MediScope AI live inference engine.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HeartSimulator;
