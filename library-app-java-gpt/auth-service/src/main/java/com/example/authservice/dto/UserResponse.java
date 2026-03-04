// src/main/java/com/example/authservice/dto/UserResponse.java
package com.example.authservice.dto;

import com.example.authservice.entity.Role;

import java.util.UUID;

public class UserResponse {
    private UUID id;
    private String username;
    private String email;
    private Role role;

    public UserResponse() {}

    public UserResponse(UUID id, String username, String email, Role role) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.role = role;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }
}
