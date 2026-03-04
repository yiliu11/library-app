// src/main/java/com/example/authservice/dto/AuthResponse.java
package com.example.authservice.dto;

import com.example.authservice.entity.Role;

public class AuthResponse {

    private String token;
    private String tokenType = "Bearer";
    private Role role;

    public AuthResponse() {}

    public AuthResponse(String token, Role role) {
        this.token = token;
        this.role = role;
    }

    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }

    public String getTokenType() { return tokenType; }
    public void setTokenType(String tokenType) { this.tokenType = tokenType; }

    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }
}
