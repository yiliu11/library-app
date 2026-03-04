package com.library.checkoutservice.controller;

import com.library.checkoutservice.dto.*;
import com.library.checkoutservice.service.CheckoutService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/checkouts")
public class CheckoutController {
    private final CheckoutService checkoutService;

    public CheckoutController(CheckoutService checkoutService) {
        this.checkoutService = checkoutService;
    }

    @PostMapping
    public ResponseEntity<CheckoutResponseDTO> checkoutBook(
            @Valid @RequestBody CheckoutRequestDTO requestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername()); // Assuming username is userId
        CheckoutResponseDTO response = checkoutService.checkoutBook(requestDTO, userId);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/renew")
    public ResponseEntity<CheckoutResponseDTO> renewCheckout(
            @Valid @RequestBody RenewalRequestDTO requestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        CheckoutResponseDTO response = checkoutService.renewCheckout(requestDTO, userId);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/return")
    public ResponseEntity<Void> returnBook(
            @Valid @RequestBody ReturnRequestDTO requestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        checkoutService.returnBook(requestDTO, userId);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/records/{userId}")
    public ResponseEntity<UserRecordDTO> getUserRecords(
            @PathVariable Long userId,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long requestingUserId = Long.parseLong(userDetails.getUsername());
        String requestingUserRole = userDetails.getAuthorities().stream()
                .findFirst()
                .map(authority -> authority.getAuthority().replace("ROLE_", ""))
                .orElse("PATRON");

        UserRecordDTO recordDTO = checkoutService.getUserRecords(userId, requestingUserId, requestingUserRole);
        return ResponseEntity.ok(recordDTO);
    }
}
