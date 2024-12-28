import { Router, Request, Response } from "express";
import { authenticateJWT } from "../middleware/middleware";
import { Middleware } from "../models/middleware";
import pool from "../config/database";

const router: Router = Router();

router.get(
  "/user/me",
  authenticateJWT,
  async (req: Request, res: Response): Promise<void> => {
    try {
      // Access user info from the token via the custom request type
      const user: Middleware = (req as any).user;

      const [result]: any = await pool.query(
        "SELECT email, name, position, tel FROM officer WHERE email = ?",
        [user.email]
      );

      res.status(200).json({
        status: 200,
        data: result[0], // Send the decoded user details
      });
    } catch (error) {
      console.error("Error fetching user:", error);
      res.status(500).json({ message: "Server error" });
    }
  }
);

export default router;
