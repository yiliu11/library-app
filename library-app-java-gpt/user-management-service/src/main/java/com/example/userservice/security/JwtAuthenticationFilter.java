package com.example.userservice.security;

import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.*;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.*;
import java.io.IOException;
import java.util.Collections;
import java.util.UUID;

public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtProvider jwtProvider;

    public JwtAuthenticationFilter(JwtProvider jwtProvider) {
        this.jwtProvider = jwtProvider;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        String header = request.getHeader(HttpHeaders.AUTHORIZATION);
        String token = null;
        if (StringUtils.hasText(header) && header.startsWith("Bearer ")) {
            token = header.substring(7);
        }

        if (token != null && jwtProvider.validateToken(token)) {
            try {
                String username = jwtProvider.getUsernameFromToken(token);
                String role = jwtProvider.getRoleFromToken(token); // expects PATRON/STAFF/LIBRARIAN
                UUID userId = jwtProvider.getUserIdFromToken(token);
                if (role != null && userId != null) {
                    GrantedAuthority authority = new SimpleGrantedAuthority("ROLE_" + role);
                    CustomUserPrincipal principal = new CustomUserPrincipal(userId, username, token, Collections.singleton(authority));
                    Authentication auth = new UsernamePasswordAuthenticationToken(principal, token, Collections.singleton(authority));
                    SecurityContextHolder.getContext().setAuthentication(auth);
                }
            } catch (Exception ex) {
                // token invalid -> do not set authentication
            }
        }
        filterChain.doFilter(request, response);
    }
}
