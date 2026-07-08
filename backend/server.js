const cors = require("cors");
const axios = require("axios");
const express = require("express");
const app = express();
app.use(cors());
const PORT = 3000;
const MESSAGE_SERVICE_URL = process.env.MESSAGE_SERVICE_URL;
app.get("/", (req, res) => {
  res.send("Backend is running successfully!");
});

app.get("/hello", async (req, res) => {
  const name = req.query.name;

  try {
   const response = await axios.get(
    `${MESSAGE_SERVICE_URL}/message?name=${name}`
);

    res.json(response.data);
  } catch (error) {
    res.status(500).json({
      message: "Message Service is unavailable."
    });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

