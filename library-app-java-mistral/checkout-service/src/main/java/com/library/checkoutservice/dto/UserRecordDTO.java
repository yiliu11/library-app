package com.library.checkoutservice.dto;

import lombok.Data;

import java.math.BigDecimal;
import java.util.List;

@Data
public class UserRecordDTO {
    private Long userId;
    private List<CheckedOutItemDTO> checkedOutItems;
    private BigDecimal totalFines;
}
