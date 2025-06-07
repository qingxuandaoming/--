package com.ljxz.cycling.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * 刷新Token请求DTO
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Data
public class RefreshTokenRequest {
    
    @NotBlank(message = "刷新Token不能为空")
    private String refreshToken;
}