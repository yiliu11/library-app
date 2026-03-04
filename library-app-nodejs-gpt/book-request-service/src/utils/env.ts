import dotenv from "dotenv";

dotenv.config();

export const env = {
  PORT: process.env.PORT || 4004,
  DATABASE_URL: process.env.DATABASE_URL as string,
  NODE_ENV: process.env.NODE_ENV || "development",
};

if (!env.DATABASE_URL) {
  throw new Error("DATABASE_URL is not defined in environment variables.");
}
