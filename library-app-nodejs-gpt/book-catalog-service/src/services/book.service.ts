import { prisma } from '../prisma/client';
import { Book } from '@prisma/client';
import { NotFoundError } from '../utils/errors';

export const getAllBooks = async (): Promise<Book[]> => {
  return prisma.book.findMany();
};

export const getBookById = async (id: string): Promise<Book> => {
  const book = await prisma.book.findUnique({ where: { id } });
  if (!book) throw new NotFoundError('Book not found');
  return book;
};

export const createBook = async (data: Partial<Book>): Promise<Book> => {
  return prisma.book.create({ data });
};

export const updateBook = async (id: string, data: Partial<Book>): Promise<Book> => {
  const existing = await prisma.book.findUnique({ where: { id } });
  if (!existing) throw new NotFoundError('Book not found');
  return prisma.book.update({ where: { id }, data });
};

export const deleteBook = async (id: string): Promise<void> => {
  const existing = await prisma.book.findUnique({ where: { id } });
  if (!existing) throw new NotFoundError('Book not found');
  await prisma.book.delete({ where: { id } });
};

export const searchBooks = async (query: any): Promise<Book[]> => {
  const { title, author, keyword } = query;
  return prisma.book.findMany({
    where: {
      OR: [
        title ? { title: { contains: title, mode: 'insensitive' } } : undefined,
        author ? { author: { contains: author, mode: 'insensitive' } } : undefined,
        keyword ? {
          OR: [
            { title: { contains: keyword, mode: 'insensitive' } },
            { author: { contains: keyword, mode: 'insensitive' } },
            { genre: { contains: keyword, mode: 'insensitive' } }
          ]
        } : undefined
      ].filter(Boolean)
    }
  });
};