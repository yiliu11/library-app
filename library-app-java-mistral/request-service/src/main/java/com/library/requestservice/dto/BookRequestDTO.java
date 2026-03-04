package com.library.requestservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

@Data
public class BookRequestDTO {
    @NotBlank(message = "Book title is required")
    private String bookTitle;

    @NotBlank(message = "Book author is required")
    private String bookAuthor;

    @Pattern(regexp = "^\\d{10,13}$|^$", message = "ISBN must be 10-13 digits or empty")
    private String bookIsbn;
}
