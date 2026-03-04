package com.example.requestservice.entity;

import javax.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "book_requests", indexes = {
        @Index(name = "idx_requests_requested_by", columnList = "requested_by"),
        @Index(name = "idx_requests_status", columnList = "status")
})
public class BookRequestEntity {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "requested_by", nullable = false)
    private UUID requestedBy;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(length = 300)
    private String author;

    @Column(columnDefinition = "text")
    private String reason;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private RequestStatus status;

    @Column(columnDefinition = "text")
    private String comments;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "updated_at")
    private Instant updatedAt;

    protected BookRequestEntity() {
        // JPA
    }

    public BookRequestEntity(UUID id, UUID requestedBy, String title, String author, String reason, RequestStatus status) {
        this.id = id;
        this.requestedBy = requestedBy;
        this.title = title;
        this.author = author;
        this.reason = reason;
        this.status = status;
        this.createdAt = Instant.now();
    }

    // Getters and setters

    public UUID getId() { return id; }
    public UUID getRequestedBy() { return requestedBy; }
    public void setRequestedBy(UUID requestedBy) { this.requestedBy = requestedBy; }

    public String getTitle() { return title; }
    public String getAuthor() { return author; }
    public String getReason() { return reason; }
    public RequestStatus getStatus() { return status; }
    public void setStatus(RequestStatus status) { this.status = status; }
    public String getComments() { return comments; }
    public void setComments(String comments) { this.comments = comments; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
}
