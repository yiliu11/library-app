// src/main/java/com/example/authservice/dto/RegisterRequest.java
package com.example.authservice.dto;

import com.example.authservice.entity.Role;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class RegisterRequest {

    @NotBlank
    @Size(min = 3, max = 100)
    private String username;

    @NotBlank
    @Email
    private String email;

    @NotBlank
    @Size(min = 8, max = 128, message = "Password must be at least 8 characters")
    private String password;

    private Role role;

    public RegisterRequest() {}

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username.trim(); }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email.trim().toLowerCase(); }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }
}
