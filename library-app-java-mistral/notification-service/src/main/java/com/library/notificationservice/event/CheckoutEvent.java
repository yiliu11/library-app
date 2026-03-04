package com.library.notificationservice.event;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class CheckoutEvent {
    private Long userId;
    private String userEmail;
    private Long bookId;
    private String bookTitle;
    private LocalDateTime dueDate;
}
