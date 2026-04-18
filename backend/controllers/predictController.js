const axios = require("axios");
const { validationResult } = require("express-validator");

const ML_API = process.env.ML_API;

const validate = (req) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    const err = new Error("Validation failed");
    err.status = 400;
    err.details = errors.array();
    throw err;
  }
};

exports.predictHeart = async (req, res, next) => {
  try {
    validate(req);

    const response = await axios.post(`${ML_API}/predict/heart`, req.body);
    res.json(response.data);

  } catch (error) {
    next(error);
  }
};

exports.predictDiabetes = async (req, res, next) => {
  try {
    validate(req);

    const response = await axios.post(`${ML_API}/predict/diabetes`, req.body);
    res.json(response.data);

  } catch (error) {
    next(error);
  }
};

exports.predictStroke = async (req, res, next) => {
  try {
    validate(req);

    const response = await axios.post(`${ML_API}/predict/stroke`, req.body);
    res.json(response.data);

  } catch (error) {
    next(error);
  }
};

exports.predictAll = async (req, res, next) => {
  try {
    const response = await axios.post(`${ML_API}/predict/all`, req.body);
    res.json(response.data);

  } catch (error) {
    next(error);
  }
};