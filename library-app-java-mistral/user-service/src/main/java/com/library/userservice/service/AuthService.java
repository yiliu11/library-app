package com.library.userservice.service;

import com.library.userservice.dto.LoginRequestDTO;
import com.library.userservice.dto.LoginResponseDTO;
import com.library.userservice.exception.ResourceNotFoundException;
import com.library.userservice.exception.UnauthorizedException;
import com.library.userservice.model.User;
import com.library.userservice.repository.UserRepository;
import com.library.userservice.security.JwtTokenUtil;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    private final AuthenticationManager authenticationManager;
    private final JwtTokenUtil jwtTokenUtil;
    private final UserRepository userRepository;
    private final CustomUserDetailsService userDetailsService;

    public AuthService(AuthenticationManager authenticationManager, JwtTokenUtil jwtTokenUtil,
                        UserRepository userRepository, CustomUserDetailsService userDetailsService) {
        this.authenticationManager = authenticationManager;
        this.jwtTokenUtil = jwtTokenUtil;
        this.userRepository = userRepository;
        this.userDetailsService = userDetailsService;
    }

    public LoginResponseDTO login(LoginRequestDTO loginRequest) {
        User user = userRepository.findByUsername(loginRequest.getUsername())
                .orElseThrow(() -> new ResourceNotFoundException("User not found."));

        if (!user.isActive()) {
            throw new UnauthorizedException("Account is locked. Please contact the administrator.");
        }

        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getUsername(), loginRequest.getPassword())
        );

        UserDetails userDetails = userDetailsService.loadUserByUsername(loginRequest.getUsername());
        String token = jwtTokenUtil.generateToken(userDetails);

        user.setFailedLoginAttempts(0);
        userRepository.save(user);

        LoginResponseDTO response = new LoginResponseDTO();
        response.setToken(token);
        response.setRole(((CustomUserDetails) userDetails).getRole());
        response.setUserId(user.getId());
        return response;
    }

    public void logout(String token) {
        // In a real-world scenario, you might add the token to a blacklist.
        // For JWT, tokens are stateless, so logout is handled client-side by discarding the token.
    }
}
