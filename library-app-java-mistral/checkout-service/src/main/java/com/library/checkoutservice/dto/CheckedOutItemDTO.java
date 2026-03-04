package com.library.checkoutservice.dto;

import com.library.checkoutservice.model.CheckoutRecord.CheckoutStatus;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class CheckedOutItemDTO {
    private Long checkoutId;
    private Long bookId;
    private String bookTitle;
    private LocalDateTime dueDate;
    private CheckoutStatus status;
    private BigDecimal fineAmount;
}
