package com.example.userservice.service;

import com.example.userservice.client.AuthServiceClient;
import com.example.userservice.dto.*;
import com.example.userservice.entity.*;
import com.example.userservice.exception.*;
import com.example.userservice.repository.UserRepository;
import org.springframework.data.domain.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final AuthServiceClient authServiceClient;

    public UserService(UserRepository userRepository, AuthServiceClient authServiceClient) {
        this.userRepository = userRepository;
        this.authServiceClient = authServiceClient;
    }

    public Page<UserResponseDto> listUsers(Optional<Role> roleFilter, int page, int size) {
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.ASC, "username"));
        Page<UserEntity> pageResult = roleFilter.map(role -> userRepository.findByRole(role, pageable))
                .orElse(userRepository.findAll(pageable));
        return pageResult.map(this::toDto);
    }

    public UserResponseDto getById(UUID id) {
        UserEntity e = userRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));
        return toDto(e);
    }

    @Transactional
    public UserResponseDto createUser(CreateUserDto dto, UUID actingUserId, String actingRole) {
        // Only librarians should call createUser; controller enforces role. Still check for uniqueness.
        if (userRepository.existsByUsername(dto.getUsername())) {
            throw new ApiException("Username already exists");
        }
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new ApiException("Email already exists");
        }

        // 1) Forward to Auth service to create credentials (and hash password)
        try {
            authServiceClient.registerUser(dto);
        } catch (RuntimeException ex) {
            throw new ApiException("Failed to create credentials: " + ex.getMessage());
        }

        // 2) Create profile in local DB
        UserEntity e = new UserEntity(UUID.randomUUID(), dto.getUsername(), dto.getEmail(), dto.getFullName(), dto.getRole());
        UserEntity saved = userRepository.save(e);
        return toDto(saved);
    }

    @Transactional
    public UserResponseDto updateUser(UUID id, UpdateUserDto dto, UUID actingUserId, String actingRole) {
        UserEntity e = userRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));

        if (dto.getUsername() != null && !dto.getUsername().equals(e.getUsername())) {
            if (userRepository.existsByUsername(dto.getUsername())) {
                throw new ApiException("Username already exists");
            }
            e.setUsername(dto.getUsername());
        }
        if (dto.getEmail() != null && !dto.getEmail().equals(e.getEmail())) {
            if (userRepository.existsByEmail(dto.getEmail())) {
                throw new ApiException("Email already exists");
            }
            e.setEmail(dto.getEmail());
        }
        if (dto.getFullName() != null) e.setFullName(dto.getFullName());
        if (dto.getRole() != null) e.setRole(dto.getRole());

        e.setUpdatedAt(Instant.now());
        UserEntity saved = userRepository.save(e);
        return toDto(saved);
    }

    @Transactional
    public void deleteUser(UUID id, UUID actingUserId, String actingRole) {
        UserEntity e = userRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));
        userRepository.delete(e);
        // Optionally: notify Auth service to remove credentials or disable account
    }

    private UserResponseDto toDto(UserEntity e) {
        return new UserResponseDto(e.getId(), e.getUsername(), e.getEmail(), e.getFullName(), e.getRole(), e.getCreatedAt(), e.getUpdatedAt());
    }
}
