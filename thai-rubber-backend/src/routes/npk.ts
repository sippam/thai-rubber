import { Router, Request, Response } from "express";
import pool from "../config/database";

const router: Router = Router();

router.post("/v1/soil/post", async (req, res) => {
  console.log(req.body);
  const { N, P, K, PH, Humidity } = req.body;

  const sql = `
        INSERT INTO npk (n, p, k, ph, humidity) 
        VALUES (?, ?, ?, ?, ?)
      `;
      
  await pool.query(sql, [N, P, K, PH, Humidity]);

  res.status(200).json({ message: "success", data: JSON.stringify(req.body) });
});

export default router;
