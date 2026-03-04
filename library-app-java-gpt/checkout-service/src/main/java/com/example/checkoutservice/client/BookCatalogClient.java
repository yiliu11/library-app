package com.example.checkoutservice.client;

import com.example.checkoutservice.dto.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.*;

import java.util.Map;
import java.util.UUID;

@Component
public class BookCatalogClient {

    private final RestTemplate restTemplate;
    private final String baseUrl;

    public BookCatalogClient(@Value("${app.catalog.base-url}") String baseUrl) {
        this.restTemplate = new RestTemplate();
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length()-1) : baseUrl;
    }

    public BookInfo getBook(UUID bookId) {
        String url = baseUrl + "/api/books/" + bookId.toString();
        try {
            ResponseEntity<BookInfo> resp = restTemplate.getForEntity(url, BookInfo.class);
            return resp.getBody();
        } catch (HttpClientErrorException.NotFound ex) {
            return null;
        } catch (RestClientException ex) {
            throw new RuntimeException("Failed to call Book Catalog service: " + ex.getMessage(), ex);
        }
    }

    public BookInfo updateCopies(UUID bookId, int newCopies, String jwtToken) {
        // we will call the PUT /api/books/{id} with a BookRequest containing updated copies
        String url = baseUrl + "/api/books/" + bookId.toString();

        // We must fetch the current book first
        BookInfo current = getBook(bookId);
        if (current == null) {
            throw new RuntimeException("Book not found in catalog");
        }
        // Build request body
        Map<String, Object> body = Map.of(
                "title", current.getTitle(),
                "author", current.getAuthor(),
                "isbn", current.getIsbn(),
                "publishedDate", current.getPublishedDate(),
                "genre", current.getGenre(),
                "copiesAvailable", newCopies
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        if (jwtToken != null) headers.setBearerAuth(jwtToken);

        HttpEntity<Map<String,Object>> entity = new HttpEntity<>(body, headers);
        try {
            ResponseEntity<BookInfo> resp = restTemplate.exchange(url, HttpMethod.PUT, entity, BookInfo.class);
            return resp.getBody();
        } catch (HttpClientErrorException.Forbidden ex) {
            throw new RuntimeException("Forbidden to update book in catalog");
        } catch (HttpClientErrorException.NotFound ex) {
            throw new RuntimeException("Book not found when updating");
        } catch (RestClientException ex) {
            throw new RuntimeException("Failed to update Book Catalog: " + ex.getMessage(), ex);
        }
    }

    // DTO representing minimal Book info returned by catalog
    public static class BookInfo {
        private String id;
        private String title;
        private String author;
        private String isbn;
        private String publishedDate; // ISO date string
        private String genre;
        private int copiesAvailable;
        private boolean available;

        public BookInfo() {}

        // getters and setters
        public String getId() { return id; }
        public void setId(String id) { this.id = id; }
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        public String getAuthor() { return author; }
        public void setAuthor(String author) { this.author = author; }
        public String getIsbn() { return isbn; }
        public void setIsbn(String isbn) { this.isbn = isbn; }
        public String getPublishedDate() { return publishedDate; }
        public void setPublishedDate(String publishedDate) { this.publishedDate = publishedDate; }
        public String getGenre() { return genre; }
        public void setGenre(String genre) { this.genre = genre; }
        public int getCopiesAvailable() { return copiesAvailable; }
        public void setCopiesAvailable(int copiesAvailable) { this.copiesAvailable = copiesAvailable; }
        public boolean isAvailable() { return available; }
        public void setAvailable(boolean available) { this.available = available; }
    }
}
