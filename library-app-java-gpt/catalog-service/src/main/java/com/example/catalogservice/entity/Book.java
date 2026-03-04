package com.example.catalogservice.entity;

import javax.persistence.*;
import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "books", indexes = {
        @Index(name = "idx_books_title", columnList = "title"),
        @Index(name = "idx_books_author", columnList = "author"),
        @Index(name = "idx_books_isbn", columnList = "isbn")
})
public class Book {

    @Id
    @Column(name = "id", nullable = false, updatable = false)
    private UUID id;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(nullable = false, length = 300)
    private String author;

    @Column(nullable = true, length = 20)
    private String isbn;

    @Column(name = "published_date")
    private LocalDate publishedDate;

    @Column(length = 100)
    private String genre;

    @Column(name = "copies_available", nullable = false)
    private int copiesAvailable;

    protected Book() {
        // JPA
    }

    public Book(UUID id, String title, String author, String isbn,
                LocalDate publishedDate, String genre, int copiesAvailable) {
        this.id = id;
        this.title = title;
        this.author = author;
        this.isbn = isbn;
        this.publishedDate = publishedDate;
        this.genre = genre;
        this.copiesAvailable = copiesAvailable;
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

    public boolean isAvailable() {
        return copiesAvailable > 0;
    }

    public void decrementCopy() {
        if (copiesAvailable <= 0) throw new IllegalStateException("No copies available");
        copiesAvailable--;
    }

    public void incrementCopy() {
        copiesAvailable++;
    }
}
