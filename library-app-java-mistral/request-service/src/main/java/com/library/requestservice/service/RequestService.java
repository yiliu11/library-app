package com.library.requestservice.service;

import com.library.requestservice.client.NotificationServiceClient;
import com.library.requestservice.client.UserServiceClient;
import com.library.requestservice.dto.*;
import com.library.requestservice.exception.*;
import com.library.requestservice.model.BookRequest;
import com.library.requestservice.model.RequestStatus;
import com.library.requestservice.repository.BookRequestRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class RequestService {
    private final BookRequestRepository bookRequestRepository;
    private final UserServiceClient userServiceClient;
    private final NotificationServiceClient notificationServiceClient;

    public RequestService(BookRequestRepository bookRequestRepository,
                          UserServiceClient userServiceClient,
                          NotificationServiceClient notificationServiceClient) {
        this.bookRequestRepository = bookRequestRepository;
        this.userServiceClient = userServiceClient;
        this.notificationServiceClient = notificationServiceClient;
    }

    @Transactional
    public BookRequestResponseDTO submitRequest(BookRequestDTO requestDTO, Long requesterId, String requesterRole) {
        if (!requesterRole.equals("STAFF")) {
            throw new ForbiddenException("Only staff members can submit book requests.");
        }

        UserDTO user = userServiceClient.getUserById(requesterId);
        if (user == null) {
            throw new ResourceNotFoundException("User not found.");
        }

        BookRequest request = new BookRequest();
        request.setBookTitle(requestDTO.getBookTitle());
        request.setBookAuthor(requestDTO.getBookAuthor());
        request.setBookIsbn(requestDTO.getBookIsbn());
        request.setRequesterId(requesterId);
        request.setStatus(RequestStatus.PENDING);

        BookRequest savedRequest = bookRequestRepository.save(request);
        return convertToResponseDTO(savedRequest);
    }

    @Transactional
    public BookRequestResponseDTO processDecision(RequestDecisionDTO decisionDTO, Long librarianId, String librarianRole) {
        if (!librarianRole.equals("LIBRARIAN")) {
            throw new ForbiddenException("Only librarians can process requests.");
        }

        BookRequest request = bookRequestRepository.findById(decisionDTO.getRequestId())
                .orElseThrow(() -> new ResourceNotFoundException("Request not found."));

        if (request.getStatus() != RequestStatus.PENDING) {
            throw new IllegalStateException("Only pending requests can be processed.");
        }

        request.setStatus(decisionDTO.getStatus());
        request.setDecisionDate(LocalDateTime.now());
        request.setDecidedBy(librarianId);
        request.setNotes(decisionDTO.getNotes());

        BookRequest updatedRequest = bookRequestRepository.save(request);

        // Send notification
        UserDTO requester = userServiceClient.getUserById(request.getRequesterId());
        NotificationRequestDTO notificationRequest = new NotificationRequestDTO();
        notificationRequest.setRecipientId(requester.getId());
        notificationRequest.setRecipientEmail(requester.getEmail());
        notificationRequest.setNotificationType("REQUEST_" + decisionDTO.getStatus().name());

        String subject = "Your Book Request Has Been " + decisionDTO.getStatus().name();
        String message = "Your request for the book '" + request.getBookTitle() +
                "' has been " + decisionDTO.getStatus().name().toLowerCase() + ".";

        if (decisionDTO.getNotes() != null && !decisionDTO.getNotes().isEmpty()) {
            message += "\nNotes: " + decisionDTO.getNotes();
        }

        notificationRequest.setSubject(subject);
        notificationRequest.setMessage(message);
        notificationServiceClient.sendNotification(notificationRequest);

        return convertToResponseDTO(updatedRequest);
    }

    public List<BookRequestResponseDTO> getPendingRequests() {
        return bookRequestRepository.findByStatus(RequestStatus.PENDING).stream()
                .map(this::convertToResponseDTO)
                .collect(Collectors.toList());
    }

    public List<BookRequestResponseDTO> getRequestsByRequester(Long requesterId) {
        return bookRequestRepository.findByRequesterId(requesterId).stream()
                .map(this::convertToResponseDTO)
                .collect(Collectors.toList());
    }

    private BookRequestResponseDTO convertToResponseDTO(BookRequest request) {
        BookRequestResponseDTO dto = new BookRequestResponseDTO();
        dto.setRequestId(request.getId());
        dto.setBookTitle(request.getBookTitle());
        dto.setStatus(request.getStatus());
        dto.setRequestDate(request.getRequestDate());
        dto.setDecisionDate(request.getDecisionDate());
        dto.setNotes(request.getNotes());
        return dto;
    }
}
