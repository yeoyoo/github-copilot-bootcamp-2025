package com.example.demo.controller;

import com.example.demo.dto.PostCreateDto;
import com.example.demo.dto.PostUpdateDto;
import com.example.demo.model.Post;
import com.example.demo.service.PostService;
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

@RestController
@RequestMapping("/api/posts")
@Tag(name = "게시물 관리", description = "게시물 조회, 생성, 수정, 삭제 API")
public class PostController {

    private final PostService postService;

    @Autowired
    public PostController(PostService postService) {
        this.postService = postService;
    }

    // 모든 포스트 목록 조회
    @GetMapping
    @Operation(summary = "모든 게시물 조회", description = "모든 게시물 목록을 조회합니다.")
    @ApiResponse(responseCode = "200", description = "성공적으로 게시물 목록 반환")
    public ResponseEntity<List<Post>> getAllPosts() {
        List<Post> posts = postService.getAllPosts();
        return ResponseEntity.ok(posts);
    }

    // 새 포스트 작성
    @PostMapping
    public ResponseEntity<Post> createPost(@RequestBody PostCreateDto postCreateDto) {
        Post createdPost = postService.createPost(postCreateDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(createdPost);
    }

    // 특정 포스트 조회
    @GetMapping("/{postId}")
    public ResponseEntity<Post> getPostById(@PathVariable Long postId) {
        return postService.getPostById(postId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // 특정 포스트 수정
    @PatchMapping("/{postId}")
    public ResponseEntity<Post> updatePost(@PathVariable Long postId, @RequestBody PostUpdateDto postUpdateDto) {
        return postService.updatePost(postId, postUpdateDto)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // 특정 포스트 삭제
    @DeleteMapping("/{postId}")
    public ResponseEntity<Void> deletePost(@PathVariable Long postId) {
        if (postService.getPostById(postId).isPresent()) {
            postService.deletePost(postId);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
