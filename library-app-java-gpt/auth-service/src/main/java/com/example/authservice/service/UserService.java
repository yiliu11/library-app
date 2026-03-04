// src/main/java/com/example/authservice/service/UserService.java
package com.example.authservice.service;

import com.example.authservice.entity.User;
import com.example.authservice.exception.ApiException;
import com.example.authservice.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findByUsernameOrThrow(String username) {
        return userRepository.findByUsername(username)
                .orElseThrow(() -> new ApiException("User not found"));
    }

    public User findById(UUID userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new ApiException("User not found"));
    }
}
