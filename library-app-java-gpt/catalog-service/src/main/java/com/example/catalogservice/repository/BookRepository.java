package com.example.catalogservice.repository;

import com.example.catalogservice.entity.Book;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.repository.*;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface BookRepository extends JpaRepository<Book, UUID> {

    @Query("SELECT b FROM Book b WHERE " +
            "(:title IS NULL OR LOWER(b.title) LIKE LOWER(CONCAT('%', :title, '%'))) AND " +
            "(:author IS NULL OR LOWER(b.author) LIKE LOWER(CONCAT('%', :author, '%'))) AND " +
            "(:keyword IS NULL OR (LOWER(b.title) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(b.author) LIKE LOWER(CONCAT('%', :keyword, '%')) OR LOWER(b.genre) LIKE LOWER(CONCAT('%', :keyword, '%'))))")
    Page<Book> search(@Param("title") String title,
                      @Param("author") String author,
                      @Param("keyword") String keyword,
                      Pageable pageable);
}
