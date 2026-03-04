// src/main/java/com/example/authservice/dto/LoginRequest.java
package com.example.authservice.dto;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class LoginRequest {

    @NotBlank
    private String username;

    @NotBlank
    @Size(min = 8)
    private String password;

    public LoginRequest() {}

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username.trim(); }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
