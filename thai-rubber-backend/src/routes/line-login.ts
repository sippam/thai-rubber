import { Router, Request, Response } from "express";
import axios from "axios";
import dotenv from "dotenv";
import { LineLogin } from "../models/line-login";

dotenv.config();

const router: Router = Router();

router.post("/login", async (req: Request, res: Response) => {
  const code = req.body.code;

  const response = await axios.post(
    "https://api.line.me/oauth2/v2.1/token",
    {
      grant_type: "authorization_code",
      code: code,
      redirect_uri: process.env.LINE_REDIRECT_URI,
      client_id: process.env.LINE_CHANNEL_ID,
      client_secret: process.env.LINE_CHANNEL_SECRET,
    },
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  const result: LineLogin = response.data;
  res.json({ token: result });
});

export default router;
