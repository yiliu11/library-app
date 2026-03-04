package com.library.notificationservice.event;

import lombok.Data;

@Data
public class RequestEvent {
    private Long requestId;
    private Long requesterId;
    private String requesterEmail;
    private String bookTitle;
    private String status;
    private String reason;
}
