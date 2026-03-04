package com.library.bookservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BookSearchDTO {
    @NotBlank(message = "Search term is required")
    private String searchTerm;

    @NotNull(message = "Search criteria is required")
    private SearchCriteria searchCriteria;

    public enum SearchCriteria {
        TITLE, AUTHOR, ISBN
    }
}
