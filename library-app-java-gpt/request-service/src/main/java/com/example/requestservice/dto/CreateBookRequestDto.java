package com.example.requestservice.dto;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;

public class CreateBookRequestDto {

    @NotBlank(message = "Title is required")
    @Size(max = 500)
    private String title;

    @Size(max = 300)
    private String author;

    @Size(max = 2000)
    private String reason;

    public CreateBookRequestDto() {}

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title != null ? title.trim() : null; }

    public String getAuthor() { return author; }
    public void setAuthor(String author) { this.author = author != null ? author.trim() : null; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason != null ? reason.trim() : null; }
}
