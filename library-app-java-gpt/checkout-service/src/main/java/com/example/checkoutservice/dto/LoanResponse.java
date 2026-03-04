package com.example.checkoutservice.dto;

import com.example.checkoutservice.entity.LoanStatus;

import java.time.LocalDate;
import java.util.UUID;

public class LoanResponse {
    private UUID id;
    private UUID bookId;
    private LocalDate checkoutDate;
    private LocalDate dueDate;
    private LocalDate returnDate;
    private int renewalCount;
    private LoanStatus status;

    public LoanResponse() {}

    public LoanResponse(UUID id, UUID bookId, LocalDate checkoutDate, LocalDate dueDate,
                        LocalDate returnDate, int renewalCount, LoanStatus status) {
        this.id = id;
        this.bookId = bookId;
        this.checkoutDate = checkoutDate;
        this.dueDate = dueDate;
        this.returnDate = returnDate;
        this.renewalCount = renewalCount;
        this.status = status;
    }

    // getters and setters

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getBookId() { return bookId; }
    public void setBookId(UUID bookId) { this.bookId = bookId; }

    public LocalDate getCheckoutDate() { return checkoutDate; }
    public void setCheckoutDate(LocalDate checkoutDate) { this.checkoutDate = checkoutDate; }

    public LocalDate getDueDate() { return dueDate; }
    public void setDueDate(LocalDate dueDate) { this.dueDate = dueDate; }

    public LocalDate getReturnDate() { return returnDate; }
    public void setReturnDate(LocalDate returnDate) { this.returnDate = returnDate; }

    public int getRenewalCount() { return renewalCount; }
    public void setRenewalCount(int renewalCount) { this.renewalCount = renewalCount; }

    public LoanStatus getStatus() { return status; }
    public void setStatus(LoanStatus status) { this.status = status; }
}
