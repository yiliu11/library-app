import express, { Application } from "express";
import cors from "cors";
import { env } from "./utils/env";
import requestRoutes from "./routes/request.routes";
import { errorHandler } from "./middlewares/errorHandler";

const app: Application = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/requests", requestRoutes);

// Error Handler
app.use(errorHandler);

const PORT = env.PORT || 4004;

app.listen(PORT, () => {
  console.log(`📚 Book Request Service running on port ${PORT}`);
});
