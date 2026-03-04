package com.library.requestservice.repository;

import com.library.requestservice.model.BookRequest;
import com.library.requestservice.model.RequestStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface BookRequestRepository extends JpaRepository<BookRequest, Long> {
    List<BookRequest> findByRequesterId(Long requesterId);
    List<BookRequest> findByStatus(RequestStatus status);
    Optional<BookRequest> findByIdAndStatus(Long id, RequestStatus status);
}
