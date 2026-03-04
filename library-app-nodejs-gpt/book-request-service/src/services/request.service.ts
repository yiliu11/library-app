import prisma from "../prisma/client";
import { RequestStatus } from "@prisma/client";
import { NotFoundError, BadRequestError } from "../utils/errors";

export class RequestService {
  // Create a new book request
  async createRequest(data: {
    title: string;
    author: string;
    description?: string;
    requestedBy: number;
  }) {
    return await prisma.bookRequest.create({
      data,
    });
  }

  // Get all book requests (optionally filter by status)
  async getRequests(status?: RequestStatus) {
    return await prisma.bookRequest.findMany({
      where: status ? { status } : undefined,
      orderBy: { createdAt: "desc" },
    });
  }

  // Get a single book request by ID
  async getRequestById(id: number) {
    const request = await prisma.bookRequest.findUnique({
      where: { id },
    });

    if (!request) throw new NotFoundError("Book request not found");
    return request;
  }

  // Update request status (approve/reject)
  async updateRequestStatus(
    id: number,
    status: RequestStatus,
    reviewedBy: number
  ) {
    const existing = await prisma.bookRequest.findUnique({ where: { id } });

    if (!existing) throw new NotFoundError("Book request not found");
    if (existing.status !== RequestStatus.PENDING) {
      throw new BadRequestError("Only pending requests can be updated");
    }

    return await prisma.bookRequest.update({
      where: { id },
      data: { status, reviewedBy },
    });
  }

  // Delete a request (only for testing/admin)
  async deleteRequest(id: number) {
    const existing = await prisma.bookRequest.findUnique({ where: { id } });
    if (!existing) throw new NotFoundError("Book request not found");

    return await prisma.bookRequest.delete({ where: { id } });
  }
}
