package com.library.notificationservice.event;

import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
public class OverdueEvent {
    private Long userId;
    private String userEmail;
    private Long bookId;
    private String bookTitle;
    private LocalDateTime dueDate;
    private BigDecimal fineAmount;
}
