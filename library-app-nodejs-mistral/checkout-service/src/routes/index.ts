import { Router } from 'express';
import checkoutRouter from './checkout.route';

const router = Router();

router.use('/api', checkoutRouter);

export default router;
