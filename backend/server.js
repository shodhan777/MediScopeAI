require("dotenv").config();

const express = require("express");
const cors = require("cors");

const logger = require("./middleware/logger");
const errorHandler = require("./middleware/errorMiddleware");

const predictRoutes = require("./routes/predictRoutes");

const app = express();

app.use(cors());
app.use(express.json());
app.use(logger);

app.use("/api", predictRoutes);

app.get("/", (req, res) => {
  res.send("MediScope AI Backend Running");
});

app.use(errorHandler);

const PORT = process.env.PORT || 5001;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});