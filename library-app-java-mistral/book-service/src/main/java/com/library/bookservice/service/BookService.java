package com.library.bookservice.service;

import com.library.bookservice.dto.BookDTO;
import com.library.bookservice.dto.BookRequestDTO;
import com.library.bookservice.dto.BookSearchDTO;
import com.library.bookservice.exception.DuplicateResourceException;
import com.library.bookservice.exception.ForbiddenException;
import com.library.bookservice.exception.ResourceNotFoundException;
import com.library.bookservice.model.Book;
import com.library.bookservice.model.Book.AvailabilityStatus;
import com.library.bookservice.model.UserRole;
import com.library.bookservice.repository.BookRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class BookService {
    private final BookRepository bookRepository;

    public BookService(BookRepository bookRepository) {
        this.bookRepository = bookRepository;
    }

    public BookDTO addBook(BookRequestDTO bookRequestDTO, UserRole userRole) {
        if (userRole != UserRole.LIBRARIAN) {
            throw new ForbiddenException("Only librarians can add books.");
        }

        if (bookRepository.existsByIsbn(bookRequestDTO.getIsbn())) {
            throw new DuplicateResourceException("A book with this ISBN already exists.");
        }

        Book book = new Book();
        book.setTitle(bookRequestDTO.getTitle());
        book.setAuthor(bookRequestDTO.getAuthor());
        book.setIsbn(bookRequestDTO.getIsbn());
        book.setPublicationDate(bookRequestDTO.getPublicationDate());
        book.setAvailabilityStatus(AvailabilityStatus.AVAILABLE);

        Book savedBook = bookRepository.save(book);
        return convertToDTO(savedBook);
    }

    public BookDTO updateBook(Long bookId, BookRequestDTO bookRequestDTO, UserRole userRole) {
        if (userRole != UserRole.LIBRARIAN) {
            throw new ForbiddenException("Only librarians can update books.");
        }

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));

        if (!book.getIsbn().equals(bookRequestDTO.getIsbn()) && bookRepository.existsByIsbn(bookRequestDTO.getIsbn())) {
            throw new DuplicateResourceException("A book with this ISBN already exists.");
        }

        book.setTitle(bookRequestDTO.getTitle());
        book.setAuthor(bookRequestDTO.getAuthor());
        book.setIsbn(bookRequestDTO.getIsbn());
        book.setPublicationDate(bookRequestDTO.getPublicationDate());

        Book updatedBook = bookRepository.save(book);
        return convertToDTO(updatedBook);
    }

    public void deleteBook(Long bookId, UserRole userRole) {
        if (userRole != UserRole.LIBRARIAN) {
            throw new ForbiddenException("Only librarians can delete books.");
        }

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));

        bookRepository.delete(book);
    }

    public List<BookDTO> searchBooks(BookSearchDTO searchDTO) {
        List<Book> books;
        switch (searchDTO.getSearchCriteria()) {
            case TITLE:
                books = bookRepository.findByTitleContainingIgnoreCase(searchDTO.getSearchTerm());
                break;
            case AUTHOR:
                books = bookRepository.findByAuthorContainingIgnoreCase(searchDTO.getSearchTerm());
                break;
            case ISBN:
                books = bookRepository.findByIsbn(searchDTO.getSearchTerm()).stream().toList();
                break;
            default:
                throw new IllegalArgumentException("Invalid search criteria.");
        }
        return books.stream().map(this::convertToDTO).collect(Collectors.toList());
    }

    public BookDTO getBookById(Long bookId) {
        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));
        return convertToDTO(book);
    }

    public List<BookDTO> getAllBooks() {
        return bookRepository.findAll().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());
    }

    public void updateBookAvailability(Long bookId, AvailabilityStatus status, UserRole userRole) {
        if (userRole != UserRole.LIBRARIAN) {
            throw new ForbiddenException("Only librarians can update book availability.");
        }

        Book book = bookRepository.findById(bookId)
                .orElseThrow(() -> new ResourceNotFoundException("Book not found with id: " + bookId));

        book.setAvailabilityStatus(status);
        bookRepository.save(book);
    }

    private BookDTO convertToDTO(Book book) {
        BookDTO bookDTO = new BookDTO();
        bookDTO.setId(book.getId());
        bookDTO.setTitle(book.getTitle());
        bookDTO.setAuthor(book.getAuthor());
        bookDTO.setIsbn(book.getIsbn());
        bookDTO.setPublicationDate(book.getPublicationDate());
        bookDTO.setAvailabilityStatus(book.getAvailabilityStatus());
        return bookDTO;
    }
}
