package com.example.requestservice.controller;

import com.example.requestservice.dto.*;
import com.example.requestservice.entity.RequestStatus;
import com.example.requestservice.exception.UnauthorizedException;
import com.example.requestservice.security.CustomUserPrincipal;
import com.example.requestservice.service.BookRequestService;
import org.springframework.data.domain.Page;
import org.springframework.http.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/requests")
@Validated
public class BookRequestController {

    private final BookRequestService service;

    public BookRequestController(BookRequestService service) {
        this.service = service;
    }

    /**
     * Create a new book request (Staff only)
     */
    @PostMapping
    public ResponseEntity<BookRequestResponseDto> createRequest(@Valid @RequestBody CreateBookRequestDto dto,
                                                                Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        if (!hasRole(authentication, "STAFF")) {
            throw new UnauthorizedException("Only staff can create book requests");
        }
        BookRequestResponseDto resp = service.createRequest(principal.getUserId(), dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    /**
     * List all requests (Librarian) or filter by status (librarian) 
     * Query params: ?status=PENDING&page=0&size=20
     */
    @GetMapping
    public ResponseEntity<Page<BookRequestResponseDto>> listRequests(@RequestParam(value = "status", required = false) String status,
                                                                      @RequestParam(value = "page", defaultValue = "0") int page,
                                                                      @RequestParam(value = "size", defaultValue = "20") int size,
                                                                      Authentication authentication) {
        // Librarian only
        if (!hasRole(authentication, "LIBRARIAN")) {
            throw new UnauthorizedException("Only librarians can list all requests");
        }
        Optional<RequestStatus> stat = Optional.empty();
        if (status != null && !status.isBlank()) {
            try {
                stat = Optional.of(RequestStatus.valueOf(status.toUpperCase()));
            } catch (IllegalArgumentException ex) {
                return ResponseEntity.badRequest().build();
            }
        }
        Page<BookRequestResponseDto> pageResult = service.listRequests(stat, page, size);
        return ResponseEntity.ok(pageResult);
    }

    /**
     * List requests created by caller
     */
    @GetMapping("/mine")
    public ResponseEntity<Page<BookRequestResponseDto>> myRequests(@RequestParam(value = "page", defaultValue = "0") int page,
                                                                   @RequestParam(value = "size", defaultValue = "20") int size,
                                                                   Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        Page<BookRequestResponseDto> pageResult = service.listRequestsForUser(principal.getUserId(), page, size);
        return ResponseEntity.ok(pageResult);
    }

    /**
     * Get single request
     * Librarians can get any; staff can only get own
     */
    @GetMapping("/{id}")
    public ResponseEntity<BookRequestResponseDto> getRequest(@PathVariable("id") UUID id,
                                                             Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        boolean isLibrarian = hasRole(authentication, "LIBRARIAN");
        BookRequestResponseDto resp = service.getById(id);
        if (!isLibrarian && !resp.getRequestedBy().equals(principal.getUserId())) {
            throw new UnauthorizedException("Insufficient privileges");
        }
        return ResponseEntity.ok(resp);
    }

    /**
     * Approve a request (Librarian only)
     */
    @PutMapping("/{id}/approve")
    public ResponseEntity<BookRequestResponseDto> approveRequest(@PathVariable("id") UUID id,
                                                                 @Valid @RequestBody(required = false) ApproveRequestDto dto,
                                                                 Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        if (!hasRole(authentication, "LIBRARIAN")) {
            throw new UnauthorizedException("Only librarians can approve requests");
        }
        String comments = dto == null ? null : dto.getComments();
        BookRequestResponseDto resp = service.approveRequest(id, comments, principal.getUserId(), getRole(authentication));
        return ResponseEntity.ok(resp);
    }

    /**
     * Reject a request (Librarian only)
     */
    @PutMapping("/{id}/reject")
    public ResponseEntity<BookRequestResponseDto> rejectRequest(@PathVariable("id") UUID id,
                                                                @Valid @RequestBody(required = false) ApproveRequestDto dto,
                                                                Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        if (!hasRole(authentication, "LIBRARIAN")) {
            throw new UnauthorizedException("Only librarians can reject requests");
        }
        String comments = dto == null ? null : dto.getComments();
        BookRequestResponseDto resp = service.rejectRequest(id, comments, principal.getUserId(), getRole(authentication));
        return ResponseEntity.ok(resp);
    }

    // helpers

    private CustomUserPrincipal extractPrincipal(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated() || !(authentication.getPrincipal() instanceof CustomUserPrincipal)) {
            throw new UnauthorizedException("Invalid authentication principal");
        }
        return (CustomUserPrincipal) authentication.getPrincipal();
    }

    private boolean hasRole(Authentication authentication, String role) {
        if (authentication == null || !authentication.isAuthenticated()) return false;
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(a -> a.equals("ROLE_" + role));
    }

    private String getRole(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) return null;
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .filter(a -> a.startsWith("ROLE_"))
                .map(a -> a.substring(5))
                .collect(Collectors.joining(","));
    }
}
