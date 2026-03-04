import { Router } from 'express';
import notificationRouter from './notification.route';

const router = Router();

router.use('/api/notifications', notificationRouter);

export default router;
