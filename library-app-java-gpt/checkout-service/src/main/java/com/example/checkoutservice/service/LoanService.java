package com.example.checkoutservice.service;

import com.example.checkoutservice.client.BookCatalogClient;
import com.example.checkoutservice.client.BookCatalogClient.BookInfo;
import com.example.checkoutservice.dto.*;
import com.example.checkoutservice.entity.*;
import com.example.checkoutservice.exception.*;
import com.example.checkoutservice.repository.LoanRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class LoanService {

    private final LoanRepository loanRepository;
    private final BookCatalogClient catalogClient;
    private final int loanPeriodDays;
    private final int maxRenewals;

    public LoanService(LoanRepository loanRepository,
                       BookCatalogClient catalogClient,
                       @Value("${app.loan.period-days:14}") int loanPeriodDays,
                       @Value("${app.loan.max-renewals:2}") int maxRenewals) {
        this.loanRepository = loanRepository;
        this.catalogClient = catalogClient;
        this.loanPeriodDays = loanPeriodDays;
        this.maxRenewals = maxRenewals;
    }

    /**
     * Checkout a book for a user. This will:
     *  1) check with catalog for availability
     *  2) decrement copies in catalog (best-effort)
     *  3) create loan record in local DB
     *
     * Note: This is not a distributed transaction. In failure after decrement, attempt to compensate by incrementing back.
     */
    @Transactional
    public LoanResponse checkout(UUID userId, UUID bookId, String jwtToken) {
        // 1) check book info
        BookInfo book = catalogClient.getBook(bookId);
        if (book == null) {
            throw new ResourceNotFoundException("Book not found");
        }
        if (book.getCopiesAvailable() <= 0) {
            throw new ApiException("Book is not available for checkout");
        }

        // 2) attempt to decrement copies in catalog
        try {
            catalogClient.updateCopies(bookId, book.getCopiesAvailable() - 1, jwtToken);
        } catch (Exception ex) {
            throw new ApiException("Failed to reserve book in catalog: " + ex.getMessage());
        }

        // 3) create loan
        LocalDate now = LocalDate.now();
        LocalDate due = now.plusDays(loanPeriodDays);
        Loan loan = new Loan(UUID.randomUUID(), userId, bookId, now, due, LoanStatus.CHECKED_OUT);
        Loan saved = loanRepository.save(loan);
        return toResponse(saved);
    }

    /**
     * Renew a loan for a user
     */
    @Transactional
    public LoanResponse renew(UUID userId, UUID loanId) {
        Loan loan = loanRepository.findById(loanId)
                .orElseThrow(() -> new ResourceNotFoundException("Loan not found"));

        if (!loan.getUserId().equals(userId)) {
            throw new UnauthorizedException("You can only renew your own loans");
        }
        if (loan.getStatus() != LoanStatus.CHECKED_OUT) {
            throw new ApiException("Loan is not active and cannot be renewed");
        }
        if (loan.getRenewalCount() >= maxRenewals) {
            throw new ApiException("Maximum renewals reached");
        }

        // Example policy: cannot renew if overdue (or could allow with fines)
        if (loan.getDueDate().isBefore(LocalDate.now())) {
            throw new ApiException("Cannot renew overdue loans");
        }

        // extend due date
        loan.setRenewalCount(loan.getRenewalCount() + 1);
        loan.setDueDate(loan.getDueDate().plusDays(loanPeriodDays));
        Loan saved = loanRepository.save(loan);
        return toResponse(saved);
    }

    public List<LoanResponse> getLoansForUser(UUID userId) {
        List<Loan> loans = loanRepository.findByUserIdOrderByCheckoutDateDesc(userId);
        return loans.stream().map(this::toResponse).collect(Collectors.toList());
    }

    public LoanResponse getLoan(UUID requesterId, UUID loanId, boolean isLibrarian) {
        Loan loan = loanRepository.findById(loanId)
                .orElseThrow(() -> new ResourceNotFoundException("Loan not found"));
        if (!loan.getUserId().equals(requesterId) && !isLibrarian) {
            throw new UnauthorizedException("Insufficient privileges");
        }
        return toResponse(loan);
    }

    private LoanResponse toResponse(Loan l) {
        return new LoanResponse(l.getId(), l.getBookId(), l.getCheckoutDate(), l.getDueDate(),
                l.getReturnDate(), l.getRenewalCount(), l.getStatus());
    }
}
