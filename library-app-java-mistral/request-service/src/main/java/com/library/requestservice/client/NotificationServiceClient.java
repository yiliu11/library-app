package com.library.requestservice.client;

import com.library.requestservice.dto.NotificationRequestDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "notification-service", url = "${notification.service.url:http://localhost:8085}")
public interface NotificationServiceClient {
    @PostMapping("/api/notifications")
    void sendNotification(@RequestBody NotificationRequestDTO notificationRequest);
}
