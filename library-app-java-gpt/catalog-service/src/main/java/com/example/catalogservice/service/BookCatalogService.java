package com.example.catalogservice.service;

import com.example.catalogservice.dto.*;
import com.example.catalogservice.entity.Book;
import com.example.catalogservice.exception.ResourceNotFoundException;
import com.example.catalogservice.repository.BookRepository;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class BookCatalogService {

    private final BookRepository bookRepository;

    public BookCatalogService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public Page<BookResponse> searchBooks(SearchRequest req) {
        int page = req.getPage() != null && req.getPage() >= 0 ? req.getPage() : 0;
        int size = req.getSize() != null && req.getSize() > 0 ? req.getSize() : 10;
        Sort.Direction dir = "desc".equalsIgnoreCase(req.getSortDir()) ? Sort.Direction.DESC : Sort.Direction.ASC;
        String sortBy = req.getSortBy() != null ? req.getSortBy() : "title";
        Pageable pageable = PageRequest.of(page, size, Sort.by(dir, sortBy));

        Page<Book> result = bookRepository.search(
                blankToNull(req.getTitle()),
                blankToNull(req.getAuthor()),
                blankToNull(req.getKeyword()),
                pageable
        );

        return result.map(this::toResponse);
    }

    @Transactional
    public BookResponse addBook(BookRequest req) {
        Book book = new Book(UUID.randomUUID(), req.getTitle(), req.getAuthor(),
                req.getIsbn(), req.getPublishedDate(), req.getGenre(),
                req.getCopiesAvailable());
        Book saved = bookRepository.save(book);
        return toResponse(saved);
    }

    @Transactional
    public BookResponse updateBook(UUID id, BookRequest req) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));

        book.setTitle(req.getTitle());
        book.setAuthor(req.getAuthor());
        book.setIsbn(req.getIsbn());
        book.setPublishedDate(req.getPublishedDate());
        book.setGenre(req.getGenre());
        book.setCopiesAvailable(req.getCopiesAvailable());

        Book saved = bookRepository.save(book);
        return toResponse(saved);
    }

    public BookResponse getById(UUID id) {
        Book book = bookRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found"));
        return toResponse(book);
    }

    private BookResponse toResponse(Book b) {
        return new BookResponse(b.getId(), b.getTitle(), b.getAuthor(), b.getIsbn(),
                b.getPublishedDate(), b.getGenre(), b.getCopiesAvailable(), b.isAvailable());
    }

    private String blankToNull(String s) {
        if (s == null) return null;
        s = s.trim();
        return s.isEmpty() ? null : s;
    }
}
