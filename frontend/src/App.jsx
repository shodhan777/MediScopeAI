import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";

import Home from "./pages/Home";
import HeartForm from "./pages/HeartForm";
import DiabetesForm from "./pages/DiabetesForm";
import StrokeForm from "./pages/StrokeForm";
import PredictAll from "./pages/PredictAll";

function App() {
  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/heart" element={<HeartForm />} />
        <Route path="/diabetes" element={<DiabetesForm />} />
        <Route path="/stroke" element={<StrokeForm />} />
        <Route path="/predict-all" element={<PredictAll />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;