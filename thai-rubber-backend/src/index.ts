import express, { Application } from "express";
import lineLoginRouter from "./routes/login"; // Ensure this is a TypeScript file or compiled JS
import lineUserProfile from "./routes/line-profile";
import user from "./routes/user";
import adaptive from "./routes/adaptive";
import npk from "./routes/npk";
import notification from "./routes/notifications";
import database from "./routes/database";
import axios from "axios";

const cors = require("cors");

const app: Application = express();
const port: number = 3000;
app.use(
  cors({ origin: ["http://localhost:4200", "https://rd-snap.vercel.app"] })
);
// Middleware for parsing JSON
app.use(express.json());

// Mount the router at the /line endpoint
app.use("/api", lineLoginRouter);
app.use("/api", lineUserProfile);
app.use("/api", user);
app.use("/api", adaptive);
app.use("/api", npk);
app.use("/api", notification);
app.use("/api", database);

async function loopNPK() {
  try {
    // Generate random values for each parameter within their defined ranges
    const humidity = 30 + (Math.random() * 2 - 1) * 0.10 * 30; // 30 ± 10%
    const n = 15 + (Math.random() * 2 - 1) * 0.15 * 15;        // 15 ± 15%
    const p = 16 + (Math.random() * 2 - 1) * 0.21 * 16;        // 16 ± 21%
    const k = 55 + (Math.random() * 2 - 1) * 0.25 * 55;        // 55 ± 25%
    const ph = 6.5 + (Math.random() * 2 - 1) * 0.08 * 6.5;     // 6.5 ± 8%

    const result = await axios.post("http://localhost:3000/api/v1/soil/post", {
      N: parseFloat(n.toFixed(1)),              // Round to 2 decimal places
      P: parseFloat(p.toFixed(1)),              // Round to 2 decimal places
      K: parseFloat(k.toFixed(1)),              // Round to 2 decimal places
      PH: parseFloat(ph.toFixed(1)),            // Round to 2 decimal places
      Humidity: parseFloat(humidity.toFixed(1)), // Round to 2 decimal places
    });

    // console.log("Data sent successfully:", result.data);
  } catch (error) {
    console.error("Error sending data to /api/v1/soil/post:", error);
  }

}

// Start the server
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);

  setInterval(loopNPK, 1000 * 60);
});
