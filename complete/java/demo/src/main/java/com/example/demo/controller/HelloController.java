package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;

@RestController
@Tag(name = "Hello API", description = "인사말을 제공하는 API")
public class HelloController {

    @GetMapping("/hello")
    @Operation(
        summary = "인사말 메시지 반환",
        description = "이름을 입력받아 맞춤형 인사말을 반환합니다"
    )
    @ApiResponse(responseCode = "200", description = "성공적으로 인사말 반환")
    public String hello(
        @Parameter(description = "인사할 대상의 이름", example = "World") 
        @RequestParam(value = "name", defaultValue = "World") String name) {
        
        return String.format("Hello, %s!", name);
    }

    
}
