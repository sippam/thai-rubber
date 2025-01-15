import { Request, Router, Response, NextFunction } from "express";
import pool from "../config/database";
import { authenticateJWT } from "../middleware/middleware";

const router: Router = Router();

router.get(
  "/follow-disease",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;

      const offset = (page - 1) * limit;

      const [countResult]: any = await pool.query(
        "SELECT COUNT(*) AS total FROM notifications NATURAL JOIN customers"
      );

      const totalRows = countResult[0].total;

      const [result] = await pool.query(
        "SELECT notification_id, line_name, officer_id, name, disease, risk, status, details, create_at FROM notifications NATURAL JOIN customers LEFT JOIN officer ON notifications.officer_id = officer.id LIMIT ? OFFSET ?",
        [limit, offset]
      );

      res.status(200).json({
        status: 200,
        data: result,
        totalRows, // Add total rows to the response
        totalPages: Math.ceil(totalRows / limit), // Calculate total pages
        currentPage: page,
        limit: limit,
      });
    } catch (error) {
      next(error);
    }
  }
);

router.post(
  "/update-notification",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      const { notification_id, officer_id, status, detail } = req.body;

      const [result] = await pool.query(
        "UPDATE notifications SET officer_id = ?, status = ?, details = ? WHERE notification_id = ?",
        [officer_id, status, detail, notification_id]
      );

      res.status(200).json({
        status: 200,
        message: "Notification updated successfully",
      });
    } catch (error) {
      next(error);
    }
  }
);

router.get(
  "/notification",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      const { id } = req.query;

      const [result]: any = await pool.query(
        "SELECT officer_id, name, status, details FROM notifications LEFT JOIN officer ON notifications.officer_id = officer.id WHERE notification_id = ?",
        [id]
      );

      res.status(200).json({
        status: 200,
        data: result[0],
      });
    } catch (error) {
      next(error);
    }
  }
);

export default router;
