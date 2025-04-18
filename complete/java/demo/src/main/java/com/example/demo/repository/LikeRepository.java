package com.example.demo.repository;

import com.example.demo.model.Like;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;
import java.util.List;

@Repository
public interface LikeRepository extends JpaRepository<Like, Long> {
    // 특정 포스트의 좋아요 목록 조회
    List<Like> findByPostId(Long postId);
    
    // 특정 사용자가 특정 포스트에 좋아요 했는지 확인
    Optional<Like> findByPostIdAndUserName(Long postId, String userName);
    
    // 특정 포스트의 좋아요 수 계산
    long countByPostId(Long postId);
}
