package com.example.userservice.dto;

import com.example.userservice.entity.Role;

import javax.validation.constraints.*;

public class UpdateUserDto {

    @Size(min = 3, max = 100)
    private String username;

    @Email
    private String email;

    @Size(max = 200)
    private String fullName;

    private Role role;

    public UpdateUserDto() {}

    // getters and setters

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username != null ? username.trim() : null; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email != null ? email.trim().toLowerCase() : null; }

    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }

    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }
}
