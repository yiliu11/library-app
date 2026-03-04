package com.library.bookservice.dto;

import com.library.bookservice.model.Book.AvailabilityStatus;
import lombok.Data;

import java.time.LocalDate;

@Data
public class BookDTO {
    private Long id;
    private String title;
    private String author;
    private String isbn;
    private LocalDate publicationDate;
    private AvailabilityStatus availabilityStatus;
}
