import React from "react";
import "../styles/AdvancedFeatures.css";

function DiseaseXAI({ result }) {
  if (!result || (!result.smart_alert && !result.xai_insights && !result.recommendations)) {
    return null;
  }

  const getAlertStyle = () => {
    if (result.smart_alert?.includes("CRITICAL")) return "alert-critical";
    if (result.smart_alert?.includes("WARNING")) return "alert-warning";
    return "alert-safe";
  };

  const getImpactBadge = (impact) => {
    if (impact === "High") return <span className="impact-tag high">High Impact</span>;
    if (impact === "Medium") return <span className="impact-tag medium">Medium Impact</span>;
    return <span className="impact-tag low">Low Impact</span>;
  };

  return (
    <div className="xai-container">
      {/* Phase 5: Smart Alert System */}
      {result.smart_alert && (
        <div className={`smart-alert-box ${getAlertStyle()}`}>
          <div className="alert-content">
            <h4>Clinical Decision Support</h4>
            <p>{result.smart_alert}</p>
          </div>
        </div>
      )}

      {/* Phase 6: Explainable AI (XAI) */}
      {result.xai_insights && result.xai_insights.length > 0 && (
        <div className="xai-section">
          <h3>Key Risk Contributing Factors</h3>
          <p className="xai-subtitle">
            Breakdown of physiological features influencing the prediction:
          </p>
          <div className="xai-grid">
            {result.xai_insights.map((item, idx) => (
              <div key={idx} className="xai-card">
                <div className="xai-card-header">
                  <span className="xai-factor-name">{item.factor}</span>
                  {getImpactBadge(item.impact)}
                </div>
                <div className="xai-card-value">
                  <strong>Measured:</strong> {item.value} <em>({item.status})</em>
                </div>
                <p className="xai-desc">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Clinical Decision Support & Recommendations */}
      {result.recommendations && result.recommendations.length > 0 && (
        <div className="cds-recommendations">
          <h3>Clinical Action Plan & Recommendations</h3>
          <ul className="recommendations-list">
            {result.recommendations.map((rec, index) => (
              <li key={index}>
                <span className="rec-icon">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default DiseaseXAI;
