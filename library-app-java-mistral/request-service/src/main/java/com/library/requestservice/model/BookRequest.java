package com.library.requestservice.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "book_requests")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class BookRequest {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "book_title", nullable = false)
    private String bookTitle;

    @Column(name = "book_author", nullable = false)
    private String bookAuthor;

    @Column(name = "book_isbn")
    private String bookIsbn;

    @Column(name = "requester_id", nullable = false)
    private Long requesterId;

    @Column(name = "request_date", nullable = false)
    @CreationTimestamp
    private LocalDateTime requestDate;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RequestStatus status;

    @Column(name = "decision_date")
    private LocalDateTime decisionDate;

    @Column(name = "decided_by")
    private Long decidedBy;

    @Column(name = "notes")
    private String notes;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    public enum RequestStatus {
        PENDING, APPROVED, REJECTED, ARCHIVED
    }
}
