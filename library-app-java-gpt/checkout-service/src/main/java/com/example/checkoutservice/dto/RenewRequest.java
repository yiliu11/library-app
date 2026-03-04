package com.example.checkoutservice.dto;

import javax.validation.constraints.NotNull;
import java.util.UUID;

public class RenewRequest {
    @NotNull
    private UUID loanId;

    public RenewRequest() {}

    public UUID getLoanId() { return loanId; }
    public void setLoanId(UUID loanId) { this.loanId = loanId; }
}
