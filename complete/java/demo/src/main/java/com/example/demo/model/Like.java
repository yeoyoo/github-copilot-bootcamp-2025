package com.example.demo.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Entity
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "likes", uniqueConstraints = {
    @UniqueConstraint(columnNames = {"postId", "userName"})
})
public class Like {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long postId;
    private String userName;
    
    // 한 사용자가 같은 포스트에 한 번만 좋아요 가능
}
