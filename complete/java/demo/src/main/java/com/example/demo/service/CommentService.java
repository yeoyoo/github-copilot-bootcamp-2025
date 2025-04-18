package com.example.demo.service;

import com.example.demo.dto.CommentCreateDto;
import com.example.demo.dto.CommentUpdateDto;
import com.example.demo.model.Comment;
import com.example.demo.repository.CommentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class CommentService {

    private final CommentRepository commentRepository;
    private final PostService postService;

    @Autowired
    public CommentService(CommentRepository commentRepository, PostService postService) {
        this.commentRepository = commentRepository;
        this.postService = postService;
    }

    // 특정 포스트의 모든 댓글 조회
    public List<Comment> getCommentsByPostId(Long postId) {
        return commentRepository.findByPostId(postId);
    }

    // 특정 댓글 조회
    public Optional<Comment> getCommentById(Long commentId) {
        return commentRepository.findById(commentId);
    }

    // 새 댓글 생성
    @Transactional
    public Comment createComment(Long postId, CommentCreateDto commentCreateDto) {
        Comment comment = Comment.builder()
                .postId(postId)
                .userName(commentCreateDto.getUserName())
                .content(commentCreateDto.getContent())
                .build();
        
        Comment savedComment = commentRepository.save(comment);
        
        // 포스트의 댓글 수 증가
        postService.updateCommentCount(postId, 1);
        
        return savedComment;
    }

    // 댓글 업데이트
    @Transactional
    public Optional<Comment> updateComment(Long commentId, CommentUpdateDto commentUpdateDto) {
        return commentRepository.findById(commentId)
                .map(comment -> {
                    comment.setContent(commentUpdateDto.getContent());
                    return commentRepository.save(comment);
                });
    }

    // 댓글 삭제
    @Transactional
    public void deleteComment(Long commentId) {
        commentRepository.findById(commentId).ifPresent(comment -> {
            Long postId = comment.getPostId();
            commentRepository.deleteById(commentId);
            
            // 포스트의 댓글 수 감소
            postService.updateCommentCount(postId, -1);
        });
    }
}
