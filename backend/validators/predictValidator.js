const { body } = require("express-validator");

exports.heartValidation = [
  body("age").isNumeric(),
  body("sex").isNumeric(),
  body("chol").isNumeric()
];

exports.diabetesValidation = [
  body("Glucose").isNumeric(),
  body("BMI").isNumeric(),
  body("Age").isNumeric()
];

exports.strokeValidation = [
  body("age").isNumeric(),
  body("avg_glucose_level").isNumeric(),
  body("bmi").isNumeric()
];