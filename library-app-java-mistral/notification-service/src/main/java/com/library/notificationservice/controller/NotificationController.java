package com.library.notificationservice.controller;

import com.library.notificationservice.dto.NotificationRequestDTO;
import com.library.notificationservice.dto.NotificationResponseDTO;
import com.library.notificationservice.service.NotificationService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/notifications")
public class NotificationController {
    private final NotificationService notificationService;

    public NotificationController(NotificationService notificationService) {
        this.notificationService = notificationService;
    }

    @PostMapping
    public ResponseEntity<NotificationResponseDTO> sendNotification(
            @Valid @RequestBody NotificationRequestDTO requestDTO) {
        NotificationResponseDTO response = notificationService.sendNotification(requestDTO);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/retry-failed")
    public ResponseEntity<Void> retryFailedNotifications() {
        notificationService.retryFailedNotifications();
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<NotificationResponseDTO>> getNotificationsByUser(@PathVariable Long userId) {
        List<NotificationResponseDTO> notifications = notificationService.getNotificationsByRecipient(userId);
        return ResponseEntity.ok(notifications);
    }

    @GetMapping("/failed")
    public ResponseEntity<List<NotificationResponseDTO>> getFailedNotifications() {
        List<NotificationResponseDTO> notifications = notificationService.getFailedNotifications();
        return ResponseEntity.ok(notifications);
    }
}
