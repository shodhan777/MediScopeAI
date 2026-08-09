const errorHandler = (err, req, res, next) => {
  console.error(err.message || err);

  let status = err.status || 500;
  let message = err.message || "Server Error";

  if (err.code === "ECONNREFUSED" || err.message?.includes("connect ECONNREFUSED")) {
    status = 503;
    message = "ML Prediction Service is temporarily unavailable.";
  } else if (err.response && err.response.status) {
    status = err.response.status;
    message = err.response.data?.message || message;
  }

  res.status(status).json({
    success: false,
    message: message
  });
};

module.exports = errorHandler;