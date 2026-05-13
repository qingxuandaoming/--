package com.ljxz.cycling.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * 登录请求DTO
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Data
public class LoginRequest {
    
    @NotBlank(message = "用户名或邮箱不能为空")
    private String usernameOrEmail;
    
    @NotBlank(message = "密码不能为空")
    private String password;
    
    private Boolean remember = false;
}