import { Request, Response, NextFunction } from 'express';
import prisma from '../prisma/client';
import { BadRequestError, NotFoundError } from '../utils/errors';
import { addDays } from 'date-fns';

const LOAN_DURATION_DAYS = 14;
const MAX_RENEWALS = 2;

export const checkoutBook = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId, bookId } = req.body;

    // Check for existing active loan
    const existingLoan = await prisma.loan.findFirst({
      where: {
        bookId,
        returnDate: null,
      },
    });

    if (existingLoan) {
      throw new BadRequestError('Book is already checked out');
    }

    const loan = await prisma.loan.create({
      data: {
        userId,
        bookId,
        dueDate: addDays(new Date(), LOAN_DURATION_DAYS),
      },
    });

    res.status(201).json({ message: 'Book checked out successfully', loan });
  } catch (error) {
    next(error);
  }
};

export const renewLoan = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId, bookId } = req.body;

    const loan = await prisma.loan.findFirst({
      where: {
        userId,
        bookId,
        returnDate: null,
      },
    });

    if (!loan) throw new NotFoundError('Loan not found');
    if (loan.renewCount >= MAX_RENEWALS) throw new BadRequestError('Renewal limit reached');

    const updatedLoan = await prisma.loan.update({
      where: { id: loan.id },
      data: {
        dueDate: addDays(loan.dueDate, LOAN_DURATION_DAYS),
        renewCount: { increment: 1 },
      },
    });

    res.status(200).json({ message: 'Loan renewed', loan: updatedLoan });
  } catch (error) {
    next(error);
  }
};

export const returnBook = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId, bookId } = req.body;

    const loan = await prisma.loan.findFirst({
      where: {
        userId,
        bookId,
        returnDate: null,
      },
    });

    if (!loan) throw new NotFoundError('Loan not found');

    const returnedLoan = await prisma.loan.update({
      where: { id: loan.id },
      data: { returnDate: new Date() },
    });

    res.status(200).json({ message: 'Book returned', loan: returnedLoan });
  } catch (error) {
    next(error);
  }
};

export const viewUserLoans = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const { userId } = req.params;

    const loans = await prisma.loan.findMany({
      where: { userId },
      orderBy: { checkoutDate: 'desc' },
    });

    res.status(200).json(loans);
  } catch (error) {
    next(error);
  }
};
