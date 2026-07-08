const express = require("express");
const app = express();

const PORT = 3000;

app.get("/", (req, res) => {
  res.send("Backend is running successfully!");
});

app.get("/hello", (req, res) => {
  const name = req.query.name;

  res.json({
    message: `Hello ${name}!`
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

