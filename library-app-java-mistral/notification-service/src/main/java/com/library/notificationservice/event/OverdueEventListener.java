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
public class OverdueEventListener {
    private final NotificationService notificationService;
    private final TemplateService templateService;

    public OverdueEventListener(NotificationService notificationService,
                                TemplateService templateService) {
        this.notificationService = notificationService;
        this.templateService = templateService;
    }

    @KafkaListener(topics = "overdue-events", groupId = "notification-group")
    public void handleOverdueEvent(OverdueEvent event) {
        NotificationRequestDTO requestDTO = new NotificationRequestDTO();
        requestDTO.setRecipientId(event.getUserId());
        requestDTO.setRecipientEmail(event.getUserEmail());

        Map<String, String> metadata = new HashMap<>();
        metadata.put("bookTitle", event.getBookTitle());
        metadata.put("dueDate", event.getDueDate().toString());
        metadata.put("fineAmount", event.getFineAmount().toString());

        requestDTO.setSubject(templateService.getEmailSubject(NotificationType.OVERDUE_BOOK, metadata));
        requestDTO.setMessage(templateService.getEmailBody(NotificationType.OVERDUE_BOOK, metadata));
        requestDTO.setNotificationType(NotificationType.OVERDUE_BOOK);
        requestDTO.setMetadata(metadata);

        notificationService.sendNotification(requestDTO);
    }
}
