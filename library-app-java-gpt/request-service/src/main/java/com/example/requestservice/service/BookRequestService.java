package com.example.requestservice.service;

import com.example.requestservice.dto.*;
import com.example.requestservice.entity.*;
import com.example.requestservice.exception.*;
import com.example.requestservice.repository.BookRequestRepository;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class BookRequestService {

    private final BookRequestRepository repository;

    public BookRequestService(BookRequestRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public BookRequestResponseDto createRequest(UUID userId, CreateBookRequestDto dto) {
        Objects.requireNonNull(userId, "userId required");
        UUID id = UUID.randomUUID();
        BookRequestEntity entity = new BookRequestEntity(id, userId, dto.getTitle(), dto.getAuthor(), dto.getReason(), RequestStatus.PENDING);
        BookRequestEntity saved = repository.save(entity);
        return toDto(saved);
    }

    public Page<BookRequestResponseDto> listRequests(Optional<RequestStatus> statusFilter, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<BookRequestEntity> pageResult = statusFilter
                .map(status -> repository.findByStatus(status, pageable))
                .orElse(repository.findAll(pageable));
        return pageResult.map(this::toDto);
    }

    public Page<BookRequestResponseDto> listRequestsForUser(UUID userId, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<BookRequestEntity> pageResult = repository.findByRequestedBy(userId, pageable);
        return pageResult.map(this::toDto);
    }

    public BookRequestResponseDto getById(UUID id) {
        BookRequestEntity e = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        return toDto(e);
    }

    @Transactional
    public BookRequestResponseDto approveRequest(UUID id, String comments, UUID actingUserId, String actingRole) {
        // Only librarians should call this: controller enforces role
        BookRequestEntity e = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        if (e.getStatus() != RequestStatus.PENDING) {
            throw new ApiException("Only PENDING requests can be approved");
        }
        e.setStatus(RequestStatus.APPROVED);
        e.setComments(comments);
        e.setUpdatedAt(Instant.now());
        BookRequestEntity saved = repository.save(e);
        // Optionally: trigger notification to requester
        return toDto(saved);
    }

    @Transactional
    public BookRequestResponseDto rejectRequest(UUID id, String comments, UUID actingUserId, String actingRole) {
        BookRequestEntity e = repository.findById(id).orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        if (e.getStatus() != RequestStatus.PENDING) {
            throw new ApiException("Only PENDING requests can be rejected");
        }
        e.setStatus(RequestStatus.REJECTED);
        e.setComments(comments);
        e.setUpdatedAt(Instant.now());
        BookRequestEntity saved = repository.save(e);
        // Optionally: trigger notification to requester
        return toDto(saved);
    }

    private BookRequestResponseDto toDto(BookRequestEntity e) {
        return new BookRequestResponseDto(e.getId(), e.getRequestedBy(), e.getTitle(), e.getAuthor(), e.getReason(), e.getStatus(), e.getComments(), e.getCreatedAt(), e.getUpdatedAt());
    }
}
