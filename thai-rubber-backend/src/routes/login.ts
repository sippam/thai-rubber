import { Router, Request, Response } from "express";
import dotenv from "dotenv";
import pool from "../config/database";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

dotenv.config();

const router: Router = Router();

router.post("/register", async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password, name, tel, position } = req.body;

    // Validate input fields
    if (!email || !password || !name || !tel || !position) {
      res
        .status(400)
        .json({ message: "All fields are required.", status: 400 });
      return;
    }

    // Check if email already exists
    const [existingUser]: any = await pool.query(
      "SELECT email FROM officer WHERE email = ?",
      [email]
    );

    if (existingUser.length > 0) {
      res
        .status(400)
        .json({ message: "Email already registered.", status: 400 });
      return;
    }

    // Hash password
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Insert user into database
    const [result]: any = await pool.query(
      "INSERT INTO officer (email, password, name, tel, position) VALUES (?, ?, ?, ?, ?)",
      [email, hashedPassword, name, tel, position]
    );

    res.status(201).json({
      message: "User registered successfully",
      status: 201,
    });
  } catch (error) {
    console.error("Error registering user:", error);
    res.status(500).json({ message: "Server error", status: 500 });
  }
});

router.post("/login", async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password } = req.body;

    // Check if email exists in the database
    const [existUser]: any = await pool.query(
      "SELECT * FROM officer WHERE email = ?",
      [email]
    );

    if (existUser.length === 0) {
      res.status(400).json({ message: "Email not found", status: 400 });
      return; // Stop further execution
    }

    // Get stored hashed password
    const user = existUser[0]; // Get user details
    const hashedPassword = user.password;

    // Compare provided password with stored hashed password
    const isMatch = await bcrypt.compare(password, hashedPassword);

    if (!isMatch) {
      res.status(400).json({ message: "Invalid password", status: 400 });
      return; // Stop further execution
    }

    // Optional: Generate JWT Token for Authentication
    const token = jwt.sign(
      { id: user.id, email: user.email }, // Payload
      process.env.JWT_SECRET || "secret", // Secret key
      { expiresIn: "30d" } // Token expiry
    );

    // Successful login response
    res.status(200).json({
      message: "Login successful",
      status: 200,
      token, // Return token to the client
      data: {
        id: user.id,
        email: user.email,
        name: user.name,
        tel: user.tel,
        position: user.position,
      },
    });
  } catch (error) {
    console.error("Login error:", error);
    res.status(500).json({ message: "Server error", status: 500 });
  }
});

export default router;
