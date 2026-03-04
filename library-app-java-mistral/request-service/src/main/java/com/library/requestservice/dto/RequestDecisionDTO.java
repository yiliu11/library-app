package com.library.requestservice.dto;

import com.library.requestservice.model.RequestStatus;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class RequestDecisionDTO {
    @NotNull(message = "Request ID is required")
    private Long requestId;

    @NotNull(message = "Status is required")
    private RequestStatus status;

    private String notes;
}
