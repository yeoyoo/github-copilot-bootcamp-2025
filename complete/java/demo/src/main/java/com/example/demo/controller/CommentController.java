// filepath: /workspaces/github-copilot-bootcamp-2025-main/java/demo/src/main/java/com/example/demo/controller/CommentController.java
package com.example.demo.controller;

import com.example.demo.dto.CommentCreateDto;
import com.example.demo.dto.CommentUpdateDto;
import com.example.demo.model.Comment;
import com.example.demo.service.CommentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/posts/{postId}/comments")
@Tag(name = "댓글 관리", description = "댓글 조회, 생성, 수정, 삭제 API")
public class CommentController {

    private final CommentService commentService;

    @Autowired
    public CommentController(CommentService commentService) {
        this.commentService = commentService;
    }

    @Operation(summary = "포스트 댓글 목록 조회", description = "특정 포스트에 작성된 모든 댓글을 조회합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "댓글 목록 조회 성공")
    })
    @GetMapping
    public ResponseEntity<List<Comment>> getCommentsByPostId(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId) {
        List<Comment> comments = commentService.getCommentsByPostId(postId);
        return ResponseEntity.ok(comments);
    }

    @Operation(summary = "댓글 작성", description = "특정 포스트에 새 댓글을 작성합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "댓글 작성 성공")
    })
    @PostMapping
    public ResponseEntity<Comment> createComment(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "댓글 작성 정보", required = true) @RequestBody CommentCreateDto commentCreateDto) {
        Comment createdComment = commentService.createComment(postId, commentCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdComment);
    }

    @Operation(summary = "댓글 상세 조회", description = "특정 댓글의 상세 정보를 조회합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "댓글 조회 성공"),
        @ApiResponse(responseCode = "404", description = "댓글을 찾을 수 없음")
    })
    @GetMapping("/{commentId}")
    public ResponseEntity<Comment> getCommentById(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "댓글 ID", required = true) @PathVariable Long commentId) {
        Optional<Comment> commentOptional = commentService.getCommentById(commentId);
        
        if (!commentOptional.isPresent()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        Comment comment = commentOptional.get();
        if (!comment.getPostId().equals(postId)) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        return ResponseEntity.ok(comment);
    }

    @Operation(summary = "댓글 수정", description = "특정 댓글의 내용을 수정합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "댓글 수정 성공"),
        @ApiResponse(responseCode = "404", description = "댓글을 찾을 수 없음")
    })
    @PatchMapping("/{commentId}")
    public ResponseEntity<Comment> updateComment(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "댓글 ID", required = true) @PathVariable Long commentId, 
        @Parameter(description = "댓글 수정 정보", required = true) @RequestBody CommentUpdateDto commentUpdateDto) {
        Optional<Comment> commentOptional = commentService.getCommentById(commentId);
        
        if (!commentOptional.isPresent()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        Comment comment = commentOptional.get();
        if (!comment.getPostId().equals(postId)) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        Optional<Comment> updatedCommentOptional = commentService.updateComment(commentId, commentUpdateDto);
        if (!updatedCommentOptional.isPresent()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        return ResponseEntity.ok(updatedCommentOptional.get());
    }

    @Operation(summary = "댓글 삭제", description = "특정 댓글을 삭제합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "댓글 삭제 성공"),
        @ApiResponse(responseCode = "404", description = "댓글을 찾을 수 없음")
    })
    @DeleteMapping("/{commentId}")
    public ResponseEntity<Void> deleteComment(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "댓글 ID", required = true) @PathVariable Long commentId) {
        Optional<Comment> commentOptional = commentService.getCommentById(commentId);
        
        if (!commentOptional.isPresent()) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        Comment comment = commentOptional.get();
        if (!comment.getPostId().equals(postId)) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        
        commentService.deleteComment(commentId);
        return ResponseEntity.noContent().build();
    }
}
