package com.ljxz.cycling.controller;

import com.ljxz.cycling.entity.User;
import com.ljxz.cycling.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * 用户控制器
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@RestController
@RequestMapping("/user")
@RequiredArgsConstructor

public class UserController {
    
    private final UserService userService;
    
    /**
     * 获取当前用户信息
     */
    @GetMapping("/profile")
    public ResponseEntity<Map<String, Object>> getProfile() {
        try {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            String username = authentication.getName();
            
            Optional<User> userOpt = userService.findByUsernameOrEmail(username);
            if (userOpt.isPresent()) {
                User user = userOpt.get();
                Map<String, Object> result = new HashMap<>();
                result.put("success", true);
                result.put("user", getUserInfo(user));
                return ResponseEntity.ok(result);
            } else {
                Map<String, Object> result = new HashMap<>();
                result.put("success", false);
                result.put("message", "用户不存在");
                return ResponseEntity.badRequest().body(result);
            }
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "获取用户信息失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 更新用户信息
     */
    @PutMapping("/profile")
    public ResponseEntity<Map<String, Object>> updateProfile(@RequestBody Map<String, Object> updateData) {
        try {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            String username = authentication.getName();
            
            Optional<User> userOpt = userService.findByUsernameOrEmail(username);
            if (userOpt.isPresent()) {
                User user = userOpt.get();
                
                // 更新允许修改的字段
                if (updateData.containsKey("fullName")) {
                    user.setFullName((String) updateData.get("fullName"));
                }
                if (updateData.containsKey("phone")) {
                    user.setPhone((String) updateData.get("phone"));
                }
                if (updateData.containsKey("avatarUrl")) {
                    user.setAvatarUrl((String) updateData.get("avatarUrl"));
                }
                
                User updatedUser = userService.updateUser(user);
                
                Map<String, Object> result = new HashMap<>();
                result.put("success", true);
                result.put("message", "用户信息更新成功");
                result.put("user", getUserInfo(updatedUser));
                return ResponseEntity.ok(result);
            } else {
                Map<String, Object> result = new HashMap<>();
                result.put("success", false);
                result.put("message", "用户不存在");
                return ResponseEntity.badRequest().body(result);
            }
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "更新用户信息失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 获取用户记录（骑行记录等）
     */
    @GetMapping("/records")
    public ResponseEntity<Map<String, Object>> getUserRecords() {
        try {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            String username = authentication.getName();
            
            // 这里可以添加获取用户骑行记录的逻辑
            // 目前返回空数组作为占位符
            Map<String, Object> result = new HashMap<>();
            result.put("success", true);
            result.put("records", new Object[]{});
            result.put("message", "获取用户记录成功");
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "获取用户记录失败: " + e.getMessage());
            return ResponseEntity.badRequest().body(result);
        }
    }
    
    /**
     * 获取用户信息（不包含敏感信息）
     */
    private Map<String, Object> getUserInfo(User user) {
        Map<String, Object> userInfo = new HashMap<>();
        userInfo.put("id", user.getId());
        userInfo.put("username", user.getUsername());
        userInfo.put("email", user.getEmail());
        userInfo.put("fullName", user.getFullName());
        userInfo.put("phone", user.getPhone());
        userInfo.put("avatarUrl", user.getAvatarUrl());
        userInfo.put("createdAt", user.getCreatedAt());
        userInfo.put("updatedAt", user.getUpdatedAt());
        return userInfo;
    }
}