package com.example.userservice.security;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.UUID;

public class CustomUserPrincipal implements UserDetails {

    private final UUID userId;
    private final String username;
    private final String token;
    private final Collection<? extends GrantedAuthority> authorities;

    public CustomUserPrincipal(UUID userId, String username, String token, Collection<? extends GrantedAuthority> authorities) {
        this.userId = userId;
        this.username = username;
        this.token = token;
        this.authorities = authorities;
    }

    public UUID getUserId() { return userId; }
    public String getToken() { return token; }

    @Override public Collection<? extends GrantedAuthority> getAuthorities() { return authorities; }
    @Override public String getPassword() { return null; }
    @Override public String getUsername() { return username; }
    @Override public boolean isAccountNonExpired() { return true; }
    @Override public boolean isAccountNonLocked() { return true; }
    @Override public boolean isCredentialsNonExpired() { return true; }
    @Override public boolean isEnabled() { return true; }
}
