import prisma from '../config/db';
import { LoanStatus } from '@prisma/client';

export const checkoutBook = async (userId: string, bookId: string) => {
  const book = await prisma.book.findUnique({ where: { id: bookId } });
  if (!book || book.status !== 'AVAILABLE') {
    throw { status: 400, message: 'Book is not available for checkout' };
  }

  const dueDate = new Date();
  dueDate.setDate(dueDate.getDate() + 14); // 2 weeks

  await prisma.$transaction([
    prisma.book.update({
      where: { id: bookId },
      data: { status: 'CHECKED_OUT' },
    }),
    prisma.loan.create({
      data: {
        userId,
        bookId,
        dueDate,
        status: 'ACTIVE',
      },
    }),
  ]);

  return { message: 'Book checked out successfully', dueDate };
};

export const renewLoan = async (userId: string, bookId: string) => {
  const loan = await prisma.loan.findFirst({
    where: {
      userId,
      bookId,
      status: 'ACTIVE',
    },
  });

  if (!loan) throw { status: 404, message: 'Loan record not found' };

  const newDueDate = new Date(loan.dueDate);
  newDueDate.setDate(newDueDate.getDate() + 14);

  await prisma.loan.update({
    where: { id: loan.id },
    data: { dueDate: newDueDate },
  });

  return { message: 'Loan renewed successfully', newDueDate };
};

export const returnBook = async (userId: string, bookId: string) => {
  const loan = await prisma.loan.findFirst({
    where: {
      userId,
      bookId,
      status: 'ACTIVE',
    },
  });

  if (!loan) throw { status: 404, message: 'Active loan not found' };

  await prisma.$transaction([
    prisma.book.update({
      where: { id: bookId },
      data: { status: 'AVAILABLE' },
    }),
    prisma.loan.update({
      where: { id: loan.id },
      data: { status: 'RETURNED', returnedAt: new Date() },
    }),
  ]);

  return { message: 'Book returned successfully' };
};

export const viewUserLoans = async (userId: string) => {
  const loans = await prisma.loan.findMany({
    where: { userId },
    include: { book: true },
    orderBy: { createdAt: 'desc' },
  });

  return loans;
};