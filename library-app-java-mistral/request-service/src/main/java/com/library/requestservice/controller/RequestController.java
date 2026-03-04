package com.library.requestservice.controller;

import com.library.requestservice.dto.BookRequestDTO;
import com.library.requestservice.dto.BookRequestResponseDTO;
import com.library.requestservice.dto.RequestDecisionDTO;
import com.library.requestservice.service.RequestService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/requests")
public class RequestController {
    private final RequestService requestService;

    public RequestController(RequestService requestService) {
        this.requestService = requestService;
    }

    @PostMapping
    @PreAuthorize("hasRole('STAFF')")
    public ResponseEntity<BookRequestResponseDTO> submitRequest(
            @Valid @RequestBody BookRequestDTO requestDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        String userRole = userDetails.getAuthorities().stream()
                .findFirst()
                .map(authority -> authority.getAuthority().replace("ROLE_", ""))
                .orElse("PATRON");

        BookRequestResponseDTO response = requestService.submitRequest(requestDTO, userId, userRole);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/decide")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<BookRequestResponseDTO> processDecision(
            @Valid @RequestBody RequestDecisionDTO decisionDTO,
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        String userRole = userDetails.getAuthorities().stream()
                .findFirst()
                .map(authority -> authority.getAuthority().replace("ROLE_", ""))
                .orElse("PATRON");

        BookRequestResponseDTO response = requestService.processDecision(decisionDTO, userId, userRole);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/pending")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<List<BookRequestResponseDTO>> getPendingRequests() {
        List<BookRequestResponseDTO> requests = requestService.getPendingRequests();
        return ResponseEntity.ok(requests);
    }

    @GetMapping("/my-requests")
    @PreAuthorize("hasAnyRole('STAFF', 'PATRON')")
    public ResponseEntity<List<BookRequestResponseDTO>> getMyRequests(
            @AuthenticationPrincipal UserDetails userDetails) {
        Long userId = Long.parseLong(userDetails.getUsername());
        List<BookRequestResponseDTO> requests = requestService.getRequestsByRequester(userId);
        return ResponseEntity.ok(requests);
    }
}
