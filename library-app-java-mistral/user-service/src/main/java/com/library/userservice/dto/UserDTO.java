package com.library.userservice.dto;

import com.library.userservice.model.User.UserRole;
import lombok.Data;

@Data
public class UserDTO {
    private Long id;
    private String username;
    private String email;
    private UserRole role;
}
