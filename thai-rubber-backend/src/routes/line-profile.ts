import { Router, Request, Response, NextFunction } from "express";
import axios from "axios";
import { UserProfile } from "../models/line-profile";

const router: Router = Router();

// router.post("/profile/me", async (req: Request, res: Response, next: NextFunction)  => {
//   try {
//     const authHeader = req.headers.authorization;
//     if (!authHeader) {
//       return res.status(401).json({ error: "Authorization header is missing" });
//     }
//     const token = authHeader.split(" ")[1];

//     const response = await axios.post(
//       "https://api.line.me/v2/profile",
//       {},
//       {
//         headers: {
//           Authorization: `Bearer ${token}`,
//         },
//       }
//     );

//     const result: UserProfile = response.data;

//     res.json({ status: response.status, profile: result });
//   } catch (error: any) {
//     console.error("Error fetching profile:", error.response?.data || error);
//     res.status(500).json({ error: "Failed to fetch profile" });
//   }
// });

router.get(
  "/profile/me",
  async (req: Request, res: Response, next: NextFunction): Promise<any> => {
    try {
      // รับ token จาก headers
      const authHeader = req.headers.authorization;

      // ตรวจสอบว่ามี token หรือไม่
      if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return res
          .status(401)
          .json({ error: "Authorization header is missing" });
      }

      const token = authHeader.split(" ")[1]; // ดึง token

      // เรียก LINE Profile API
      const response = await axios.post(
        "https://api.line.me/v2/profile",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const result: UserProfile = response.data;

      // ส่งข้อมูลโปรไฟล์กลับไปยัง client
      res.json({ status: response.status, profile: result });
    } catch (error: any) {
      next(error); // ส่ง error ไปยัง middleware ถัดไป
    }
  }
);

export default router;
