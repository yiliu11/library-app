import { body, param, query } from 'express-validator';

export const createBookValidator = [
  body('title').isString().withMessage('Title must be a string'),
  body('author').isString().withMessage('Author must be a string'),
  body('genre').optional().isString().withMessage('Genre must be a string'),
  body('publishedYear')
    .optional()
    .isInt({ min: 1000, max: new Date().getFullYear() })
    .withMessage('Published year must be a valid year'),
  body('isbn')
    .optional()
    .isString()
    .withMessage('ISBN must be a string')
];

export const updateBookValidator = [
  param('id').isUUID().withMessage('Book ID must be a valid UUID'),
  ...createBookValidator
];

export const getBookByIdValidator = [
  param('id').isUUID().withMessage('Book ID must be a valid UUID')
];

export const deleteBookValidator = [
  param('id').isUUID().withMessage('Book ID must be a valid UUID')
];

export const searchBooksValidator = [
  query('title').optional().isString().withMessage('Title must be a string'),
  query('author').optional().isString().withMessage('Author must be a string'),
  query('keyword').optional().isString().withMessage('Keyword must be a string')
];
