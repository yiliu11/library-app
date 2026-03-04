package com.library.notificationservice.event;

import com.library.notificationservice.dto.NotificationRequestDTO;
import com.library.notificationservice.model.NotificationType;
import com.library.notificationservice.service.NotificationService;
import com.library.notificationservice.service.TemplateService;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
public class CheckoutEventListener {
    private final NotificationService notificationService;
    private final TemplateService templateService;

    public CheckoutEventListener(NotificationService notificationService,
                                 TemplateService templateService) {
        this.notificationService = notificationService;
        this.templateService = templateService;
    }

    @KafkaListener(topics = "checkout-events", groupId = "notification-group")
    public void handleCheckoutEvent(CheckoutEvent event) {
        NotificationRequestDTO requestDTO = new NotificationRequestDTO();
        requestDTO.setRecipientId(event.getUserId());
        requestDTO.setRecipientEmail(event.getUserEmail());

        Map<String, String> metadata = new HashMap<>();
        metadata.put("bookTitle", event.getBookTitle());
        metadata.put("dueDate", event.getDueDate().toString());

        requestDTO.setSubject(templateService.getEmailSubject(NotificationType.CHECKOUT_CONFIRMATION, metadata));
        requestDTO.setMessage(templateService.getEmailBody(NotificationType.CHECKOUT_CONFIRMATION, metadata));
        requestDTO.setNotificationType(NotificationType.CHECKOUT_CONFIRMATION);
        requestDTO.setMetadata(metadata);

        notificationService.sendNotification(requestDTO);
    }
}
