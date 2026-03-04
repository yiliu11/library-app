import { RequestRepository } from '../repositories/request.repository';
import { BookRequestDTO, BookRequestResponseDTO, RequestStatus } from '../dtos/request.dto';
import { RequestDecisionDTO } from '../dtos/decision.dto';
import { BadRequestError, ForbiddenError, NotFoundError } from '../middlewares/error.middleware';
import { logger } from '../utils/logger';
import axios from 'axios';
import { env } from '../config/env';

export class RequestService {
  constructor(private requestRepository: RequestRepository) {}

  async submitRequest(requestDTO: BookRequestDTO, requesterId: number, requesterRole: string): Promise<BookRequestResponseDTO> {
    if (requesterRole !== 'STAFF') {
      throw new ForbiddenError('Only staff members can submit book requests');
    }

    const request: any = {
      book_title: requestDTO.bookTitle,
      book_author: requestDTO.bookAuthor,
      book_isbn: requestDTO.bookIsbn,
      requester_id: requesterId,
      status: RequestStatus.PENDING,
      notes: requestDTO.notes,
    };

    const createdRequest = await this.requestRepository.createRequest(request);

    // Send notification to librarians (in a real app, you might notify specific librarians)
    try {
      await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
        notificationType: 'NEW_BOOK_REQUEST',
        subject: 'New Book Request Submitted',
        message: `A new book request has been submitted: "${requestDTO.bookTitle}" by "${requestDTO.bookAuthor}"`,
        metadata: {
          requestId: createdRequest.id,
          bookTitle: requestDTO.bookTitle,
          bookAuthor: requestDTO.bookAuthor,
        },
      });
    } catch (err) {
      logger.error(`Failed to send notification for new request: ${err}`);
    }

    return new BookRequestResponseDTO(createdRequest);
  }

  async processDecision(decisionDTO: RequestDecisionDTO, librarianId: number): Promise<BookRequestResponseDTO> {
    const request = await this.requestRepository.findById(decisionDTO.requestId);
    if (!request) {
      throw new NotFoundError('Request not found');
    }

    if (request.status !== RequestStatus.PENDING) {
      throw new BadRequestError('Only pending requests can be processed');
    }

    const updatedRequest = await this.requestRepository.updateStatus(
      decisionDTO.requestId,
      decisionDTO.status,
      librarianId
    );

    if (!updatedRequest) {
      throw new BadRequestError('Failed to update request status');
    }

    // If approved, add to book collection (in a real app, this might be a separate process)
    if (decisionDTO.status === RequestStatus.APPROVED) {
      try {
        await axios.post(`${env.BOOK_SERVICE_URL}/api/books`, {
          title: updatedRequest.book_title,
          author: updatedRequest.book_author,
          isbn: updatedRequest.book_isbn,
        });
      } catch (err) {
        logger.error(`Failed to add approved book to collection: ${err}`);
        // In a real app, you might want to handle this more gracefully
      }
    }

    // Send notification to requester
    try {
      const notificationType = decisionDTO.status === RequestStatus.APPROVED
        ? 'REQUEST_APPROVED'
        : 'REQUEST_REJECTED';

      await axios.post(`${env.NOTIFICATION_SERVICE_URL}/api/notifications`, {
        recipientId: updatedRequest.requester_id,
        notificationType,
        subject: `Your Book Request Has Been ${decisionDTO.status}`,
        message: `Your request for "${updatedRequest.book_title}" has been ${decisionDTO.status.toLowerCase()}. ${
          decisionDTO.notes ? `Notes: ${decisionDTO.notes}` : ''
        }`,
        metadata: {
          requestId: updatedRequest.id,
          bookTitle: updatedRequest.book_title,
          status: decisionDTO.status,
        },
      });
    } catch (err) {
      logger.error(`Failed to send decision notification: ${err}`);
    }

    return new BookRequestResponseDTO(updatedRequest);
  }

  async getPendingRequests(): Promise<BookRequestResponseDTO[]> {
    const requests = await this.requestRepository.findPendingRequests();
    return requests.map(request => new BookRequestResponseDTO(request));
  }

  async getRequestsByRequester(requesterId: number): Promise<BookRequestResponseDTO[]> {
    const requests = await this.requestRepository.findByRequester(requesterId);
    return requests.map(request => new BookRequestResponseDTO(request));
  }
}
