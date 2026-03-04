package com.library.notificationservice.service;

import com.library.notificationservice.dto.*;
import com.library.notificationservice.exception.NotificationException;
import com.library.notificationservice.exception.ResourceNotFoundException;
import com.library.notificationservice.model.Notification;
import com.library.notificationservice.model.NotificationStatus;
import com.library.notificationservice.repository.NotificationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class NotificationService {
    private final NotificationRepository notificationRepository;
    private final EmailService emailService;
    private final SMSService smsService;

    @Value("${notification.retry.max-attempts:3}")
    private int maxRetryAttempts;

    @Value("${notification.retry.delay:30000}")
    private long retryDelay;

    @Autowired
    public NotificationService(NotificationRepository notificationRepository,
                               EmailService emailService,
                               SMSService smsService) {
        this.notificationRepository = notificationRepository;
        this.emailService = emailService;
        this.smsService = smsService;
    }

    @Transactional
    public NotificationResponseDTO sendNotification(NotificationRequestDTO requestDTO) {
        Notification notification = new Notification();
        notification.setRecipientId(requestDTO.getRecipientId());
        notification.setRecipientEmail(requestDTO.getRecipientEmail());
        notification.setRecipientPhone(requestDTO.getRecipientPhone());
        notification.setSubject(requestDTO.getSubject());
        notification.setMessage(requestDTO.getMessage());
        notification.setNotificationType(requestDTO.getNotificationType());
        notification.setStatus(NotificationStatus.PENDING);
        notification.setMetadata(requestDTO.getMetadata());

        Notification savedNotification = notificationRepository.save(notification);

        try {
            sendEmailNotification(requestDTO);
            notification.setStatus(NotificationStatus.SENT);
            notification.setSentAt(LocalDateTime.now());
        } catch (Exception e) {
            notification.setStatus(NotificationStatus.FAILED);
            throw new NotificationException("Failed to send email notification: " + e.getMessage());
        }

        notificationRepository.save(notification);

        NotificationResponseDTO responseDTO = new NotificationResponseDTO();
        responseDTO.setNotificationId(savedNotification.getId());
        responseDTO.setStatus(savedNotification.getStatus());
        responseDTO.setTimestamp(LocalDateTime.now());

        return responseDTO;
    }

    @Retryable(maxAttemptsExpression = "${notification.retry.max-attempts:3}",
               backoff = @Backoff(delayExpression = "${notification.retry.delay:30000}"))
    public void sendEmailNotification(NotificationRequestDTO requestDTO) {
        EmailNotificationDTO emailDTO = new EmailNotificationDTO();
        emailDTO.setTo(requestDTO.getRecipientEmail());
        emailDTO.setSubject(requestDTO.getSubject());
        emailDTO.setBody(requestDTO.getMessage());
        emailService.sendEmail(emailDTO);
    }

    public void sendSMSNotification(NotificationRequestDTO requestDTO) {
        if (requestDTO.getRecipientPhone() != null && !requestDTO.getRecipientPhone().isEmpty()) {
            SMSNotificationDTO smsDTO = new SMSNotificationDTO();
            smsDTO.setTo(requestDTO.getRecipientPhone());
            smsDTO.setMessage(requestDTO.getMessage());
            smsService.sendSMS(smsDTO);
        }
    }

    @Transactional
    public void retryFailedNotifications() {
        List<Notification> failedNotifications = notificationRepository.findByStatus(NotificationStatus.FAILED);
        for (Notification notification : failedNotifications) {
            try {
                EmailNotificationDTO emailDTO = new EmailNotificationDTO();
                emailDTO.setTo(notification.getRecipientEmail());
                emailDTO.setSubject(notification.getSubject());
                emailDTO.setBody(notification.getMessage());
                emailService.sendEmail(emailDTO);

                notification.setStatus(NotificationStatus.SENT);
                notification.setSentAt(LocalDateTime.now());
                notificationRepository.save(notification);
            } catch (Exception e) {
                // Log the error and continue with the next notification
                System.err.println("Failed to retry notification " + notification.getId() + ": " + e.getMessage());
            }
        }
    }

    public List<NotificationResponseDTO> getNotificationsByRecipient(Long recipientId) {
        return notificationRepository.findByRecipientId(recipientId).stream()
                .map(this::convertToResponseDTO)
                .collect(Collectors.toList());
    }

    public List<NotificationResponseDTO> getFailedNotifications() {
        return notificationRepository.findByStatus(NotificationStatus.FAILED).stream()
                .map(this::convertToResponseDTO)
                .collect(Collectors.toList());
    }

    private NotificationResponseDTO convertToResponseDTO(Notification notification) {
        NotificationResponseDTO dto = new NotificationResponseDTO();
        dto.setNotificationId(notification.getId());
        dto.setStatus(notification.getStatus());
        dto.setTimestamp(notification.getSentAt() != null ? notification.getSentAt() : notification.getCreatedAt());
        return dto;
    }
}
