const { body } = require("express-validator");

exports.heartValidation = [
  body("age").isNumeric().withMessage("Age must be a number").isFloat({ min: 1, max: 120 }),
  body("sex").isNumeric(),
  body("trestbps").isNumeric().isFloat({ min: 50, max: 250 }),
  body("chol").isNumeric().isFloat({ min: 50, max: 600 })
];

exports.diabetesValidation = [
  body("Glucose").isNumeric().isFloat({ min: 30, max: 400 }),
  body("BloodPressure").isNumeric().isFloat({ min: 30, max: 220 }),
  body("BMI").isNumeric().isFloat({ min: 10, max: 80 }),
  body("Age").isNumeric().isFloat({ min: 1, max: 120 })
];

exports.strokeValidation = [
  body("age").isNumeric().isFloat({ min: 1, max: 120 }),
  body("avg_glucose_level").isNumeric().isFloat({ min: 30, max: 350 }),
  body("bmi").isNumeric().isFloat({ min: 10, max: 80 })
];