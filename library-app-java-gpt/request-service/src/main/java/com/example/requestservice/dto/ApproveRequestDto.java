package com.example.requestservice.dto;

import javax.validation.constraints.Size;

public class ApproveRequestDto {

    @Size(max = 2000)
    private String comments;

    public ApproveRequestDto() {}

    public String getComments() { return comments; }
    public void setComments(String comments) { this.comments = comments != null ? comments.trim() : null; }
}
