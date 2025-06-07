package com.ljxz.cycling.service;

import com.ljxz.cycling.entity.User;
import com.ljxz.cycling.util.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

/**
 * 认证服务类
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final JwtUtil jwtUtil;
    
    /**
     * 用户登录
     * @param usernameOrEmail 用户名或邮箱
     * @param password 密码
     * @return 登录结果
     */
    public Map<String, Object> login(String usernameOrEmail, String password) {
        try {
            // 认证用户
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(usernameOrEmail, password)
            );
            
            UserDetails userDetails = (UserDetails) authentication.getPrincipal();
            User user = (User) userDetails;
            
            // 生成token
            String accessToken = jwtUtil.generateToken(userDetails);
            String refreshToken = jwtUtil.generateRefreshToken(userDetails);
            
            Map<String, Object> result = new HashMap<>();
            result.put("success", true);
            result.put("message", "登录成功");
            result.put("accessToken", accessToken);
            result.put("refreshToken", refreshToken);
            result.put("user", getUserInfo(user));
            
            return result;
            
        } catch (BadCredentialsException e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "用户名或密码错误");
            return result;
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "登录失败: " + e.getMessage());
            return result;
        }
    }
    
    /**
     * 用户注册
     * @param username 用户名
     * @param email 邮箱
     * @param password 密码
     * @param fullName 全名
     * @return 注册结果
     */
    public Map<String, Object> register(String username, String email, String password, String fullName) {
        try {
            // 创建用户对象
            User user = new User();
            user.setUsername(username);
            user.setEmail(email);
            user.setPasswordHash(password); // 在UserService中会进行加密
            user.setFullName(fullName);
            
            // 注册用户
            User savedUser = userService.registerUser(user);
            
            Map<String, Object> result = new HashMap<>();
            result.put("success", true);
            result.put("message", "注册成功");
            result.put("user", getUserInfo(savedUser));
            
            return result;
            
        } catch (RuntimeException e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", e.getMessage());
            return result;
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "注册失败: " + e.getMessage());
            return result;
        }
    }
    
    /**
     * 刷新token
     * @param refreshToken 刷新token
     * @return 新的token
     */
    public Map<String, Object> refreshToken(String refreshToken) {
        try {
            if (!jwtUtil.validateTokenFormat(refreshToken)) {
                Map<String, Object> result = new HashMap<>();
                result.put("success", false);
                result.put("message", "无效的刷新token");
                return result;
            }
            
            String username = jwtUtil.getUsernameFromToken(refreshToken);
            User user = userService.findByUsernameOrEmail(username)
                    .orElseThrow(() -> new RuntimeException("用户不存在"));
            
            String newAccessToken = jwtUtil.generateToken(user);
            String newRefreshToken = jwtUtil.generateRefreshToken(user);
            
            Map<String, Object> result = new HashMap<>();
            result.put("success", true);
            result.put("message", "Token刷新成功");
            result.put("accessToken", newAccessToken);
            result.put("refreshToken", newRefreshToken);
            
            return result;
            
        } catch (Exception e) {
            Map<String, Object> result = new HashMap<>();
            result.put("success", false);
            result.put("message", "Token刷新失败: " + e.getMessage());
            return result;
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
        return userInfo;
    }
}