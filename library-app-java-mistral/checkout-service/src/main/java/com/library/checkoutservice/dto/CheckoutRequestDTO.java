package com.library.checkoutservice.dto;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class CheckoutRequestDTO {
    @NotNull(message = "User ID is required")
    private Long userId;

    @NotNull(message = "Book ID is required")
    private Long bookId;
}
