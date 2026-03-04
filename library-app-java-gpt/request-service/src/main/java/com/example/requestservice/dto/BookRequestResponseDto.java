package com.example.requestservice.dto;

import com.example.requestservice.entity.RequestStatus;

import java.time.Instant;
import java.util.UUID;

public class BookRequestResponseDto {

    private UUID id;
    private UUID requestedBy;
    private String title;
    private String author;
    private String reason;
    private RequestStatus status;
    private String comments;
    private Instant createdAt;
    private Instant updatedAt;

    public BookRequestResponseDto() {}

    public BookRequestResponseDto(UUID id, UUID requestedBy, String title, String author, String reason,
                                  RequestStatus status, String comments, Instant createdAt, Instant updatedAt) {
        this.id = id;
        this.requestedBy = requestedBy;
        this.title = title;
        this.author = author;
        this.reason = reason;
        this.status = status;
        this.comments = comments;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    // getters and setters

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getRequestedBy() { return requestedBy; }
    public void setRequestedBy(UUID requestedBy) { this.requestedBy = requestedBy; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }

    public RequestStatus getStatus() { return status; }
    public void setStatus(RequestStatus status) { this.status = status; }

    public String getComments() { return comments; }
    public void setComments(String comments) { this.comments = comments; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }

    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}
