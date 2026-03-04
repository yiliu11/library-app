// src/main/java/com/example/authservice/service/AuthService.java
package com.example.authservice.service;

import com.example.authservice.dto.*;
import com.example.authservice.entity.Role;
import com.example.authservice.entity.User;
import com.example.authservice.exception.ResourceAlreadyExistsException;
import com.example.authservice.exception.UnauthorizedException;
import com.example.authservice.repository.UserRepository;
import com.example.authservice.security.JwtProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;

    public AuthService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       JwtProvider jwtProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
    }

    @Transactional
    public UserResponse register(RegisterRequest req) {
        if (userRepository.existsByUsername(req.getUsername())) {
            throw new ResourceAlreadyExistsException("Username already exists");
        }
        if (userRepository.existsByEmail(req.getEmail())) {
            throw new ResourceAlreadyExistsException("Email already exists");
        }

        Role role = req.getRole() != null ? req.getRole() : Role.PATRON; // default

        String hashed = passwordEncoder.encode(req.getPassword());
        User user = new User(UUID.randomUUID(), req.getUsername(), req.getEmail(), hashed, role);
        User saved = userRepository.save(user);
        return new UserResponse(saved.getId(), saved.getUsername(), saved.getEmail(), saved.getRole());
    }

    public AuthResponse login(LoginRequest req) {
        User user = userRepository.findByUsername(req.getUsername())
                .orElseThrow(() -> new UnauthorizedException("Invalid username or password"));

        if (!passwordEncoder.matches(req.getPassword(), user.getPasswordHash())) {
            throw new UnauthorizedException("Invalid username or password");
        }

        String token = jwtProvider.generateToken(user.getId(), user.getUsername(), user.getRole());
        return new AuthResponse(token, user.getRole());
    }
}
