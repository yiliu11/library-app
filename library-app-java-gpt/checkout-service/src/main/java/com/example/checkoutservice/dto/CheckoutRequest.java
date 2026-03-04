package com.example.checkoutservice.dto;

import javax.validation.constraints.NotNull;
import java.util.UUID;

public class CheckoutRequest {

    @NotNull
    private UUID bookId;

    public CheckoutRequest() {}

    public UUID getBookId() { return bookId; }
    public void setBookId(UUID bookId) { this.bookId = bookId; }
}
