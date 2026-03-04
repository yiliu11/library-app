// src/main/java/com/example/authservice/exception/ApiException.java
package com.example.authservice.exception;

public class ApiException extends RuntimeException {
    public ApiException(String message) {
        super(message);
    }
    public ApiException(String message, Throwable cause) {
        super(message, cause);
    }
}
