// filepath: /workspaces/github-copilot-bootcamp-2025-main/java/demo/src/main/java/com/example/demo/controller/LikeController.java
package com.example.demo.controller;

import com.example.demo.dto.LikeBaseDto;
import com.example.demo.model.Like;
import com.example.demo.service.LikeService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/posts/{postId}/likes")
@Tag(name = "좋아요 관리", description = "포스트 좋아요 추가 및 취소 API")
public class LikeController {

    private final LikeService likeService;

    @Autowired
    public LikeController(LikeService likeService) {
        this.likeService = likeService;
    }

    // 특정 포스트에 좋아요 추가
    @Operation(summary = "좋아요 추가", description = "특정 포스트에 좋아요를 추가합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "201", description = "좋아요 추가 성공"),
        @ApiResponse(responseCode = "400", description = "잘못된 요청")
    })
    @PostMapping
    public ResponseEntity<Like> addLike(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "좋아요 정보", required = true) @RequestBody LikeBaseDto likeBaseDto) {
        Like like = likeService.addLike(postId, likeBaseDto);
        return ResponseEntity.status(HttpStatus.CREATED).body(like);
    }

    // 특정 포스트의 좋아요 취소
    @Operation(summary = "좋아요 취소", description = "특정 포스트의 좋아요를 취소합니다.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "좋아요 취소 성공"),
        @ApiResponse(responseCode = "404", description = "좋아요를 찾을 수 없음")
    })
    @DeleteMapping
    public ResponseEntity<Void> removeLike(
        @Parameter(description = "포스트 ID", required = true) @PathVariable Long postId, 
        @Parameter(description = "사용자 이름", required = true) @RequestParam String userName) {
        if (likeService.hasLiked(postId, userName)) {
            likeService.removeLike(postId, userName);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
