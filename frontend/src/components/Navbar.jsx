import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>MediScope AI</h2>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/heart">Heart</Link>
        <Link to="/diabetes">Diabetes</Link>
        <Link to="/stroke">Stroke</Link>
        <Link to="/predict-all">Predict All</Link>
      </div>
    </nav>
  );
}

export default Navbar;