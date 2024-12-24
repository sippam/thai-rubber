import express, { Application } from "express";
import lineLoginRouter from "./routes/line-login"; // Ensure this is a TypeScript file or compiled JS
import lineUserProfile from "./routes/line-profile";
const cors = require("cors");

const app: Application = express();
const port: number = 3000;
app.use(
  cors({ origin: ["http://localhost:4200", "https://rd-snap.vercel.app"] })
);
// Middleware for parsing JSON
app.use(express.json());

// Mount the router at the /line endpoint
app.use("/api/line", lineLoginRouter);
app.use("/api/line", lineUserProfile);

// Start the server
app.listen(port, () => {
  console.log(`App listening at http://localhost:${port}`);
});
