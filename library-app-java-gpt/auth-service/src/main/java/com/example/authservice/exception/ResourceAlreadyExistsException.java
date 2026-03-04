// src/main/java/com/example/authservice/exception/ResourceAlreadyExistsException.java
package com.example.authservice.exception;

public class ResourceAlreadyExistsException extends ApiException {
    public ResourceAlreadyExistsException(String message) {
        super(message);
    }
}
