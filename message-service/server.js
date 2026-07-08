const express = require("express");
const app = express();

const PORT = 4000;

app.get("/message", (req, res) => {
  const name = req.query.name;

  res.json({
    message: `Hello ${name}! 👋`
  });
});

app.listen(PORT, () => {
  console.log(`Message Service is running on port ${PORT}`);
});