import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import bookRoutes from './routes/book.routes';
import { errorHandler } from './middlewares/error.middleware';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5002;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/books', bookRoutes);

// Global Error Handler
app.use(errorHandler);

// Start Server
app.listen(PORT, () => {
  console.log(`Book Catalog Service running on port ${PORT}`);
});
