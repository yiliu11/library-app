package com.library.userservice.dto;

import com.library.userservice.model.User.UserRole;
import lombok.Data;

@Data
public class LoginResponseDTO {
    private String token;
    private UserRole role;
    private Long userId;
}
