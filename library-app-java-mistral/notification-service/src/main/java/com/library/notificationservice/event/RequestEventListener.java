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
public class RequestEventListener {
    private final NotificationService notificationService;
    private final TemplateService templateService;

    public RequestEventListener(NotificationService notificationService,
                                TemplateService templateService) {
        this.notificationService = notificationService;
        this.templateService = templateService;
    }

    @KafkaListener(topics = "request-events", groupId = "notification-group")
    public void handleRequestEvent(RequestEvent event) {
        NotificationRequestDTO requestDTO = new NotificationRequestDTO();
        requestDTO.setRecipientId(event.getRequesterId());
        requestDTO.setRecipientEmail(event.getRequesterEmail());

        Map<String, String> metadata = new HashMap<>();
        metadata.put("bookTitle", event.getBookTitle());
        metadata.put("reason", event.getReason());

        NotificationType type = event.getStatus().equals("APPROVED")
                ? NotificationType.REQUEST_APPROVED
                : NotificationType.REQUEST_REJECTED;

        requestDTO.setSubject(templateService.getEmailSubject(type, metadata));
        requestDTO.setMessage(templateService.getEmailBody(type, metadata));
        requestDTO.setNotificationType(type);
        requestDTO.setMetadata(metadata);

        notificationService.sendNotification(requestDTO);
    }
}
