package com.example.catalogservice.dto;

import javax.validation.constraints.*;
import java.time.LocalDate;

public class BookRequest {

    @NotBlank
    @Size(max = 500)
    private String title;

    @NotBlank
    @Size(max = 300)
    private String author;

    @Size(max = 20)
    private String isbn;

    private LocalDate publishedDate;

    @Size(max = 100)
    private String genre;

    @Min(0)
    private int copiesAvailable = 1;

    public BookRequest() {}

    // getters and setters

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title != null ? title.trim() : null; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author != null ? author.trim() : null; }

    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn != null ? isbn.trim() : null; }

    public LocalDate getPublishedDate() { return publishedDate; }
    public void setPublishedDate(LocalDate publishedDate) { this.publishedDate = publishedDate; }

    public String getGenre() { return genre; }
    public void setGenre(String genre) { this.genre = genre != null ? genre.trim() : null; }

    public int getCopiesAvailable() { return copiesAvailable; }
    public void setCopiesAvailable(int copiesAvailable) { this.copiesAvailable = copiesAvailable; }
}
