package com.library.checkoutservice.service;

import com.library.checkoutservice.client.BookServiceClient;
import com.library.checkoutservice.client.UserServiceClient;
import com.library.checkoutservice.dto.*;
import com.library.checkoutservice.exception.*;
import com.library.checkoutservice.model.CheckoutRecord;
import com.library.checkoutservice.model.CheckoutRecord.CheckoutStatus;
import com.library.checkoutservice.repository.CheckoutRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class CheckoutService {
    private static final int MAX_CHECKOUTS = 5;
    private static final int CHECKOUT_DURATION_DAYS = 14;
    private static final int RENEWAL_DURATION_DAYS = 7;
    private static final BigDecimal DAILY_FINE = new BigDecimal("0.50");

    private final CheckoutRepository checkoutRepository;
    private final UserServiceClient userServiceClient;
    private final BookServiceClient bookServiceClient;

    public CheckoutService(CheckoutRepository checkoutRepository,
                           UserServiceClient userServiceClient,
                           BookServiceClient bookServiceClient) {
        this.checkoutRepository = checkoutRepository;
        this.userServiceClient = userServiceClient;
        this.bookServiceClient = bookServiceClient;
    }

    @Transactional
    public CheckoutResponseDTO checkoutBook(CheckoutRequestDTO requestDTO, Long requestingUserId) {
        // Validate user
        UserDTO user = userServiceClient.getUserById(requestingUserId);
        if (user == null) {
            throw new ResourceNotFoundException("User not found.");
        }

        // Check if user has reached checkout limit
        List<CheckoutRecord> activeCheckouts = checkoutRepository.findByUserIdAndStatus(
                requestingUserId, CheckoutStatus.ACTIVE);
        if (activeCheckouts.size() >= MAX_CHECKOUTS) {
            throw new CheckoutLimitExceededException("You have reached the maximum number of checkouts (" + MAX_CHECKOUTS + ").");
        }

        // Check if book is available
        BookDTO book = bookServiceClient.getBookById(requestDTO.getBookId());
        if (book == null) {
            throw new ResourceNotFoundException("Book not found.");
        }
        if (!book.getAvailabilityStatus().equals("AVAILABLE")) {
            throw new BookUnavailableException("Book is not available for checkout.");
        }

        // Create checkout record
        CheckoutRecord checkoutRecord = new CheckoutRecord();
        checkoutRecord.setUserId(requestingUserId);
        checkoutRecord.setBookId(requestDTO.getBookId());
        checkoutRecord.setCheckoutDate(LocalDateTime.now());
        checkoutRecord.setDueDate(LocalDateTime.now().plusDays(CHECKOUT_DURATION_DAYS));
        checkoutRecord.setStatus(CheckoutStatus.ACTIVE);
        checkoutRecord.setFineAmount(BigDecimal.ZERO);

        CheckoutRecord savedRecord = checkoutRepository.save(checkoutRecord);

        // Update book availability
        bookServiceClient.updateBookAvailability(requestDTO.getBookId(), "CHECKED_OUT");

        // Prepare response
        CheckoutResponseDTO response = new CheckoutResponseDTO();
        response.setCheckoutId(savedRecord.getId());
        response.setBookId(savedRecord.getBookId());
        response.setBookTitle(book.getTitle());
        response.setDueDate(savedRecord.getDueDate());
        response.setStatus(savedRecord.getStatus());

        return response;
    }

    @Transactional
    public CheckoutResponseDTO renewCheckout(RenewalRequestDTO requestDTO, Long requestingUserId) {
        CheckoutRecord checkoutRecord = checkoutRepository.findById(requestDTO.getCheckoutId())
                .orElseThrow(() -> new ResourceNotFoundException("Checkout record not found."));

        // Validate user ownership
        if (!checkoutRecord.getUserId().equals(requestingUserId)) {
            throw new ForbiddenException("You can only renew your own checkouts.");
        }

        // Check if renewal is allowed
        if (checkoutRecord.getStatus() != CheckoutStatus.ACTIVE) {
            throw new IllegalStateException("Only active checkouts can be renewed.");
        }
        if (LocalDateTime.now().isAfter(checkoutRecord.getDueDate())) {
            throw new IllegalStateException("Overdue items cannot be renewed.");
        }

        // Update due date
        checkoutRecord.setDueDate(LocalDateTime.now().plusDays(RENEWAL_DURATION_DAYS));
        checkoutRecord.setStatus(CheckoutStatus.RENEWED);
        CheckoutRecord updatedRecord = checkoutRepository.save(checkoutRecord);

        // Prepare response
        CheckoutResponseDTO response = new CheckoutResponseDTO();
        response.setCheckoutId(updatedRecord.getId());
        response.setBookId(updatedRecord.getBookId());
        BookDTO book = bookServiceClient.getBookById(updatedRecord.getBookId());
        response.setBookTitle(book.getTitle());
        response.setDueDate(updatedRecord.getDueDate());
        response.setStatus(updatedRecord.getStatus());

        return response;
    }

    @Transactional
    public void returnBook(ReturnRequestDTO requestDTO, Long requestingUserId) {
        CheckoutRecord checkoutRecord = checkoutRepository.findById(requestDTO.getCheckoutId())
                .orElseThrow(() -> new ResourceNotFoundException("Checkout record not found."));

        // Validate user ownership
        if (!checkoutRecord.getUserId().equals(requestingUserId)) {
            throw new ForbiddenException("You can only return your own checkouts.");
        }

        // Update checkout record
        checkoutRecord.setReturnDate(LocalDateTime.now());
        checkoutRecord.setStatus(CheckoutStatus.RETURNED);

        // Calculate fine if overdue
        if (LocalDateTime.now().isAfter(checkoutRecord.getDueDate())) {
            long daysOverdue = java.time.temporal.ChronoUnit.DAYS.between(
                    checkoutRecord.getDueDate(), LocalDateTime.now());
            BigDecimal fine = DAILY_FINE.multiply(new BigDecimal(daysOverdue));
            checkoutRecord.setFineAmount(fine);
        }

        checkoutRepository.save(checkoutRecord);

        // Update book availability
        bookServiceClient.updateBookAvailability(checkoutRecord.getBookId(), "AVAILABLE");
    }

    public UserRecordDTO getUserRecords(Long userId, Long requestingUserId, String requestingUserRole) {
        // Validate access
        if (!requestingUserId.equals(userId) && !requestingUserRole.equals("LIBRARIAN")) {
            throw new ForbiddenException("You can only view your own records.");
        }

        List<CheckoutRecord> checkouts = checkoutRepository.findByUserId(userId);
        List<CheckedOutItemDTO> checkedOutItems = checkouts.stream()
                .map(this::convertToCheckedOutItemDTO)
                .collect(Collectors.toList());

        BigDecimal totalFines = checkouts.stream()
                .map(CheckoutRecord::getFineAmount)
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        UserRecordDTO recordDTO = new UserRecordDTO();
        recordDTO.setUserId(userId);
        recordDTO.setCheckedOutItems(checkedOutItems);
        recordDTO.setTotalFines(totalFines);

        return recordDTO;
    }

    private CheckedOutItemDTO convertToCheckedOutItemDTO(CheckoutRecord checkoutRecord) {
        CheckedOutItemDTO itemDTO = new CheckedOutItemDTO();
        itemDTO.setCheckoutId(checkoutRecord.getId());
        itemDTO.setBookId(checkoutRecord.getBookId());

        BookDTO book = bookServiceClient.getBookById(checkoutRecord.getBookId());
        itemDTO.setBookTitle(book.getTitle());

        itemDTO.setDueDate(checkoutRecord.getDueDate());
        itemDTO.setStatus(checkoutRecord.getStatus());
        itemDTO.setFineAmount(checkoutRecord.getFineAmount());

        return itemDTO;
    }
}
