const express = require("express");
const router = express.Router();

const {
  predictHeart,
  predictDiabetes,
  predictStroke,
  predictAll
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

module.exports = router;