import { createLogger, transports, format } from 'winston';
import { env } from '../config/env';

const { combine, timestamp, printf, colorize, errors } = format;

const logFormat = printf(({ level, message, timestamp, stack }) => {
  return `${timestamp} [${level}]: ${stack || message}`;
});

export const logger = createLogger({
  level: env.LOG_LEVEL,
  format: combine(
    colorize(),
    timestamp(),
    errors({ stack: true }),
    logFormat
  ),
  transports: [new transports.Console()],
});
