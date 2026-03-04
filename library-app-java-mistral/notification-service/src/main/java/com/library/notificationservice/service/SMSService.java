package com.library.notificationservice.service;

import com.library.notificationservice.dto.SMSNotificationDTO;
import org.springframework.stereotype.Service;

@Service
public class SMSService {
    // In a real application, this would integrate with a SMS gateway like Twilio
    public void sendSMS(SMSNotificationDTO smsDTO) {
        // Mock implementation - replace with actual SMS gateway integration
        System.out.println("Sending SMS to: " + smsDTO.getTo());
        System.out.println("Message: " + smsDTO.getMessage());
    }
}
