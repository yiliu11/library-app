package com.library.requestservice.dto;

import com.library.requestservice.model.RequestStatus;
import lombok.Data;

import java.time.LocalDateTime;

@Data
public class BookRequestResponseDTO {
    private Long requestId;
    private String bookTitle;
    private RequestStatus status;
    private LocalDateTime requestDate;
    private LocalDateTime decisionDate;
    private String notes;
}
