package com.example.userservice.controller;

import com.example.userservice.dto.*;
import com.example.userservice.entity.Role;
import com.example.userservice.exception.UnauthorizedException;
import com.example.userservice.security.CustomUserPrincipal;
import com.example.userservice.service.UserService;
import org.springframework.data.domain.Page;
import org.springframework.http.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.Optional;
import java.util.UUID;

@RestController
@RequestMapping("/api/users")
@Validated
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) { this.userService = userService; }

    /**
     * List users (Librarian only)
     * Optional ?role=STAFF
     */
    @GetMapping
    public ResponseEntity<Page<UserResponseDto>> listUsers(@RequestParam(value = "role", required = false) String role,
                                                           @RequestParam(value = "page", defaultValue = "0") int page,
                                                           @RequestParam(value = "size", defaultValue = "20") int size,
                                                           Authentication authentication) {
        enforceRole(authentication, "LIBRARIAN");
        Optional<Role> roleFilter = Optional.empty();
        if (role != null && !role.isBlank()) {
            try {
                roleFilter = Optional.of(Role.valueOf(role.toUpperCase()));
            } catch (IllegalArgumentException ex) {
                return ResponseEntity.badRequest().build();
            }
        }
        Page<UserResponseDto> resp = userService.listUsers(roleFilter, page, size);
        return ResponseEntity.ok(resp);
    }

    /**
     * Get user by id (librarian or the user themself)
     */
    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDto> getUser(@PathVariable("id") UUID id, Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        boolean isLibrarian = hasRole(authentication, "LIBRARIAN");
        if (!isLibrarian && !principal.getUserId().equals(id)) {
            throw new UnauthorizedException("Insufficient privileges");
        }
        UserResponseDto resp = userService.getById(id);
        return ResponseEntity.ok(resp);
    }

    /**
     * Create user (Librarian only)
     */
    @PostMapping
    public ResponseEntity<UserResponseDto> createUser(@Valid @RequestBody CreateUserDto dto, Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        enforceRole(authentication, "LIBRARIAN");
        UserResponseDto resp = userService.createUser(dto, principal.getUserId(), getRole(authentication));
        return ResponseEntity.status(HttpStatus.CREATED).body(resp);
    }

    /**
     * Update user (Librarian or user themself)
     */
    @PutMapping("/{id}")
    public ResponseEntity<UserResponseDto> updateUser(@PathVariable("id") UUID id,
                                                      @Valid @RequestBody UpdateUserDto dto,
                                                      Authentication authentication) {
        CustomUserPrincipal principal = extractPrincipal(authentication);
        boolean isLibrarian = hasRole(authentication, "LIBRARIAN");
        if (!isLibrarian && !principal.getUserId().equals(id)) {
            throw new UnauthorizedException("Insufficient privileges");
        }
        UserResponseDto resp = userService.updateUser(id, dto, principal.getUserId(), getRole(authentication));
        return ResponseEntity.ok(resp);
    }

    /**
     * Delete user (Librarian only)
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable("id") UUID id, Authentication authentication) {
        enforceRole(authentication, "LIBRARIAN");
        CustomUserPrincipal principal = extractPrincipal(authentication);
        userService.deleteUser(id, principal.getUserId(), getRole(authentication));
        return ResponseEntity.noContent().build();
    }

    // helpers

    private CustomUserPrincipal extractPrincipal(Authentication authentication) {
        if (authentication == null || !authentication.isAuthenticated() || !(authentication.getPrincipal() instanceof CustomUserPrincipal)) {
            throw new UnauthorizedException("Invalid authentication principal");
        }
        return (CustomUserPrincipal) authentication.getPrincipal();
    }

    private void enforceRole(Authentication authentication, String role) {
        if (!hasRole(authentication, role)) {
            throw new UnauthorizedException("Requires role: " + role);
        }
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
                .findFirst().orElse(null);
    }
}
