const express = require("express");
const router = express.Router();

const {
  predictHeart,
  predictDiabetes,
  predictStroke,
  predictAll,
  predictResearchAll,
  getResearchMetrics
} = require("../controllers/predictController");

const {
  heartValidation,
  diabetesValidation,
  strokeValidation
} = require("../validators/predictValidator");

router.post("/predict/heart", heartValidation, predictHeart);
router.post("/predict/diabetes", diabetesValidation, predictDiabetes);
router.post("/predict/stroke", strokeValidation, predictStroke);
router.post("/predict/all", predictAll);

router.post("/predict/research/all", predictResearchAll);
router.get("/research/metrics", getResearchMetrics);

module.exports = router;