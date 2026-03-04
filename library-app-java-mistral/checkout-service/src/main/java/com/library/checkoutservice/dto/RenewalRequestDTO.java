package com.library.checkoutservice.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class RenewalRequestDTO {
    @NotNull(message = "Checkout ID is required")
    private Long checkoutId;
}
