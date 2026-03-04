// src/services/user.service.ts

import { prisma } from '../config/prisma';
import bcrypt from 'bcrypt';
import { NotFound, BadRequest } from '../utils/errors';

const SALT_ROUNDS = 10;

export type CreateUserInput = {
  email: string;
  username: string;
  password: string;
  role?: 'patron' | 'staff' | 'librarian';
  fullName?: string | null;
};

export const createUser = async (input: CreateUserInput) => {
  // ensure uniqueness
  const existing = await prisma.user.findFirst({
    where: { OR: [{ email: input.email }, { username: input.username }] }
  });
  if (existing) {
    throw BadRequest('Email or username already in use');
  }

  const hashed = await bcrypt.hash(input.password, SALT_ROUNDS);
  const user = await prisma.user.create({
    data: {
      email: input.email,
      username: input.username,
      password: hashed,
      role: input.role ?? 'patron',
      fullName: input.fullName ?? null
    },
    select: {
      id: true,
      email: true,
      username: true,
      role: true,
      fullName: true,
      isActive: true,
      createdAt: true
    }
  });
  return user;
};

export const getUserById = async (id: string) => {
  const user = await prisma.user.findUnique({
    where: { id },
    select: {
      id: true,
      email: true,
      username: true,
      role: true,
      fullName: true,
      isActive: true,
      createdAt: true,
      updatedAt: true
    }
  });
  if (!user) throw NotFound('User not found');
  return user;
};

export const listUsers = async (opts: { page?: number; size?: number; role?: string; search?: string }) => {
  const page = opts.page ?? 1;
  const size = opts.size ?? 20;
  const skip = (page - 1) * size;

  const where: any = {};
  if (opts.role) where.role = opts.role;
  if (opts.search) {
    where.OR = [
      { email: { contains: opts.search, mode: 'insensitive' } },
      { username: { contains: opts.search, mode: 'insensitive' } },
      { fullName: { contains: opts.search, mode: 'insensitive' } }
    ];
  }

  const [items, total] = await Promise.all([
    prisma.user.findMany({
      where,
      skip,
      take: size,
      orderBy: { createdAt: 'desc' },
      select: { id: true, email: true, username: true, role: true, fullName: true, isActive: true, createdAt: true }
    }),
    prisma.user.count({ where })
  ]);

  return { items, total, page, size };
};

export const updateUser = async (id: string, updates: Partial<CreateUserInput> & { isActive?: boolean; role?: string }) => {
  // ensure user exists
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) throw NotFound('User not found');

  const data: any = {};
  if (updates.email) data.email = updates.email;
  if (updates.username) data.username = updates.username;
  if (typeof updates.fullName !== 'undefined') data.fullName = updates.fullName;
  if (typeof updates.isActive !== 'undefined') data.isActive = updates.isActive;
  if (updates.role) data.role = updates.role;

  if (updates.password) {
    data.password = await bcrypt.hash(updates.password, SALT_ROUNDS);
  }

  const updated = await prisma.user.update({
    where: { id },
    data,
    select: { id: true, email: true, username: true, role: true, fullName: true, isActive: true, updatedAt: true }
  });
  return updated;
};

export const deleteUser = async (id: string) => {
  const user = await prisma.user.findUnique({ where: { id } });
  if (!user) throw NotFound('User not found');
  await prisma.user.delete({ where: { id } });
  return { message: 'User deleted' };
};
