package com.ljxz.cycling.config;

import com.ljxz.cycling.service.UserDetailsServiceImpl;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.web.cors.CorsConfigurationSource;

import java.util.List;
import java.util.Arrays;

/**
 * Spring Security配置类
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Configuration
@EnableWebSecurity
@EnableConfigurationProperties(SecurityConfig.SecurityProperties.class)
@RequiredArgsConstructor
public class SecurityConfig {
    
    private final UserDetailsServiceImpl userDetailsService;
    private final JwtAuthenticationFilter jwtAuthenticationFilter;
    private final SecurityProperties securityProperties;
    private final CorsConfigurationSource corsConfigurationSource;
    
    @ConfigurationProperties(prefix = "security")
    public static class SecurityProperties {
        private List<String> permitAll = Arrays.asList(
            "/auth/**",
            "/public/**",
            "/health",
            "/route/health",
            "/api/route/health",
            "/test",
            "/api/test",
            "/tables",
            "/api/tables",
            "/cycling-routes/**",
            "/api/cycling-routes/**",
            "/feedback/**",
            "/api/feedback/**",
            "/actuator/**",
            "/swagger-ui/**",
            "/v3/api-docs/**"
        );
        
        public List<String> getPermitAll() {
            return permitAll;
        }
        
        public void setPermitAll(List<String> permitAll) {
            this.permitAll = permitAll;
        }
    }
    
    /**
     * 密码编码器
     */
    @Bean
    public BCryptPasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    /**
     * 认证提供者
     */
    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }
    
    /**
     * 认证管理器
     */
    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
    
    /**
     * 安全过滤器链
     */
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // 禁用CSRF
            .csrf(AbstractHttpConfigurer::disable)
            
            // 配置CORS - 使用WebConfig中定义的corsConfigurationSource
            .cors(cors -> cors.configurationSource(corsConfigurationSource))
            
            // 配置授权规则
            .authorizeHttpRequests(authz -> {
                // 允许访问的路径
                String[] permitAllArray = securityProperties.getPermitAll().toArray(new String[0]);
                authz.requestMatchers(permitAllArray).permitAll();
                
                // 其他请求需要认证
                authz.anyRequest().authenticated();
            })
            
            // 配置会话管理
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            
            // 配置认证提供者
            .authenticationProvider(authenticationProvider())
            
            // 添加JWT过滤器
            .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
}