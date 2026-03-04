package com.library.checkoutservice.client;

import com.library.checkoutservice.dto.BookDTO;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.*;

@FeignClient(name = "book-service", url = "${book.service.url:http://localhost:8082}")
public interface BookServiceClient {
    @GetMapping("/api/books/{bookId}")
    BookDTO getBookById(@PathVariable Long bookId);

    @PutMapping("/api/books/{bookId}/availability")
    void updateBookAvailability(@PathVariable Long bookId, @RequestParam String status);
}
