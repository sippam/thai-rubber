import mysql from "mysql2/promise"; // Import mysql2 with promise support
import dotenv from "dotenv";

dotenv.config();
// Create a connection pool for better performance
const pool = mysql.createPool({
  host: process.env.DB_HOST, // Replace with your MySQL host (e.g., 127.0.0.1)
  user: process.env.DB_USER, // Replace with your MySQL username
  password: process.env.DB_PASSWORD, // Replace with your MySQL password
  database: process.env.DB_DATABSE, // Replace with your database name
  waitForConnections: true,
  connectionLimit: 10, // Number of connections in the pool
  queueLimit: 0,
});

export default pool;
