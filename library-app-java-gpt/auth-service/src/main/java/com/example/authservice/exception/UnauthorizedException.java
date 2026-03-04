// src/main/java/com/example/authservice/exception/UnauthorizedException.java
package com.example.authservice.exception;

public class UnauthorizedException extends ApiException {
    public UnauthorizedException(String message) {
        super(message);
    }
}
