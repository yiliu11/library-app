package com.example.checkoutservice.controller;

import com.example.checkoutservice.dto.*;
import com.example.checkoutservice.exception.UnauthorizedException;
import com.example.checkoutservice.service.LoanService;
import org.springframework.http.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/loans")
@Validated
public class LoanController {

    private final LoanService loanService;

    public LoanController(LoanService loanService) {
        this.loanService = loanService;
    }

    /**
     * Checkout a book
     */
    @PostMapping("/checkout")
    public ResponseEntity<LoanResponse> checkout(@Valid @RequestBody CheckoutRequest request,
                                                 Authentication authentication) {
        UUID userId = extractUserId(authentication);
        String token = extractJwtFromAuth(authentication);
        LoanResponse resp = loanService.checkout(userId, request.getBookId(), token);
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    /**
     * Renew loan
     */
    @PostMapping("/{loanId}/renew")
    public ResponseEntity<LoanResponse> renew(@PathVariable("loanId") UUID loanId,
                                              Authentication authentication) {
        UUID userId = extractUserId(authentication);
        LoanResponse resp = loanService.renew(userId, loanId);
        return ResponseEntity.ok(resp);
    }

    /**
     * Get my loans
     */
    @GetMapping("/me")
    public ResponseEntity<List<LoanResponse>> myLoans(Authentication authentication) {
        UUID userId = extractUserId(authentication);
        List<LoanResponse> list = loanService.getLoansForUser(userId);
        return ResponseEntity.ok(list);
    }

    /**
     * Get loan by id (owner OR librarian)
     */
    @GetMapping("/{id}")
    public ResponseEntity<LoanResponse> getLoan(@PathVariable("id") UUID id,
                                                Authentication authentication) {
        UUID requesterId = extractUserId(authentication);
        boolean isLibrarian = hasRole(authentication, "LIBRARIAN");
        LoanResponse resp = loanService.getLoan(requesterId, id, isLibrarian);
        return ResponseEntity.ok(resp);
    }

    private UUID extractUserId(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated()) {
            throw new UnauthorizedException("Authentication required");
        }
        Object principal = authentication.getPrincipal();
        if (principal instanceof com.example.checkoutservice.security.CustomUserPrincipal) {
            return ((com.example.checkoutservice.security.CustomUserPrincipal) principal).getUserId();
        }
        throw new UnauthorizedException("Unable to extract user id from authentication principal");
    }

    private String extractJwtFromAuth(Authentication authentication) {
    Object credentials = authentication.getCredentials();
    return credentials instanceof String ? (String) credentials : null;
}

    private boolean hasRole(Authentication authentication, String role) {
        if (authentication == null || !authentication.isAuthenticated()) return false;
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(a -> a.equals("ROLE_" + role));
    }
}
