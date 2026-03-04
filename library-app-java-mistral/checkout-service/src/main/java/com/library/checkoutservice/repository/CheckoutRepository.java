package com.library.checkoutservice.repository;

import com.library.checkoutservice.model.CheckoutRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface CheckoutRepository extends JpaRepository<CheckoutRecord, Long> {
    List<CheckoutRecord> findByUserId(Long userId);
    Optional<CheckoutRecord> findByUserIdAndBookIdAndStatus(Long userId, Long bookId, CheckoutRecord.CheckoutStatus status);
    List<CheckoutRecord> findByStatus(CheckoutRecord.CheckoutStatus status);
    List<CheckoutRecord> findByUserIdAndStatus(Long userId, CheckoutRecord.CheckoutStatus status);
}
