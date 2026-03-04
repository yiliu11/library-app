package com.library.notificationservice.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}

public class NotificationException extends RuntimeException {
    public NotificationException(String message) {
        super(message);
    }
}
