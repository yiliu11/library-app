package com.example.requestservice.config;

import com.example.requestservice.security.JwtAuthenticationFilter;
import com.example.requestservice.security.JwtProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.*;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.*;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableMethodSecurity
public class SecurityConfig {

    @Autowired
    private JwtProvider jwtProvider;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        JwtAuthenticationFilter jwtFilter = new JwtAuthenticationFilter(jwtProvider);

        http
            .csrf().disable()
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS).and()
            .authorizeRequests()
                // staff can create requests; librarians can view and approve/reject
                .antMatchers(HttpMethod.POST, "/api/requests").authenticated()
                .antMatchers(HttpMethod.GET, "/api/requests/mine").authenticated()
                .antMatchers(HttpMethod.GET, "/api/requests/**").authenticated()
                .antMatchers(HttpMethod.PUT, "/api/requests/**/approve", "/api/requests/**/reject").authenticated()
                .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
