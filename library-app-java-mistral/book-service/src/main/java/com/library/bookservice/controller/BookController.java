package com.library.bookservice.controller;

import com.library.bookservice.dto.BookDTO;
import com.library.bookservice.dto.BookRequestDTO;
import com.library.bookservice.dto.BookSearchDTO;
import com.library.bookservice.model.Book.AvailabilityStatus;
import com.library.bookservice.service.BookService;
import com.library.bookservice.service.UserRole;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/books")
public class BookController {
    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @PostMapping
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<BookDTO> addBook(
            @Valid @RequestBody BookRequestDTO bookRequestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        UserRole role = extractRole(userDetails);
        BookDTO bookDTO = bookService.addBook(bookRequestDTO, role);
        return ResponseEntity.ok(bookDTO);
    }

    @PutMapping("/{bookId}")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<BookDTO> updateBook(
            @PathVariable Long bookId,
            @Valid @RequestBody BookRequestDTO bookRequestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        UserRole role = extractRole(userDetails);
        BookDTO bookDTO = bookService.updateBook(bookId, bookRequestDTO, role);
        return ResponseEntity.ok(bookDTO);
    }

    @DeleteMapping("/{bookId}")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<Void> deleteBook(
            @PathVariable Long bookId,
            @AuthenticationPrincipal UserDetails userDetails) {
        UserRole role = extractRole(userDetails);
        bookService.deleteBook(bookId, role);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/search")
    public ResponseEntity<List<BookDTO>> searchBooks(@Valid @RequestBody BookSearchDTO searchDTO) {
        List<BookDTO> books = bookService.searchBooks(searchDTO);
        return ResponseEntity.ok(books);
    }

    @GetMapping("/{bookId}")
    public ResponseEntity<BookDTO> getBookById(@PathVariable Long bookId) {
        BookDTO bookDTO = bookService.getBookById(bookId);
        return ResponseEntity.ok(bookDTO);
    }

    @GetMapping
    public ResponseEntity<List<BookDTO>> getAllBooks() {
        List<BookDTO> books = bookService.getAllBooks();
        return ResponseEntity.ok(books);
    }

    @PutMapping("/{bookId}/availability")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<Void> updateBookAvailability(
            @PathVariable Long bookId,
            @RequestParam AvailabilityStatus status,
            @AuthenticationPrincipal UserDetails userDetails) {
        UserRole role = extractRole(userDetails);
        bookService.updateBookAvailability(bookId, status, role);
        return ResponseEntity.noContent().build();
    }

    private UserRole extractRole(UserDetails userDetails) {
        String role = userDetails.getAuthorities().stream()
                .findFirst()
                .map(authority -> authority.getAuthority().replace("ROLE_", ""))
                .orElse("PATRON");
        return UserRole.valueOf(role);
    }
}
