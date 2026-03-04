package com.example.checkoutservice.entity;

import javax.persistence.*;
import java.time.LocalDate;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "loans", indexes = {
        @Index(name = "idx_loans_user", columnList = "user_id"),
        @Index(name = "idx_loans_book", columnList = "book_id")
})
public class Loan {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(name = "book_id", nullable = false)
    private UUID bookId;

    @Column(name = "checkout_date", nullable = false)
    private LocalDate checkoutDate;

    @Column(name = "due_date", nullable = false)
    private LocalDate dueDate;

    @Column(name = "return_date")
    private LocalDate returnDate;

    @Column(name = "renewal_count", nullable = false)
    private int renewalCount = 0;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private LoanStatus status;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    protected Loan() {
        // JPA
    }

    public Loan(UUID id, UUID userId, UUID bookId, LocalDate checkoutDate,
                LocalDate dueDate, LoanStatus status) {
        this.id = id;
        this.userId = userId;
        this.bookId = bookId;
        this.checkoutDate = checkoutDate;
        this.dueDate = dueDate;
        this.status = status;
        this.createdAt = Instant.now();
    }

    // getters and setters

    public UUID getId() { return id; }
    public UUID getUserId() { return userId; }
    public UUID getBookId() { return bookId; }
    public LocalDate getCheckoutDate() { return checkoutDate; }
    public LocalDate getDueDate() { return dueDate; }
    public LocalDate getReturnDate() { return returnDate; }
    public int getRenewalCount() { return renewalCount; }
    public LoanStatus getStatus() { return status; }

    public void setReturnDate(LocalDate returnDate) { this.returnDate = returnDate; }
    public void setDueDate(LocalDate dueDate) { this.dueDate = dueDate; }
    public void setRenewalCount(int renewalCount) { this.renewalCount = renewalCount; }
    public void setStatus(LoanStatus status) { this.status = status; }
}
