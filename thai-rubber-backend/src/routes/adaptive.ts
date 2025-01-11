import { Router, Request, Response, NextFunction } from "express";
import pool from "../config/database";
import { Adaptive } from "../models/adaptive";
import { FieldPacket, RowDataPacket } from "mysql2";
import { authenticateJWT } from "../middleware/middleware";

const router: Router = Router();

router.get(
  "/adaptive",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      const { disease, from, to } = req.query;

      if (from == "undefined" || to == "undefined") {
        const [rows]: [RowDataPacket[], FieldPacket[]] = await pool.query(
          "SELECT plot_id, accuracy_7_day, accuracy_14_day, accuracy_outbreak, create_at FROM plot WHERE disease = ?",
          [disease]
        );
        res.json({ status: 200, data: rows });
      } else {
        const [rows]: [RowDataPacket[], FieldPacket[]] = await pool.query(
          "SELECT plot_id, accuracy_7_day, accuracy_14_day, accuracy_outbreak, create_at FROM plot WHERE disease = ? AND create_at BETWEEN ? AND ?",
          [disease, from, to]
        );

        res.json({ status: 200, data: rows });
      }
    } catch (error: any) {
      next(error);
    }
  }
);

router.get(
  "/adaptive-table",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      const { disease } = req.query;

      const [rows]: [RowDataPacket[], FieldPacket[]] = await pool.query(
        "SELECT sevirity, true_label_7_day, predicted_label_7_day, accuracy_7_day, true_label_14_day, predicted_label_14_day, accuracy_14_day, true_label_outbreak, predicted_label_outbreak, accuracy_outbreak, create_at FROM adaptive WHERE disease = ?",
        [disease]
      );
      res.json({ status: 200, data: rows });
    } catch (error: any) {
      next(error);
    }
  }
);
export default router;
