function RiskCard({ result }) {
  if (!result) return null;

  const percent = (result.risk_score * 100).toFixed(0);

  const getColor = () => {
    if (result.risk_level === "High") return "red";
    if (result.risk_level === "Medium") return "orange";
    return "green";
  };

  return (
    <div className="risk-card">
      <h2>Prediction Result</h2>

      <div className={`badge ${getColor()}`}>
        {result.risk_level} Risk
      </div>

      <p><strong>Risk Score:</strong> {percent}%</p>

      <div className="progress">
        <div
          className={`progress-fill ${getColor()}`}
          style={{ width: `${percent}%` }}
        ></div>
      </div>

      {result.confidence && (
        <p><strong>Confidence:</strong> {result.confidence}</p>
      )}
    </div>
  );
}

export default RiskCard;