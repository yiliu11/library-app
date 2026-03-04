package com.library.notificationservice.repository;

import com.library.notificationservice.model.Notification;
import com.library.notificationservice.model.NotificationStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NotificationRepository extends JpaRepository<Notification, Long> {
    List<Notification> findByRecipientId(Long recipientId);
    List<Notification> findByStatus(NotificationStatus status);
    List<Notification> findByRecipientIdAndStatus(Long recipientId, NotificationStatus status);
}
