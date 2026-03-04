package com.library.userservice.controller;

import com.library.userservice.dto.UserDTO;
import com.library.userservice.dto.UserRegistrationDTO;
import com.library.userservice.model.User.UserRole;
import com.library.userservice.security.CustomUserDetails;
import com.library.userservice.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    @PreAuthorize("hasRole('LIBRARIAN')")
    public ResponseEntity<UserDTO> registerUser(
            @Valid @RequestBody UserRegistrationDTO registrationDTO,
            @AuthenticationPrincipal CustomUserDetails currentUser) {
        UserDTO userDTO = userService.registerUser(registrationDTO, currentUser.getRole());
        return ResponseEntity.ok(userDTO);
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('LIBRARIAN', 'STAFF')")
    public ResponseEntity<List<UserDTO>> getAllUsers() {
        List<UserDTO> users = userService.getAllUsers();
        return ResponseEntity.ok(users);
    }

    @GetMapping("/{userId}")
    @PreAuthorize("hasAnyRole('LIBRARIAN', 'STAFF')")
    public ResponseEntity<UserDTO> getUserById(@PathVariable Long userId) {
        UserDTO userDTO = userService.getUserById(userId);
        return ResponseEntity.ok(userDTO);
    }
}
