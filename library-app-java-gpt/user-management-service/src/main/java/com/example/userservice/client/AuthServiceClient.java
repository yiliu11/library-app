package com.example.userservice.client;

import com.example.userservice.dto.CreateUserDto;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.*;

import java.util.Map;

@Component
public class AuthServiceClient {

    private final RestTemplate restTemplate = new RestTemplate();
    private final String baseUrl;

    public AuthServiceClient(@Value("${app.auth.base-url}") String baseUrl) {
        this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length()-1) : baseUrl;
    }

    /**
     * Forward registration to Auth Service /api/auth/register
     * Returns the Auth service response body as Map (or throws in case of failure).
     */
    public Map<String, Object> registerUser(CreateUserDto dto) {
        String url = baseUrl + "/api/auth/register";

        // Build payload expected by Auth service DTO
        Map<String, Object> payload = Map.of(
                "username", dto.getUsername(),
                "email", dto.getEmail(),
                "password", dto.getInitialPassword() != null ? dto.getInitialPassword() : generateRandomPassword(),
                "role", dto.getRole().name()
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String,Object>> entity = new HttpEntity<>(payload, headers);
        try {
            ResponseEntity<Map> resp = restTemplate.postForEntity(url, entity, Map.class);
            return resp.getBody();
        } catch (HttpClientErrorException.Conflict ex) {
            throw new RuntimeException("Auth service reported conflict: " + ex.getResponseBodyAsString());
        } catch (RestClientException ex) {
            throw new RuntimeException("Failed to call Auth service: " + ex.getMessage(), ex);
        }
    }

    private String generateRandomPassword() {
        // Simple random password generator: in production use a secure generator and email the password
        return "ChangeMe!" + System.currentTimeMillis() % 10000;
    }
}
