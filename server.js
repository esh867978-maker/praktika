require("dotenv").config();

const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/config.js", (_req, res) => {
  const apiKey = process.env.OPENWEATHER_API_KEY || "";
  res.type("application/javascript");
  res.send(`window.APP_CONFIG = { apiKey: "${apiKey}" };`);
});

app.use(express.static(path.join(__dirname)));

app.get("*", (_req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

app.listen(PORT, () => {
  console.log(`Weather app running on port ${PORT}`);
});
