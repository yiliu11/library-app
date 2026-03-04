package com.library.notificationservice.dto;

import com.library.notificationservice.model.NotificationStatus;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class NotificationResponseDTO {
    private Long notificationId;
    private NotificationStatus status;
    private LocalDateTime timestamp;
}
