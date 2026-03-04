package com.example.catalogservice.dto;

import java.time.LocalDate;
import java.util.UUID;

public class BookResponse {

    private UUID id;
    private String title;
    private String author;
    private String isbn;
    private LocalDate publishedDate;
    private String genre;
    private int copiesAvailable;
    private boolean available;

    public BookResponse() {}

    public BookResponse(UUID id, String title, String author, String isbn,
                        LocalDate publishedDate, String genre, int copiesAvailable, boolean available) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publishedDate = publishedDate;
        this.genre = genre;
        this.copiesAvailable = copiesAvailable;
        this.available = available;
    }

    // getters and setters

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author; }

    public String getIsbn() { return isbn; }
    public void setIsbn(String isbn) { this.isbn = isbn; }

    public LocalDate getPublishedDate() { return publishedDate; }
    public void setPublishedDate(LocalDate publishedDate) { this.publishedDate = publishedDate; }

    public String getGenre() { return genre; }
    public void setGenre(String genre) { this.genre = genre; }

    public int getCopiesAvailable() { return copiesAvailable; }
    public void setCopiesAvailable(int copiesAvailable) { this.copiesAvailable = copiesAvailable; }

    public boolean isAvailable() { return available; }
    public void setAvailable(boolean available) { this.available = available; }
}
