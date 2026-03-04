import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';
import loanRoutes from './routes/loan.routes';
import errorHandler from './middlewares/errorHandler';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 4002;

app.use(cors());
app.use(express.json());

// Routes
app.use('/api/loans', loanRoutes);

// Error handler
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Checkout & Renewal Service running on port ${PORT}`);
});
