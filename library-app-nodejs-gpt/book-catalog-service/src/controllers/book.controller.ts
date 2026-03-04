import { Request, Response, NextFunction } from 'express';
import * as bookService from '../services/book.service';
import { sendResponse } from '../utils/response';

export const getAllBooks = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const books = await bookService.getAllBooks();
    sendResponse(res, 200, 'Books retrieved successfully', books);
  } catch (err) {
    next(err);
  }
};

export const getBookById = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const book = await bookService.getBookById(req.params.id);
    sendResponse(res, 200, 'Book retrieved successfully', book);
  } catch (err) {
    next(err);
  }
};

export const createBook = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const newBook = await bookService.createBook(req.body);
    sendResponse(res, 201, 'Book created successfully', newBook);
  } catch (err) {
    next(err);
  }
};

export const updateBook = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const updatedBook = await bookService.updateBook(req.params.id, req.body);
    sendResponse(res, 200, 'Book updated successfully', updatedBook);
  } catch (err) {
    next(err);
  }
};

export const deleteBook = async (req: Request, res: Response, next: NextFunction) => {
  try {
    await bookService.deleteBook(req.params.id);
    sendResponse(res, 200, 'Book deleted successfully');
  } catch (err) {
    next(err);
  }
};

export const searchBooks = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { query } = req;
    const result = await bookService.searchBooks(query);
    sendResponse(res, 200, 'Search results', result);
  } catch (err) {
    next(err);
  }
};