import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="container">
      <h1>MediScope AI</h1>
      <p>Unified Multi-Disease Prediction System</p>

      <div className="grid">
        <Link to="/heart">Heart Disease</Link>
        <Link to="/diabetes">Diabetes</Link>
        <Link to="/stroke">Stroke</Link>
        <Link to="/predict-all">Predict All</Link>
      </div>
    </div>
  );
}

export default Home;