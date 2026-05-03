# 灵境行者 - 安全指南

## 📋 目录

- [安全概览](#安全概览)
- [认证与授权](#认证与授权)
- [数据安全](#数据安全)
- [网络安全](#网络安全)
- [前端安全](#前端安全)
- [后端安全](#后端安全)
- [数据库安全](#数据库安全)
- [API 安全](#api-安全)
- [部署安全](#部署安全)
- [监控与审计](#监控与审计)
- [安全事件响应](#安全事件响应)
- [合规要求](#合规要求)

## 🛡️ 安全概览

### 安全架构

```
┌─────────────────────────────────────────────────────────┐
│                    前端安全层                            │
│  • XSS 防护        • CSRF 防护      • 内容安全策略      │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                    网络安全层                            │
│  • HTTPS 加密      • 防火墙配置      • DDoS 防护       │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                   应用安全层                             │
│  • JWT 认证        • 权限控制        • 输入验证         │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                   数据安全层                             │
│  • 数据加密        • 访问控制        • 备份加密         │
└─────────────────────────────────────────────────────────┘
```

### 安全等级

| 数据类型 | 安全等级 | 保护措施 |
|----------|----------|----------|
| 用户密码 | 高 | bcrypt 哈希 + 盐值 |
| 个人信息 | 高 | 数据库加密 + 访问控制 |
| 位置数据 | 中 | 传输加密 + 匿名化 |
| 设备信息 | 中 | 访问控制 + 日志记录 |
| 公开路线 | 低 | 基础验证 + 内容过滤 |

## 🔐 认证与授权

### JWT 认证机制

#### Token 结构

```javascript
// JWT Header
{
  "alg": "HS256",
  "typ": "JWT"
}

// JWT Payload
{
  "sub": "1234567890",
  "name": "用户名",
  "iat": 1516239022,
  "exp": 1516242622,
  "roles": ["USER"],
  "permissions": ["READ_ROUTES", "CREATE_ROUTES"]
}
```

#### 安全配置

```yaml
# Java 后端 JWT 配置
jwt:
  secret: ${JWT_SECRET:your-256-bit-secret-key-here}
  expiration: 3600  # 1小时
  refresh-expiration: 604800  # 7天
  issuer: ljxz-backend
  audience: ljxz-frontend
```

```python
# Python 后端 JWT 配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'your-secret-key')
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
JWT_ALGORITHM = 'HS256'
```

### 密码安全策略

#### 密码复杂度要求

```javascript
// 前端密码验证
const passwordRules = {
  minLength: 8,
  maxLength: 128,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecialChars: true,
  forbiddenPatterns: [
    /123456/,
    /password/i,
    /qwerty/i
  ]
}

function validatePassword(password) {
  const errors = []
  
  if (password.length < passwordRules.minLength) {
    errors.push(`密码长度至少${passwordRules.minLength}位`)
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('密码必须包含大写字母')
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('密码必须包含小写字母')
  }
  
  if (!/\d/.test(password)) {
    errors.push('密码必须包含数字')
  }
  
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push('密码必须包含特殊字符')
  }
  
  return errors
}
```

#### 密码哈希

```java
// Java 后端密码哈希
@Service
public class PasswordService {
    
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);
    
    public String hashPassword(String plainPassword) {
        return passwordEncoder.encode(plainPassword);
    }
    
    public boolean verifyPassword(String plainPassword, String hashedPassword) {
        return passwordEncoder.matches(plainPassword, hashedPassword);
    }
}
```

```python
# Python 后端密码哈希
from werkzeug.security import generate_password_hash, check_password_hash

class PasswordService:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return generate_password_hash(
            plain_password, 
            method='pbkdf2:sha256:100000'
        )
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, plain_password)
```

### 权限控制

#### 角色定义

```java
// 角色枚举
public enum Role {
    ADMIN("管理员", Arrays.asList(
        Permission.USER_MANAGE,
        Permission.ROUTE_MANAGE,
        Permission.SYSTEM_CONFIG
    )),
    MODERATOR("版主", Arrays.asList(
        Permission.ROUTE_MODERATE,
        Permission.CONTENT_MODERATE
    )),
    USER("普通用户", Arrays.asList(
        Permission.ROUTE_CREATE,
        Permission.ROUTE_READ,
        Permission.PROFILE_UPDATE
    )),
    GUEST("访客", Arrays.asList(
        Permission.ROUTE_READ
    ));
    
    private final String description;
    private final List<Permission> permissions;
}
```

#### 权限注解

```java
// 方法级权限控制
@RestController
@RequestMapping("/api/routes")
public class RouteController {
    
    @GetMapping
    @PreAuthorize("hasPermission('ROUTE_READ')")
    public ResponseEntity<List<Route>> getRoutes() {
        // 实现逻辑
    }
    
    @PostMapping
    @PreAuthorize("hasPermission('ROUTE_CREATE')")
    public ResponseEntity<Route> createRoute(@RequestBody Route route) {
        // 实现逻辑
    }
    
    @DeleteMapping("/{id}")
    @PreAuthorize("hasPermission('ROUTE_DELETE') or @routeService.isOwner(#id, authentication.name)")
    public ResponseEntity<Void> deleteRoute(@PathVariable Long id) {
        // 实现逻辑
    }
}
```

## 🔒 数据安全

### 敏感数据加密

#### 数据库字段加密

```java
// JPA 字段加密
@Entity
public class User {
    
    @Id
    private Long id;
    
    @Column(nullable = false)
    private String email;
    
    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "phone_encrypted")
    private String phone;
    
    @Convert(converter = EncryptedStringConverter.class)
    @Column(name = "id_card_encrypted")
    private String idCard;
}

@Converter
public class EncryptedStringConverter implements AttributeConverter<String, String> {
    
    @Autowired
    private EncryptionService encryptionService;
    
    @Override
    public String convertToDatabaseColumn(String attribute) {
        return encryptionService.encrypt(attribute);
    }
    
    @Override
    public String convertToEntityAttribute(String dbData) {
        return encryptionService.decrypt(dbData);
    }
}
```

#### 加密服务

```java
@Service
public class EncryptionService {
    
    private final AESUtil aesUtil;
    
    public EncryptionService(@Value("${app.encryption.key}") String encryptionKey) {
        this.aesUtil = new AESUtil(encryptionKey);
    }
    
    public String encrypt(String plainText) {
        if (plainText == null) return null;
        try {
            return aesUtil.encrypt(plainText);
        } catch (Exception e) {
            throw new EncryptionException("加密失败", e);
        }
    }
    
    public String decrypt(String encryptedText) {
        if (encryptedText == null) return null;
        try {
            return aesUtil.decrypt(encryptedText);
        } catch (Exception e) {
            throw new EncryptionException("解密失败", e);
        }
    }
}
```

### 数据脱敏

```java
// 数据脱敏工具
public class DataMaskingUtil {
    
    public static String maskEmail(String email) {
        if (email == null || !email.contains("@")) {
            return email;
        }
        String[] parts = email.split("@");
        String username = parts[0];
        String domain = parts[1];
        
        if (username.length() <= 2) {
            return "*" + username.substring(1) + "@" + domain;
        }
        
        return username.substring(0, 2) + "***" + username.substring(username.length() - 1) + "@" + domain;
    }
    
    public static String maskPhone(String phone) {
        if (phone == null || phone.length() < 7) {
            return phone;
        }
        return phone.substring(0, 3) + "****" + phone.substring(phone.length() - 4);
    }
    
    public static String maskIdCard(String idCard) {
        if (idCard == null || idCard.length() < 8) {
            return idCard;
        }
        return idCard.substring(0, 4) + "**********" + idCard.substring(idCard.length() - 4);
    }
}
```

## 🌐 网络安全

### HTTPS 配置

#### Nginx 配置

```nginx
server {
    listen 443 ssl http2;
    server_name ljxz.com www.ljxz.com;
    
    # SSL 证书配置
    ssl_certificate /etc/ssl/certs/ljxz.com.crt;
    ssl_certificate_key /etc/ssl/private/ljxz.com.key;
    
    # SSL 安全配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # 其他安全头
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    
    # CSP 配置
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://webapi.amap.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://restapi.amap.com;" always;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name ljxz.com www.ljxz.com;
    return 301 https://$server_name$request_uri;
}
```

### 防火墙配置

```bash
#!/bin/bash
# iptables 防火墙规则

# 清空现有规则
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# 设置默认策略
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 允许本地回环
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 允许已建立的连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 允许 SSH (限制来源IP)
iptables -A INPUT -p tcp --dport 22 -s 192.168.1.0/24 -j ACCEPT

# 允许 HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 允许应用端口（仅本地访问）
iptables -A INPUT -p tcp --dport 8080 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 3306 -s 127.0.0.1 -j ACCEPT

# 防止 DDoS 攻击
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

# 保存规则
iptables-save > /etc/iptables/rules.v4
```

## 🖥️ 前端安全

### XSS 防护

#### 输入验证和转义

```javascript
// XSS 防护工具
class XSSProtection {
  static sanitizeInput(input) {
    if (typeof input !== 'string') return input
    
    return input
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;')
  }
  
  static sanitizeHTML(html) {
    // 使用 DOMPurify 库
    return DOMPurify.sanitize(html, {
      ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'p', 'br'],
      ALLOWED_ATTR: []
    })
  }
  
  static validateURL(url) {
    try {
      const parsedURL = new URL(url)
      // 只允许 http 和 https 协议
      return ['http:', 'https:'].includes(parsedURL.protocol)
    } catch {
      return false
    }
  }
}

// 在组件中使用
export default {
  methods: {
    handleUserInput(input) {
      // 验证和清理用户输入
      const sanitizedInput = XSSProtection.sanitizeInput(input)
      
      // 进一步验证
      if (this.containsSuspiciousContent(sanitizedInput)) {
        this.$message.error('输入内容包含不安全字符')
        return
      }
      
      this.processInput(sanitizedInput)
    },
    
    containsSuspiciousContent(input) {
      const suspiciousPatterns = [
        /<script/i,
        /javascript:/i,
        /on\w+=/i,
        /eval\(/i,
        /expression\(/i
      ]
      
      return suspiciousPatterns.some(pattern => pattern.test(input))
    }
  }
}
```

### CSRF 防护

```javascript
// CSRF Token 管理
class CSRFProtection {
  static getToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content')
  }
  
  static setTokenHeader(config) {
    const token = this.getToken()
    if (token) {
      config.headers['X-CSRF-TOKEN'] = token
    }
    return config
  }
}

// Axios 拦截器
axios.interceptors.request.use(config => {
  // 为非 GET 请求添加 CSRF Token
  if (!['get', 'head', 'options'].includes(config.method.toLowerCase())) {
    CSRFProtection.setTokenHeader(config)
  }
  return config
})
```

### 内容安全策略 (CSP)

```html
<!-- 在 HTML 头部设置 CSP -->
<meta http-equiv="Content-Security-Policy" content="
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://webapi.amap.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://restapi.amap.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';
">
```

## ⚙️ 后端安全

### 输入验证

#### Java 后端验证

```java
// 输入验证注解
@RestController
@Validated
public class UserController {
    
    @PostMapping("/users")
    public ResponseEntity<User> createUser(
        @Valid @RequestBody CreateUserRequest request
    ) {
        // 实现逻辑
    }
}

// DTO 验证
public class CreateUserRequest {
    
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    @Size(max = 255, message = "邮箱长度不能超过255字符")
    private String email;
    
    @NotBlank(message = "密码不能为空")
    @Pattern(
        regexp = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$",
        message = "密码必须包含大小写字母、数字和特殊字符，长度至少8位"
    )
    private String password;
    
    @Pattern(
        regexp = "^[\\u4e00-\\u9fa5a-zA-Z0-9_-]{2,20}$",
        message = "昵称只能包含中文、英文、数字、下划线和连字符，长度2-20字符"
    )
    private String nickname;
    
    @Pattern(
        regexp = "^1[3-9]\\d{9}$",
        message = "手机号格式不正确"
    )
    private String phone;
}
```

#### 自定义验证器

```java
// 自定义坐标验证注解
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = CoordinateValidator.class)
public @interface ValidCoordinate {
    String message() default "坐标格式不正确";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

// 坐标验证器
public class CoordinateValidator implements ConstraintValidator<ValidCoordinate, BigDecimal> {
    
    @Override
    public boolean isValid(BigDecimal value, ConstraintValidatorContext context) {
        if (value == null) return true;
        
        // 纬度范围：-90 到 90
        // 经度范围：-180 到 180
        return value.compareTo(new BigDecimal("-180")) >= 0 && 
               value.compareTo(new BigDecimal("180")) <= 0;
    }
}
```

### SQL 注入防护

```java
// 使用 JPA 查询
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // 安全的参数化查询
    @Query("SELECT u FROM User u WHERE u.email = :email AND u.status = :status")
    Optional<User> findByEmailAndStatus(@Param("email") String email, @Param("status") Integer status);
    
    // 避免动态 SQL
    @Query(value = "SELECT * FROM users WHERE email = ? AND created_at > ?", nativeQuery = true)
    List<User> findByEmailAndCreatedAfter(String email, LocalDateTime createdAt);
}

// 动态查询使用 Criteria API
@Service
public class UserSearchService {
    
    public List<User> searchUsers(UserSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<User> query = cb.createQuery(User.class);
        Root<User> root = query.from(User.class);
        
        List<Predicate> predicates = new ArrayList<>();
        
        if (criteria.getEmail() != null) {
            predicates.add(cb.like(root.get("email"), "%" + criteria.getEmail() + "%"));
        }
        
        if (criteria.getStatus() != null) {
            predicates.add(cb.equal(root.get("status"), criteria.getStatus()));
        }
        
        query.where(predicates.toArray(new Predicate[0]));
        
        return entityManager.createQuery(query).getResultList();
    }
}
```

### 接口限流

```java
// 使用 Redis 实现限流
@Component
public class RateLimitService {
    
    @Autowired
    private RedisTemplate<String, String> redisTemplate;
    
    public boolean isAllowed(String key, int limit, int windowSeconds) {
        String redisKey = "rate_limit:" + key;
        
        try {
            String countStr = redisTemplate.opsForValue().get(redisKey);
            int count = countStr != null ? Integer.parseInt(countStr) : 0;
            
            if (count >= limit) {
                return false;
            }
            
            if (count == 0) {
                redisTemplate.opsForValue().set(redisKey, "1", Duration.ofSeconds(windowSeconds));
            } else {
                redisTemplate.opsForValue().increment(redisKey);
            }
            
            return true;
        } catch (Exception e) {
            // 限流服务异常时允许通过
            return true;
        }
    }
}

// 限流注解
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface RateLimit {
    int value() default 100;  // 每分钟请求次数
    int window() default 60;  // 时间窗口（秒）
    String key() default "";  // 限流键
}

// 限流切面
@Aspect
@Component
public class RateLimitAspect {
    
    @Autowired
    private RateLimitService rateLimitService;
    
    @Around("@annotation(rateLimit)")
    public Object around(ProceedingJoinPoint point, RateLimit rateLimit) throws Throwable {
        String key = generateKey(point, rateLimit);
        
        if (!rateLimitService.isAllowed(key, rateLimit.value(), rateLimit.window())) {
            throw new RateLimitExceededException("请求过于频繁，请稍后再试");
        }
        
        return point.proceed();
    }
    
    private String generateKey(ProceedingJoinPoint point, RateLimit rateLimit) {
        if (!rateLimit.key().isEmpty()) {
            return rateLimit.key();
        }
        
        // 使用 IP + 方法名作为默认键
        String ip = getClientIP();
        String method = point.getSignature().getName();
        return ip + ":" + method;
    }
}
```

## 🗄️ 数据库安全

### 连接安全

```yaml
# application-prod.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/ljxz?useSSL=true&requireSSL=true&verifyServerCertificate=true&useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000
```

### 数据库用户权限

```sql
-- 创建应用专用数据库用户
CREATE USER 'ljxz_app'@'localhost' IDENTIFIED BY 'strong_password_here';

-- 只授予必要的权限
GRANT SELECT, INSERT, UPDATE, DELETE ON ljxz.* TO 'ljxz_app'@'localhost';

-- 创建只读用户（用于报表查询）
CREATE USER 'ljxz_readonly'@'localhost' IDENTIFIED BY 'readonly_password';
GRANT SELECT ON ljxz.* TO 'ljxz_readonly'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;

-- 禁用不必要的功能
SET GLOBAL local_infile = 0;
SET GLOBAL general_log = 0;
```

### 审计日志

```sql
-- 启用审计日志
INSTALL PLUGIN audit_log SONAME 'audit_log.so';

-- 配置审计策略
SET GLOBAL audit_log_policy = 'ALL';
SET GLOBAL audit_log_format = 'JSON';
SET GLOBAL audit_log_file = '/var/log/mysql/audit.log';

-- 创建审计表
CREATE TABLE audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(100),
    record_id BIGINT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_user_id (user_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_created_at (created_at)
);
```

## 🔌 API 安全

### API 网关安全

```yaml
# Spring Cloud Gateway 配置
spring:
  cloud:
    gateway:
      routes:
        - id: java-backend
          uri: http://localhost:8080
          predicates:
            - Path=/api/**
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
                key-resolver: "#{@ipKeyResolver}"
            - name: CircuitBreaker
              args:
                name: backend-circuit-breaker
                fallbackUri: forward:/fallback
```

### API 版本控制

```java
// API 版本控制
@RestController
@RequestMapping("/api/v1/users")
public class UserV1Controller {
    // v1 实现
}

@RestController
@RequestMapping("/api/v2/users")
public class UserV2Controller {
    // v2 实现
}

// 版本废弃通知
@GetMapping("/deprecated-endpoint")
@Deprecated
public ResponseEntity<String> deprecatedEndpoint() {
    HttpHeaders headers = new HttpHeaders();
    headers.add("Deprecation", "true");
    headers.add("Sunset", "2025-12-31T23:59:59Z");
    headers.add("Link", "</api/v2/new-endpoint>; rel=\"successor-version\"");
    
    return ResponseEntity.ok()
        .headers(headers)
        .body("This endpoint is deprecated");
}
```

### API 文档安全

```java
// Swagger 安全配置
@Configuration
@EnableWebSecurity
public class SwaggerSecurityConfig {
    
    @Bean
    public SecurityFilterChain swaggerFilterChain(HttpSecurity http) throws Exception {
        return http
            .requestMatchers("/swagger-ui/**", "/v3/api-docs/**")
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/swagger-ui/**", "/v3/api-docs/**")
                .hasRole("ADMIN")
            )
            .httpBasic()
            .build();
    }
}

// 生产环境禁用 Swagger
@Profile("!prod")
@Configuration
public class SwaggerConfig {
    // Swagger 配置
}
```

## 🚀 部署安全

### 容器安全

```dockerfile
# 安全的 Dockerfile
FROM openjdk:17-jre-slim

# 创建非 root 用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 设置工作目录
WORKDIR /app

# 复制应用文件
COPY --chown=appuser:appuser target/ljxz-backend.jar app.jar

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# 启动应用
ENTRYPOINT ["java", "-jar", "-Djava.security.egd=file:/dev/./urandom", "app.jar"]
```

### 环境变量安全

```bash
# .env.example
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ljxz
DB_USERNAME=ljxz_user
DB_PASSWORD=your_secure_password_here

# JWT 配置
JWT_SECRET=your_256_bit_secret_key_here
JWT_EXPIRATION=3600

# 加密密钥
ENCRYPTION_KEY=your_encryption_key_here

# 高德地图 API
AMAP_WEB_KEY=your_amap_web_key
AMAP_WEB_SECRET=your_amap_web_secret
AMAP_SERVICE_KEY=your_amap_service_key

# Redis 配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# 邮件配置
MAIL_HOST=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=noreply@ljxz.com
MAIL_PASSWORD=your_mail_password
```

### 密钥管理

```bash
#!/bin/bash
# 密钥轮换脚本

KEY_DIR="/etc/ljxz/keys"
BACKUP_DIR="/etc/ljxz/keys/backup"

# 创建目录
mkdir -p $KEY_DIR $BACKUP_DIR

# 生成新的 JWT 密钥
generate_jwt_key() {
    openssl rand -base64 32 > $KEY_DIR/jwt_secret.new
    echo "New JWT key generated"
}

# 生成新的加密密钥
generate_encryption_key() {
    openssl rand -base64 32 > $KEY_DIR/encryption_key.new
    echo "New encryption key generated"
}

# 备份旧密钥
backup_keys() {
    if [ -f $KEY_DIR/jwt_secret ]; then
        cp $KEY_DIR/jwt_secret $BACKUP_DIR/jwt_secret.$(date +%Y%m%d_%H%M%S)
    fi
    
    if [ -f $KEY_DIR/encryption_key ]; then
        cp $KEY_DIR/encryption_key $BACKUP_DIR/encryption_key.$(date +%Y%m%d_%H%M%S)
    fi
}

# 应用新密钥
apply_new_keys() {
    mv $KEY_DIR/jwt_secret.new $KEY_DIR/jwt_secret
    mv $KEY_DIR/encryption_key.new $KEY_DIR/encryption_key
    
    # 重启应用服务
    systemctl restart ljxz-backend
    systemctl restart ljxz-python-backend
    
    echo "Keys rotated successfully"
}

# 执行密钥轮换
backup_keys
generate_jwt_key
generate_encryption_key
apply_new_keys
```

## 📊 监控与审计

### 安全监控

```java
// 安全事件监听器
@Component
public class SecurityEventListener {
    
    private static final Logger securityLogger = LoggerFactory.getLogger("SECURITY");
    
    @EventListener
    public void handleAuthenticationSuccess(AuthenticationSuccessEvent event) {
        String username = event.getAuthentication().getName();
        String ip = getClientIP();
        
        securityLogger.info("Login successful - User: {}, IP: {}", username, ip);
    }
    
    @EventListener
    public void handleAuthenticationFailure(AbstractAuthenticationFailureEvent event) {
        String username = event.getAuthentication().getName();
        String ip = getClientIP();
        String reason = event.getException().getMessage();
        
        securityLogger.warn("Login failed - User: {}, IP: {}, Reason: {}", username, ip, reason);
        
        // 检查是否需要锁定账户
        checkBruteForceAttack(username, ip);
    }
    
    @EventListener
    public void handleAccessDenied(AccessDeniedEvent event) {
        String username = event.getAuthentication().getName();
        String resource = event.getConfigAttribute().toString();
        
        securityLogger.warn("Access denied - User: {}, Resource: {}", username, resource);
    }
    
    private void checkBruteForceAttack(String username, String ip) {
        // 实现暴力破解检测逻辑
        // 如果检测到攻击，可以临时锁定账户或IP
    }
}
```

### 日志安全

```xml
<!-- logback-spring.xml -->
<configuration>
    <!-- 普通应用日志 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/application.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>
            <totalSizeCap>3GB</totalSizeCap>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <!-- 安全日志 -->
    <appender name="SECURITY_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/security.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/security.%d{yyyy-MM-dd}.log.gz</fileNamePattern>
            <maxHistory>90</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <!-- 安全日志记录器 -->
    <logger name="SECURITY" level="INFO" additivity="false">
        <appender-ref ref="SECURITY_FILE"/>
    </logger>
    
    <root level="INFO">
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

## 🚨 安全事件响应

### 事件分类

| 级别 | 事件类型 | 响应时间 | 处理流程 |
|------|----------|----------|----------|
| 严重 | 数据泄露、系统入侵 | 1小时内 | 立即隔离、通知管理层、启动应急预案 |
| 高 | 暴力破解、权限提升 | 4小时内 | 阻断攻击源、加强监控、分析日志 |
| 中 | 异常访问、可疑行为 | 24小时内 | 记录分析、调整安全策略 |
| 低 | 配置错误、轻微违规 | 72小时内 | 修复配置、更新文档 |

### 应急响应流程

```bash
#!/bin/bash
# 安全事件应急响应脚本

INCIDENT_TYPE=$1
SEVERITY=$2

case $SEVERITY in
    "CRITICAL")
        # 严重事件处理
        echo "CRITICAL incident detected: $INCIDENT_TYPE"
        
        # 立即隔离受影响系统
        systemctl stop ljxz-backend
        systemctl stop ljxz-python-backend
        
        # 备份当前日志
        tar -czf /backup/incident_logs_$(date +%Y%m%d_%H%M%S).tar.gz /var/log/ljxz/
        
        # 通知管理员
        echo "Critical security incident: $INCIDENT_TYPE" | mail -s "URGENT: Security Alert" admin@ljxz.com
        
        # 启动取证模式
        ./forensic_mode.sh
        ;;
        
    "HIGH")
        # 高级事件处理
        echo "HIGH severity incident: $INCIDENT_TYPE"
        
        # 增强监控
        ./enhance_monitoring.sh
        
        # 分析攻击模式
        ./analyze_attack_pattern.sh
        
        # 通知安全团队
        echo "High severity incident: $INCIDENT_TYPE" | mail -s "Security Alert" security@ljxz.com
        ;;
        
    *)
        echo "Standard incident handling for: $INCIDENT_TYPE"
        # 标准处理流程
        ;;
esac
```

## 📋 合规要求

### 数据保护合规

#### 个人信息保护

```java
// 个人信息处理记录
@Entity
public class PersonalDataProcessingRecord {
    
    @Id
    private Long id;
    
    private Long userId;
    private String dataType;  // 数据类型
    private String purpose;   // 处理目的
    private String legalBasis; // 法律依据
    private LocalDateTime processedAt;
    private String processor; // 处理者
    private String retention; // 保留期限
    
    // getters and setters
}

// 数据主体权利实现
@Service
public class DataSubjectRightsService {
    
    // 数据可携带权
    public byte[] exportUserData(Long userId) {
        // 导出用户所有数据
        UserDataExport export = new UserDataExport();
        export.setPersonalInfo(userService.getUserInfo(userId));
        export.setRoutes(routeService.getUserRoutes(userId));
        export.setRecords(recordService.getUserRecords(userId));
        
        return JsonUtils.toJsonBytes(export);
    }
    
    // 被遗忘权
    public void deleteUserData(Long userId) {
        // 软删除用户数据
        userService.markAsDeleted(userId);
        routeService.anonymizeUserRoutes(userId);
        recordService.anonymizeUserRecords(userId);
        
        // 记录删除操作
        auditService.recordDataDeletion(userId, "User requested data deletion");
    }
    
    // 数据更正权
    public void correctUserData(Long userId, DataCorrectionRequest request) {
        // 更正用户数据
        userService.updateUserInfo(userId, request.getCorrectedData());
        
        // 记录更正操作
        auditService.recordDataCorrection(userId, request);
    }
}
```

### 安全合规检查清单

#### 开发阶段

- [ ] 代码安全审查
- [ ] 依赖漏洞扫描
- [ ] 静态代码分析
- [ ] 安全测试用例
- [ ] 敏感信息检查

#### 部署阶段

- [ ] 服务器安全加固
- [ ] 网络安全配置
- [ ] 证书配置验证
- [ ] 访问控制测试
- [ ] 监控告警配置

#### 运维阶段

- [ ] 定期安全扫描
- [ ] 日志审计检查
- [ ] 备份恢复测试
- [ ] 应急响应演练
- [ ] 安全培训记录

---

## 📞 安全联系方式

- **安全团队邮箱**：security@ljxz.com
- **漏洞报告**：security-report@ljxz.com
- **紧急联系电话**：+86 138-0013-8000
- **安全事件热线**：+86 400-123-4567

---

*最后更新：2025年1月*
*下次审查：2025年7月*