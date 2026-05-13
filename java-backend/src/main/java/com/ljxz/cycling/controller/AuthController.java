package com.ljxz.cycling.controller;

import com.ljxz.cycling.dto.LoginRequest;
import com.ljxz.cycling.dto.RefreshTokenRequest;
import com.ljxz.cycling.dto.RegisterRequest;
import com.ljxz.cycling.service.AuthService;
import com.ljxz.cycling.service.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * 认证控制器
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor

public class AuthController {
    
    private final AuthService authService;
    private final UserService userService;
    
    /**
     * 用户登录
     */
    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> login(@Valid @RequestBody LoginRequest request) {
        Map<String, Object> result = authService.login(request.getUsernameOrEmail(), request.getPassword());
        
        if ((Boolean) result.get("success")) {
            return ResponseEntity.ok(result);
        } else {
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 用户注册
     */
    @PostMapping("/register")
    public ResponseEntity<Map<String, Object>> register(@Valid @RequestBody RegisterRequest request) {
        // 验证密码确认
        if (!request.getPassword().equals(request.getConfirmPassword())) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "密码和确认密码不匹配");
            return ResponseEntity.badRequest().body(result);
        }
        
        // 构建全名
        String fullName = "";
        if (request.getFirstName() != null && request.getLastName() != null) {
            fullName = request.getFirstName() + " " + request.getLastName();
        } else if (request.getFirstName() != null) {
            fullName = request.getFirstName();
        } else if (request.getLastName() != null) {
            fullName = request.getLastName();
        }
        
        Map<String, Object> result = authService.register(
                request.getUsername(),
                request.getEmail(),
                request.getPassword(),
                fullName
        );
        
        if ((Boolean) result.get("success")) {
            return ResponseEntity.ok(result);
        } else {
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 刷新Token
     */
    @PostMapping("/refresh")
    public ResponseEntity<Map<String, Object>> refreshToken(@Valid @RequestBody RefreshTokenRequest request) {
        Map<String, Object> result = authService.refreshToken(request.getRefreshToken());
        
        if ((Boolean) result.get("success")) {
            return ResponseEntity.ok(result);
        } else {
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 用户登出
     */
    @PostMapping("/logout")
    public ResponseEntity<Map<String, Object>> logout() {
        // 由于使用JWT，登出主要在前端处理（删除token）
        // 这里可以添加token黑名单逻辑
        Map<String, Object> result = new HashMap<>();
        result.put("success", true);
        result.put("message", "登出成功");
        return ResponseEntity.ok(result);
    }
    
    /**
     * 检查用户名是否可用
     */
    @GetMapping("/check-username")
    public ResponseEntity<Map<String, Object>> checkUsername(@RequestParam String username) {
        boolean exists = userService.existsByUsername(username);
        Map<String, Object> result = new HashMap<>();
        result.put("available", !exists);
        result.put("message", exists ? "用户名已存在" : "用户名可用");
        return ResponseEntity.ok(result);
    }
    
    /**
     * 检查邮箱是否可用
     */
    @GetMapping("/check-email")
    public ResponseEntity<Map<String, Object>> checkEmail(@RequestParam String email) {
        boolean exists = userService.existsByEmail(email);
        Map<String, Object> result = new HashMap<>();
        result.put("available", !exists);
        result.put("message", exists ? "邮箱已存在" : "邮箱可用");
        return ResponseEntity.ok(result);
    }
}