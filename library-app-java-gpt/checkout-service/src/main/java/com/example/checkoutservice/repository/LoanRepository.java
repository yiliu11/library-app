package com.example.checkoutservice.repository;

import com.example.checkoutservice.entity.Loan;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public interface LoanRepository extends JpaRepository<Loan, UUID> {
    List<Loan> findByUserIdOrderByCheckoutDateDesc(UUID userId);
    Optional<Loan> findByIdAndUserId(UUID id, UUID userId);
}
