import { logger } from './logger';

export class InputSanitizer {
  /**
   * Sanitizes a string input to prevent SQL injection and XSS.
   * @param input The input string to sanitize.
   * @returns The sanitized string.
   */
  sanitize(input: string): string {
    if (!input) return input;

    // Basic SQL injection prevention by escaping single quotes
    // Note: This is a simple example. In production, use parameterized queries!
    const sanitized = input.replace(/'/g, "''");

    // Basic XSS prevention by escaping HTML tags
    // Note: For full XSS protection, use a library like DOMPurify on the frontend
    return sanitized.replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  /**
   * Sanitizes an object by sanitizing all string properties.
   * @param obj The object to sanitize.
   * @returns The sanitized object.
   */
  sanitizeObject<T extends Record<string, any>>(obj: T): T {
    if (!obj) return obj;

    const sanitizedObj: any = {};
    for (const key in obj) {
      if (typeof obj[key] === 'string') {
        sanitizedObj[key] = this.sanitize(obj[key]);
      } else {
        sanitizedObj[key] = obj[key];
      }
    }
    return sanitizedObj;
  }
}

export const inputSanitizer = new InputSanitizer();
