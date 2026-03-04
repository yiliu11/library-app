package com.library.notificationservice.dto;

import com.library.notificationservice.model.NotificationType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.Map;

@Data
public class NotificationRequestDTO {
    @NotNull(message = "Recipient ID is required")
    private Long recipientId;

    @NotBlank(message = "Recipient email is required")
    private String recipientEmail;

    private String recipientPhone;

    @NotBlank(message = "Subject is required")
    private String subject;

    @NotBlank(message = "Message is required")
    private String message;

    @NotNull(message = "Notification type is required")
    private NotificationType notificationType;

    private Map<String, String> metadata;
}
