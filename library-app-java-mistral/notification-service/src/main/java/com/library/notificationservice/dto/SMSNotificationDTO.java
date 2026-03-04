package com.library.notificationservice.dto;

import lombok.Data;

@Data
public class SMSNotificationDTO {
    private String to;
    private String message;
}
