package com.example.demo.service;

import com.example.demo.dto.LikeBaseDto;
import com.example.demo.model.Like;
import com.example.demo.repository.LikeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.Optional;

@Service
public class LikeService {

    private final LikeRepository likeRepository;
    private final PostService postService;

    @Autowired
    public LikeService(LikeRepository likeRepository, PostService postService) {
        this.likeRepository = likeRepository;
        this.postService = postService;
    }

    // 좋아요 추가
    @Transactional
    public Like addLike(Long postId, LikeBaseDto likeBaseDto) {
        Optional<Like> existingLike = likeRepository.findByPostIdAndUserName(postId, likeBaseDto.getUserName());
        
        if (existingLike.isPresent()) {
            // 이미 좋아요를 누른 경우
            return existingLike.get();
        }
        
        Like like = Like.builder()
                .postId(postId)
                .userName(likeBaseDto.getUserName())
                .build();
        
        Like savedLike = likeRepository.save(like);
        
        // 포스트의 좋아요 수 증가
        postService.updateLikeCount(postId, 1);
        
        return savedLike;
    }

    // 좋아요 취소
    @Transactional
    public void removeLike(Long postId, String userName) {
        Optional<Like> existingLike = likeRepository.findByPostIdAndUserName(postId, userName);
        
        existingLike.ifPresent(like -> {
            likeRepository.delete(like);
            
            // 포스트의 좋아요 수 감소
            postService.updateLikeCount(postId, -1);
        });
    }

    // 특정 사용자가 특정 포스트에 좋아요 했는지 확인
    public boolean hasLiked(Long postId, String userName) {
        return likeRepository.findByPostIdAndUserName(postId, userName).isPresent();
    }

    // 특정 포스트의 좋아요 수 계산
    public long countLikesByPostId(Long postId) {
        return likeRepository.countByPostId(postId);
    }
}
