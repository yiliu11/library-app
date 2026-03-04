package com.example.requestservice.repository;

import com.example.requestservice.entity.BookRequestEntity;
import com.example.requestservice.entity.RequestStatus;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface BookRequestRepository extends JpaRepository<BookRequestEntity, UUID> {

    Page<BookRequestEntity> findByStatus(RequestStatus status, Pageable pageable);

    Page<BookRequestEntity> findByRequestedBy(UUID requestedBy, Pageable pageable);

    Optional<BookRequestEntity> findByIdAndRequestedBy(UUID id, UUID requestedBy);
}
