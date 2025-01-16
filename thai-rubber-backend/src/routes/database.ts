import { Router, Request, Response, NextFunction } from "express";
import pool from "../config/database";
const router: Router = Router();
import fs from "fs";
import path from "path";
import archiver from "archiver";
import { authenticateJWT } from "../middleware/middleware";
import { parse } from "json2csv";

router.get(
  "/count-picture",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { disease, sevirity } = req.query;

      const sql = `
        SELECT COUNT(*) AS total 
        FROM uploads 
        NATURAL JOIN weather_disease 
        WHERE disease LIKE ? 
        ${sevirity ? "AND sevirity = ?" : ""}
      `;

      const queryParams: any = [`%${disease}%`];

      // เพิ่ม `sevirity` ใน queryParams ถ้ามีค่า
      if (sevirity) {
        queryParams.push(Number(sevirity));
      }

      const [result]: any = await pool.query(sql, queryParams);

      res.status(200).json({
        status: 200,
        data: result[0].total,
      });
    } catch (error) {
      next(error);
    }
  }
);

router.get(
  "/download-zip",
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      // ดึง path ของไฟล์ทั้งหมดจากฐานข้อมูล
      const [rows]: any = await pool.query("SELECT path FROM uploads");

      if (!rows || rows.length === 0) {
        // หากไม่มีไฟล์ในฐานข้อมูล ส่ง response 404
        res.status(404).json({
          status: 404,
          message: "No files found",
        });
        return;
      }

      // ตั้งชื่อไฟล์ ZIP
      const zipFileName = "uploads.zip";

      // สร้าง write stream สำหรับบีบอัดไฟล์
      const output = fs.createWriteStream(zipFileName);
      const archive = archiver("zip", { zlib: { level: 9 } }); // บีบอัดสูงสุด

      // กำหนดให้ archive เขียนข้อมูลไปยัง output stream
      archive.pipe(output);

      // ระบุเส้นทางหลักไปยัง `uploads` ที่อยู่นอกโฟลเดอร์ backend
      const baseUploadsPath = path.resolve(
        __dirname,
        "../../../thai_rubber_line"
      );

      // เพิ่มไฟล์เข้าไปใน archive
      rows.forEach((row: any) => {
        const filePath = path.join(baseUploadsPath, row.path); // ระบุ path แบบสมบูรณ์
        if (fs.existsSync(filePath)) {
          archive.file(filePath, { name: path.basename(filePath) }); // เพิ่มไฟล์เข้า ZIP
        } else {
          console.warn(`File not found: ${filePath}`);
        }
      });
      // สร้างไฟล์ ZIP เสร็จสมบูรณ์
      await archive.finalize();

      // เมื่อบีบอัดเสร็จสมบูรณ์ ให้ส่งไฟล์ ZIP ให้ผู้ใช้
      output.on("close", () => {
        res.download(zipFileName, (err) => {
          if (err) {
            next(err); // หากมีข้อผิดพลาดในการดาวน์โหลด
          }

          // ลบไฟล์ ZIP หลังจากส่งออกเสร็จ
          fs.unlinkSync(zipFileName);
        });
      });
    } catch (error) {
      // ส่งข้อผิดพลาดไปยัง middleware จัดการข้อผิดพลาด
      next(error);
    }
  }
);

router.post(
  "/get-all",
  authenticateJWT,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const disease = req.body.disease || ""; // Replace undefined with ''
      const province = req.body.province || "";
      const district = req.body.district || "";
      const tambon = req.body.tambon || "";
      const rubber = req.body.rubber || "";
      const start = req.body.start || "1999-1-1";
      const end = req.body.end || new Date().toISOString();

      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;

      const offset = (page - 1) * limit;

      const sql = `
      SELECT 
      transaction_id, line_name AS name, disease, area, land_type, soil_type, rubber_type, temperature_min, temperature_max, temperature_avg, precipitation_sum, wind_speed, wind_direction, wind_gust, shortwave_radiation_sum, relative_humidity, soil_moisture, sevirity, forecast_7days, forecast_14days, risk, create_at
       FROM weather_disease
      NATURAL JOIN uploads
      NATURAL JOIN address
      NATURAL JOIN plantation
      NATURAL JOIN customers
      WHERE disease LIKE ? 
        AND province LIKE ? 
        AND district LIKE ? 
        AND subdistrict LIKE ? 
        AND rubber_type LIKE ? 
        AND create_at BETWEEN ? AND ?
        LIMIT ? OFFSET ?;
        `;

      const queryParams = [
        `%${disease}%`,
        `%${province}%`,
        `%${district}%`,
        `%${tambon}%`,
        `%${rubber}%`,
        start,
        end,
        limit,
        offset,
      ];

      const [countResult]: any = await pool.query(
        `SELECT COUNT(*) AS total FROM weather_disease
      NATURAL JOIN uploads
      NATURAL JOIN address
      NATURAL JOIN plantation
      NATURAL JOIN customers
      WHERE disease LIKE ? 
        AND province LIKE ? 
        AND district LIKE ? 
        AND subdistrict LIKE ? 
        AND rubber_type LIKE ? 
        AND create_at BETWEEN ? AND ?;`,
        [
          `%${disease}%`,
          `%${province}%`,
          `%${district}%`,
          `%${tambon}%`,
          `%${rubber}%`,
          start,
          end,
        ]
      );

      const totalRows = countResult[0].total;

      const [result] = await pool.query(sql, queryParams);

      res.status(200).json({
        status: 200,
        data: result,
        totalRows,
        totalPages: Math.ceil(totalRows / limit),
        currentPage: page,
        limit: limit,
      });
    } catch (error) {
      next(error);
    }
  }
);

router.post(
  "/download-csv",
  async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const disease = req.body.disease || "";
      const province = req.body.province || "";
      const district = req.body.district || "";
      const tambon = req.body.tambon || "";
      const rubber = req.body.rubber || "";
      const start = req.body.start || "1999-1-1";
      const end = req.body.end || new Date().toISOString();

      const sql = `
      SELECT 
      transaction_id, line_name AS name, disease, area, land_type, soil_type, rubber_type, temperature_min, temperature_max, temperature_avg, precipitation_sum, wind_speed, wind_direction, wind_gust, shortwave_radiation_sum, relative_humidity, soil_moisture, sevirity, forecast_7days, forecast_14days, risk, create_at
      FROM weather_disease
      NATURAL JOIN uploads
      NATURAL JOIN address
      NATURAL JOIN plantation
      NATURAL JOIN customers
      WHERE disease LIKE ? 
        AND province LIKE ? 
        AND district LIKE ? 
        AND subdistrict LIKE ? 
        AND rubber_type LIKE ? 
        AND create_at BETWEEN ? AND ?;
      `;

      const queryParams = [
        `%${disease}%`,
        `%${province}%`,
        `%${district}%`,
        `%${tambon}%`,
        `%${rubber}%`,
        start,
        end,
      ];

      const [result]: any = await pool.query(sql, queryParams);

      if (!result || result.length === 0) {
        res.status(404).json({
          status: 404,
          message: "No data found",
        });
        return;
      }

      // ทำความสะอาดข้อมูล
      const cleanResult = result.map((row: any) => ({
        ...row,
        disease: row.disease.replace(/\n/g, " "), // แทนที่ newline ด้วย space
        create_at: new Date(row.create_at).toLocaleString(), // แปลงวันที่เป็นรูปแบบอ่านง่าย
      }));

      // แปลงข้อมูลเป็น CSV
      const csv = parse(cleanResult, {
        fields: Object.keys(cleanResult[0]),
      });

      // เพิ่ม BOM (\uFEFF) สำหรับภาษาไทย
      const bomCsv = `\uFEFF${csv}`;

      // ส่ง CSV เป็นไฟล์ให้ผู้ใช้
      res.setHeader("Content-Type", "text/csv");
      res.setHeader("Content-Disposition", "attachment; filename=data.csv");
      res.status(200).send(bomCsv);
    } catch (error) {
      next(error);
    }
  }
);

export default router;
