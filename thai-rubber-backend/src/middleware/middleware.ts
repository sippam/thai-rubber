import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";

dotenv.config();
// Extend Request interface to include 'user'
interface CustomRequest extends Request {
  user?: any;
}

export const authenticateJWT = (
  req: CustomRequest,
  res: Response,
  next: NextFunction
): void => {
  const authHeader = req.headers.authorization;

  // Check if Authorization header exists
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    res.status(401).json({ message: "Unauthorized" }); // Send response and stop further processing
    return; // Exit function
  }

  const token = authHeader.split(" ")[1]; // Extract token from header

  try {
    // Verify and decode token
    const decoded = jwt.verify(token, process.env.JWT_SECRET || "secret");
    req.user = decoded; // Attach user data to request
    next(); // Proceed to next middleware
  } catch (error) {
    res.status(403).json({ message: "Forbidden" }); // Invalid or expired token
  }
};
