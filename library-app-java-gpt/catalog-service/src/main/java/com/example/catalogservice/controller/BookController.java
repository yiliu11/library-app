package com.example.catalogservice.controller;

import com.example.catalogservice.dto.*;
import com.example.catalogservice.exception.UnauthorizedException;
import com.example.catalogservice.service.BookCatalogService;
import org.springframework.data.domain.Page;
import org.springframework.http.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.security.Principal;
import java.util.UUID;

@RestController
@RequestMapping("/api/books")
@Validated
public class BookController {

    private final BookCatalogService bookService;

    public BookController(BookCatalogService bookService) {
        this.bookService = bookService;
    }

    /**
     * Search books with optional filters and pagination.
     */
    @GetMapping
    public ResponseEntity<Page<BookResponse>> searchBooks(
            @RequestParam(value = "title", required = false) String title,
            @RequestParam(value = "author", required = false) String author,
            @RequestParam(value = "keyword", required = false) String keyword,
            @RequestParam(value = "page", required = false, defaultValue = "0") Integer page,
            @RequestParam(value = "size", required = false, defaultValue = "10") Integer size,
            @RequestParam(value = "sortBy", required = false, defaultValue = "title") String sortBy,
            @RequestParam(value = "sortDir", required = false, defaultValue = "asc") String sortDir
    ) {
        SearchRequest req = new SearchRequest();
        req.setTitle(title);
        req.setAuthor(author);
        req.setKeyword(keyword);
        req.setPage(page);
        req.setSize(size);
        req.setSortBy(sortBy);
        req.setSortDir(sortDir);

        Page<BookResponse> result = bookService.searchBooks(req);
        return ResponseEntity.ok(result);
    }

    /**
     * Get single book by id.
     */
    @GetMapping("/{id}")
    public ResponseEntity<BookResponse> getBook(@PathVariable("id") UUID id) {
        BookResponse resp = bookService.getById(id);
        return ResponseEntity.ok(resp);
    }

    /**
     * Add a new book - LIBRARIAN role only.
     */
    @PostMapping
    public ResponseEntity<BookResponse> addBook(@Valid @RequestBody BookRequest request,
                                                Principal principal,
                                                Authentication authentication) {
        enforceRole(authentication, "LIBRARIAN");
        BookResponse created = bookService.addBook(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    /**
     * Update book details - LIBRARIAN only.
     */
    @PutMapping("/{id}")
    public ResponseEntity<BookResponse> updateBook(@PathVariable("id") UUID id,
                                                   @Valid @RequestBody BookRequest request,
                                                   Principal principal,
                                                   Authentication authentication) {
        enforceRole(authentication, "LIBRARIAN");
        BookResponse updated = bookService.updateBook(id, request);
        return ResponseEntity.ok(updated);
    }

    private void enforceRole(Authentication authentication, String requiredRole) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new UnauthorizedException("Authentication required");
        }
        boolean has = authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(a -> a.equals("ROLE_" + requiredRole));
        if (!has) {
            throw new UnauthorizedException("Insufficient privileges: requires " + requiredRole);
        }
    }
}
