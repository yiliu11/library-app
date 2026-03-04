package com.library.requestservice.dto;

import com.library.requestservice.model.RequestStatus;
import lombok.Data;

import java.util.Map;

@Data
public class NotificationRequestDTO {
    private Long recipientId;
    private String recipientEmail;
    private String subject;
    private String message;
    private String notificationType;
    private Map<String, String> metadata;
}
