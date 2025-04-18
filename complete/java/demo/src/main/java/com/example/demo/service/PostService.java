package com.example.demo.service;

import com.example.demo.dto.PostCreateDto;
import com.example.demo.dto.PostUpdateDto;
import com.example.demo.model.Post;
import com.example.demo.repository.PostRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class PostService {

    private final PostRepository postRepository;

    @Autowired
    public PostService(PostRepository postRepository) {
        this.postRepository = postRepository;
    }

    // 모든 포스트 조회
    public List<Post> getAllPosts() {
        return postRepository.findAll();
    }

    // 특정 포스트 조회
    public Optional<Post> getPostById(Long postId) {
        return postRepository.findById(postId);
    }

    // 새 포스트 생성
    @Transactional
    public Post createPost(PostCreateDto postCreateDto) {
        Post post = Post.builder()
                .userName(postCreateDto.getUserName())
                .content(postCreateDto.getContent())
                .likeCount(0)
                .commentCount(0)
                .build();
        
        return postRepository.save(post);
    }

    // 포스트 업데이트
    @Transactional
    public Optional<Post> updatePost(Long postId, PostUpdateDto postUpdateDto) {
        return postRepository.findById(postId)
                .map(post -> {
                    post.setContent(postUpdateDto.getContent());
                    return postRepository.save(post);
                });
    }

    // 포스트 삭제
    @Transactional
    public void deletePost(Long postId) {
        postRepository.deleteById(postId);
    }

    // 좋아요 수 업데이트
    @Transactional
    public void updateLikeCount(Long postId, int change) {
        postRepository.findById(postId).ifPresent(post -> {
            post.setLikeCount(post.getLikeCount() + change);
            postRepository.save(post);
        });
    }

    // 댓글 수 업데이트
    @Transactional
    public void updateCommentCount(Long postId, int change) {
        postRepository.findById(postId).ifPresent(post -> {
            post.setCommentCount(post.getCommentCount() + change);
            postRepository.save(post);
        });
    }
}
