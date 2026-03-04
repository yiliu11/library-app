package com.library.notificationservice.service;

import com.library.notificationservice.model.NotificationType;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class TemplateService {
    public String getEmailSubject(NotificationType type, Map<String, String> metadata) {
        return switch (type) {
            case OVERDUE_BOOK -> "Overdue Book Reminder: " + metadata.getOrDefault("bookTitle", "Unknown Book");
            case REQUEST_APPROVED -> "Your Book Request Has Been Approved";
            case REQUEST_REJECTED -> "Your Book Request Has Been Rejected";
            case DUE_DATE_REMINDER -> "Due Date Reminder for: " + metadata.getOrDefault("bookTitle", "Unknown Book");
            case PASSWORD_RESET -> "Password Reset Request";
            case CHECKOUT_CONFIRMATION -> "Checkout Confirmation for: " + metadata.getOrDefault("bookTitle", "Unknown Book");
            case RENEWAL_CONFIRMATION -> "Renewal Confirmation for: " + metadata.getOrDefault("bookTitle", "Unknown Book");
            default -> "Library Notification";
        };
    }

    public String getEmailBody(NotificationType type, Map<String, String> metadata) {
        return switch (type) {
            case OVERDUE_BOOK -> String.format(
                    "Dear User,\n\nThe book '%s' is overdue. Please return it as soon as possible to avoid further fines.\n\nDue Date: %s\nCurrent Fine: $%s\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"),
                    metadata.getOrDefault("fineAmount", "0.00"));

            case REQUEST_APPROVED -> String.format(
                    "Dear User,\n\nYour request for the book '%s' has been approved. It will be added to our collection soon.\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"));

            case REQUEST_REJECTED -> String.format(
                    "Dear User,\n\nYour request for the book '%s' has been rejected.\nReason: %s\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("reason", "No reason provided"));

            case DUE_DATE_REMINDER -> String.format(
                    "Dear User,\n\nThis is a reminder that the book '%s' is due on %s.\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            case PASSWORD_RESET -> "Dear User,\n\nYou have requested a password reset. Please use the following link to reset your password:\n\n[Reset Link]\n\nThank you,\nLibrary Team";

            case CHECKOUT_CONFIRMATION -> String.format(
                    "Dear User,\n\nYou have successfully checked out the book '%s'.\n\nDue Date: %s\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            case RENEWAL_CONFIRMATION -> String.format(
                    "Dear User,\n\nYou have successfully renewed the book '%s'.\n\nNew Due Date: %s\n\nThank you,\nLibrary Team",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            default -> "Dear User,\n\nYou have a new notification from the library.\n\nThank you,\nLibrary Team";
        };
    }

    public String getSMSMessage(NotificationType type, Map<String, String> metadata) {
        return switch (type) {
            case OVERDUE_BOOK -> String.format(
                    "The book '%s' is overdue. Please return it ASAP to avoid fines. Due: %s",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            case REQUEST_APPROVED -> String.format(
                    "Your request for '%s' has been approved. It will be added to our collection soon.",
                    metadata.getOrDefault("bookTitle", "Unknown Book"));

            case REQUEST_REJECTED -> String.format(
                    "Your request for '%s' has been rejected. Reason: %s",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("reason", "No reason provided"));

            case DUE_DATE_REMINDER -> String.format(
                    "Reminder: '%s' is due on %s.",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            case PASSWORD_RESET -> "Password reset requested. Check your email for the reset link.";

            case CHECKOUT_CONFIRMATION -> String.format(
                    "You checked out '%s'. Due: %s.",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            case RENEWAL_CONFIRMATION -> String.format(
                    "You renewed '%s'. New due: %s.",
                    metadata.getOrDefault("bookTitle", "Unknown Book"),
                    metadata.getOrDefault("dueDate", "Unknown Date"));

            default -> "You have a new library notification.";
        };
    }
}
