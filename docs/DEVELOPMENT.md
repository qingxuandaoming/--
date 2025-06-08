# 灵境行者 - 开发指南

## 📋 目录

- [开发环境搭建](#开发环境搭建)
- [代码规范](#代码规范)
- [分支管理](#分支管理)
- [提交规范](#提交规范)
- [测试策略](#测试策略)
- [开发流程](#开发流程)
- [调试指南](#调试指南)
- [性能优化](#性能优化)
- [常见问题](#常见问题)

## 🛠️ 开发环境搭建

### 系统要求

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| Node.js | >= 16.0.0 | 前端开发环境 |
| Java | >= 17 | Java 后端开发 |
| Python | >= 3.8 | Python 爬虫服务 |
| MySQL | >= 8.0 | 数据库服务 |
| Git | >= 2.20 | 版本控制 |

### IDE 推荐配置

#### VS Code 扩展

```json
{
  "recommendations": [
    "vetur.vetur",
    "ms-python.python",
    "redhat.java",
    "ms-vscode.vscode-json",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-eslint"
  ]
}
```

#### IntelliJ IDEA 插件

- Vue.js
- Python
- Database Tools and SQL
- GitToolBox

### 环境变量配置

#### 前端环境变量

```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8080
VITE_PYTHON_API_URL=http://localhost:5000
VITE_AMAP_KEY=cc888f3fbd2b5c82cb3b842d8277c241
VITE_AMAP_SECURITY_KEY=045a4882fc3282b9bf01d689b11a06d7
```

#### Python 后端环境变量

```bash
# .env
DATABASE_URL=mysql://root:123456@localhost:3306/ljxz
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

#### Java 后端配置

```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/ljxz
    username: root
    password: 123456
  jpa:
    show-sql: true
    hibernate:
      ddl-auto: update
```

## 📝 代码规范

### 前端代码规范 (Vue 3)

#### 组件命名

```javascript
// ✅ 正确：PascalCase
const UserProfile = defineComponent({
  name: 'UserProfile'
})

// ❌ 错误：camelCase
const userProfile = defineComponent({
  name: 'userProfile'
})
```

#### 变量命名

```javascript
// ✅ 正确：camelCase
const userName = ref('')
const isLoading = ref(false)

// ❌ 错误：snake_case
const user_name = ref('')
const is_loading = ref(false)
```

#### 文件结构

```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
// 1. 导入
import { ref, computed, onMounted } from 'vue'

// 2. Props 定义
const props = defineProps({
  // props 定义
})

// 3. 响应式数据
const data = ref(null)

// 4. 计算属性
const computedValue = computed(() => {
  // 计算逻辑
})

// 5. 方法
const handleClick = () => {
  // 方法实现
}

// 6. 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
/* 样式 */
</style>
```

### Java 后端代码规范

#### 包结构

```
com.ljxz.cycling
├── controller/     # 控制器层
├── service/        # 服务层
├── repository/     # 数据访问层
├── model/          # 实体模型
├── dto/            # 数据传输对象
├── config/         # 配置类
├── exception/      # 异常处理
└── util/           # 工具类
```

#### 命名规范

```java
// ✅ 正确：类名 PascalCase
public class UserController {
    
    // ✅ 正确：方法名 camelCase
    public ResponseEntity<User> getUserById(Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
    
    // ✅ 正确：常量 UPPER_SNAKE_CASE
    private static final String DEFAULT_PAGE_SIZE = "10";
}
```

#### 注释规范

```java
/**
 * 用户控制器
 * 处理用户相关的 HTTP 请求
 * 
 * @author 开发者姓名
 * @version 1.0
 * @since 2025-01-01
 */
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    /**
     * 根据 ID 获取用户信息
     * 
     * @param id 用户 ID
     * @return 用户信息
     * @throws UserNotFoundException 用户不存在时抛出
     */
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        // 实现逻辑
    }
}
```

### Python 后端代码规范

#### 命名规范

```python
# ✅ 正确：snake_case
class EquipmentService:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
    
    def get_equipment_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """根据 ID 获取设备信息"""
        return self.repository.find_by_id(equipment_id)

# ✅ 正确：常量 UPPER_SNAKE_CASE
DEFAULT_PAGE_SIZE = 20
MAX_RETRY_COUNT = 3
```

#### 类型注解

```python
from typing import List, Optional, Dict, Any

def process_equipment_data(
    equipment_list: List[Dict[str, Any]],
    filter_criteria: Optional[Dict[str, str]] = None
) -> List[Equipment]:
    """处理设备数据
    
    Args:
        equipment_list: 设备数据列表
        filter_criteria: 过滤条件
        
    Returns:
        处理后的设备对象列表
        
    Raises:
        ValueError: 数据格式错误时抛出
    """
    # 实现逻辑
```

## 🌿 分支管理

### 分支策略

```
main                 # 主分支，生产环境代码
├── develop          # 开发分支，集成最新功能
├── feature/*        # 功能分支
├── hotfix/*         # 热修复分支
└── release/*        # 发布分支
```

### 分支命名规范

| 分支类型 | 命名格式 | 示例 |
|----------|----------|------|
| 功能开发 | `feature/功能描述` | `feature/user-authentication` |
| Bug 修复 | `bugfix/问题描述` | `bugfix/login-error` |
| 热修复 | `hotfix/问题描述` | `hotfix/security-patch` |
| 发布 | `release/版本号` | `release/v1.2.0` |

### 分支操作流程

```bash
# 1. 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# 2. 开发完成后推送
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature

# 3. 创建 Pull Request
# 在 GitHub/GitLab 上创建 PR，目标分支为 develop

# 4. 代码审查通过后合并
git checkout develop
git pull origin develop
git branch -d feature/new-feature
```

## 📋 提交规范

### Commit Message 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): 添加用户登录功能` |
| `fix` | Bug 修复 | `fix(api): 修复用户数据获取错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装指南` |
| `style` | 代码格式 | `style(css): 调整按钮样式` |
| `refactor` | 代码重构 | `refactor(service): 优化数据处理逻辑` |
| `test` | 测试相关 | `test(unit): 添加用户服务单元测试` |
| `chore` | 构建/工具 | `chore(deps): 更新依赖版本` |

### 提交示例

```bash
# ✅ 正确示例
git commit -m "feat(map): 添加路线规划功能

- 集成高德地图 API
- 实现起点终点选择
- 添加路线优化算法

Closes #123"

# ❌ 错误示例
git commit -m "修改了一些代码"
git commit -m "bug fix"
```

## 🧪 测试策略

### 测试金字塔

```
    E2E Tests (10%)
   ┌─────────────────┐
  │  Integration    │ (20%)
 │     Tests        │
└───────────────────┘
│   Unit Tests     │ (70%)
└─────────────────────┘
```

### 前端测试

#### 单元测试 (Vitest)

```javascript
// tests/components/UserProfile.test.js
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import UserProfile from '@/components/UserProfile.vue'

describe('UserProfile', () => {
  it('renders user name correctly', () => {
    const wrapper = mount(UserProfile, {
      props: {
        user: { name: 'John Doe', email: 'john@example.com' }
      }
    })
    
    expect(wrapper.text()).toContain('John Doe')
  })
})
```

#### E2E 测试 (Cypress)

```javascript
// cypress/e2e/user-flow.cy.js
describe('User Authentication Flow', () => {
  it('should login successfully', () => {
    cy.visit('/login')
    cy.get('[data-cy=username]').type('testuser')
    cy.get('[data-cy=password]').type('password123')
    cy.get('[data-cy=login-btn]').click()
    
    cy.url().should('include', '/dashboard')
    cy.get('[data-cy=welcome-message]').should('be.visible')
  })
})
```

### Java 后端测试

#### 单元测试 (JUnit 5)

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("根据 ID 获取用户 - 成功")
    void getUserById_Success() {
        // Given
        Long userId = 1L;
        User expectedUser = new User(userId, "John Doe");
        when(userRepository.findById(userId)).thenReturn(Optional.of(expectedUser));
        
        // When
        User actualUser = userService.getUserById(userId);
        
        // Then
        assertThat(actualUser).isEqualTo(expectedUser);
        verify(userRepository).findById(userId);
    }
}
```

#### 集成测试

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.properties")
class UserControllerIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    void getUserById_ShouldReturnUser() {
        // Given
        Long userId = 1L;
        
        // When
        ResponseEntity<User> response = restTemplate.getForEntity(
            "/api/users/" + userId, User.class);
        
        // Then
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(response.getBody().getId()).isEqualTo(userId);
    }
}
```

### Python 后端测试

#### 单元测试 (pytest)

```python
# tests/test_equipment_service.py
import pytest
from unittest.mock import Mock, patch
from services.equipment_service import EquipmentService

class TestEquipmentService:
    
    @pytest.fixture
    def equipment_service(self):
        return EquipmentService()
    
    @patch('services.equipment_service.requests.get')
    def test_fetch_equipment_data_success(self, mock_get, equipment_service):
        # Given
        mock_response = Mock()
        mock_response.json.return_value = {'data': [{'id': 1, 'name': 'Test Equipment'}]}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # When
        result = equipment_service.fetch_equipment_data()
        
        # Then
        assert len(result) == 1
        assert result[0]['name'] == 'Test Equipment'
```

## 🔄 开发流程

### 功能开发流程

```mermaid
graph TD
    A[需求分析] --> B[技术设计]
    B --> C[创建功能分支]
    C --> D[编写代码]
    D --> E[单元测试]
    E --> F[集成测试]
    F --> G[代码审查]
    G --> H{审查通过?}
    H -->|否| D
    H -->|是| I[合并到 develop]
    I --> J[部署到测试环境]
    J --> K[功能测试]
    K --> L{测试通过?}
    L -->|否| D
    L -->|是| M[发布到生产环境]
```

### 代码审查清单

#### 通用检查项

- [ ] 代码符合项目规范
- [ ] 变量和函数命名清晰
- [ ] 注释充分且准确
- [ ] 没有硬编码的配置
- [ ] 错误处理完善
- [ ] 性能考虑合理
- [ ] 安全性检查通过

#### 前端特定检查项

- [ ] 组件职责单一
- [ ] Props 类型定义正确
- [ ] 响应式数据使用合理
- [ ] 样式作用域正确
- [ ] 无内存泄漏风险

#### 后端特定检查项

- [ ] API 设计符合 RESTful 规范
- [ ] 数据验证完整
- [ ] 事务处理正确
- [ ] 日志记录充分
- [ ] 异常处理完善

## 🐛 调试指南

### 前端调试

#### Vue DevTools

```javascript
// 在组件中添加调试信息
export default {
  name: 'MyComponent',
  setup() {
    const debugInfo = computed(() => ({
      props: props,
      state: state.value,
      computed: computedValue.value
    }))
    
    // 开发环境下暴露调试信息
    if (process.env.NODE_ENV === 'development') {
      window.debugComponent = debugInfo
    }
    
    return { debugInfo }
  }
}
```

#### 网络请求调试

```javascript
// utils/api.js
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL
})

// 请求拦截器
api.interceptors.request.use(config => {
  console.log('🚀 Request:', config)
  return config
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    console.log('✅ Response:', response)
    return response
  },
  error => {
    console.error('❌ Error:', error)
    return Promise.reject(error)
  }
)
```

### Java 后端调试

#### 日志配置

```yaml
# application-dev.yml
logging:
  level:
    com.ljxz.cycling: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG
    org.hibernate.type.descriptor.sql.BasicBinder: TRACE
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
```

#### 调试注解

```java
@RestController
@Slf4j
public class UserController {
    
    @GetMapping("/users/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        log.debug("Getting user with id: {}", id);
        
        try {
            User user = userService.findById(id);
            log.debug("Found user: {}", user);
            return ResponseEntity.ok(user);
        } catch (UserNotFoundException e) {
            log.warn("User not found with id: {}", id);
            return ResponseEntity.notFound().build();
        }
    }
}
```

### Python 后端调试

#### 日志配置

```python
# config/logging.py
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler(
            'logs/cycling-route.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Cycling Route startup')
```

#### 调试装饰器

```python
import functools
import time
from flask import current_app

def debug_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        current_app.logger.debug(
            f"{func.__name__} executed in {end_time - start_time:.4f} seconds"
        )
        return result
    return wrapper

@debug_time
def fetch_equipment_data():
    # 实现逻辑
    pass
```

## ⚡ 性能优化

### 前端性能优化

#### 代码分割

```javascript
// router/index.js
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue')
  },
  {
    path: '/profile',
    component: () => import('@/views/Profile.vue')
  }
]
```

#### 组件懒加载

```vue
<template>
  <div>
    <Suspense>
      <template #default>
        <AsyncComponent />
      </template>
      <template #fallback>
        <div>Loading...</div>
      </template>
    </Suspense>
  </div>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() =>
  import('@/components/HeavyComponent.vue')
)
</script>
```

#### 图片优化

```vue
<template>
  <img 
    :src="optimizedImageSrc" 
    :alt="imageAlt"
    loading="lazy"
    @load="onImageLoad"
    @error="onImageError"
  />
</template>

<script setup>
const optimizedImageSrc = computed(() => {
  const { src, width, height } = props
  return `${src}?w=${width}&h=${height}&q=80&f=webp`
})
</script>
```

### 后端性能优化

#### 数据库查询优化

```java
// 使用 JPA 查询优化
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    @Query("SELECT u FROM User u LEFT JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);
    
    @Query(value = "SELECT * FROM users WHERE status = :status LIMIT :limit", 
           nativeQuery = true)
    List<User> findActiveUsersWithLimit(@Param("status") String status, 
                                       @Param("limit") int limit);
}
```

#### 缓存策略

```java
@Service
@CacheConfig(cacheNames = "users")
public class UserService {
    
    @Cacheable(key = "#id")
    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
    
    @CacheEvict(key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
}
```

## ❓ 常见问题

### 环境问题

#### Q: 前端启动失败，提示端口被占用

```bash
# 查找占用端口的进程
netstat -ano | findstr :5174

# 终止进程
taskkill /PID <进程ID> /F

# 或者使用不同端口启动
npm run dev -- --port 5175
```

#### Q: Java 后端连接数据库失败

```yaml
# 检查 application.yml 配置
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/ljxz?useSSL=false&serverTimezone=UTC
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver
```

#### Q: Python 后端依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 如果仍然失败，尝试创建新的虚拟环境
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 开发问题

#### Q: Git 提交被拒绝

```bash
# 检查提交信息格式
git log --oneline -5

# 修改最后一次提交信息
git commit --amend -m "feat(auth): 添加用户登录功能"

# 强制推送（谨慎使用）
git push --force-with-lease origin feature-branch
```

#### Q: 代码格式检查失败

```bash
# 前端代码格式化
npm run lint:fix
npm run format

# Java 代码格式化（使用 IDE）
# IntelliJ IDEA: Ctrl+Alt+L
# VS Code: Shift+Alt+F

# Python 代码格式化
black .
flake8 .
```

### 部署问题

#### Q: 生产环境构建失败

```bash
# 清理缓存
npm run clean
rm -rf node_modules package-lock.json
npm install

# 检查环境变量
echo $NODE_ENV
echo $VITE_API_BASE_URL

# 重新构建
npm run build
```

#### Q: 数据库迁移失败

```sql
-- 检查数据库连接
SHOW DATABASES;
USE ljxz;
SHOW TABLES;

-- 检查表结构
DESCRIBE users;
DESCRIBE equipment;

-- 手动执行迁移脚本
SOURCE database/init.sql;
```

---

## 📞 技术支持

如果遇到本文档未涵盖的问题，请通过以下方式获取帮助：

1. **查看项目 Wiki**：详细的技术文档和 FAQ
2. **提交 Issue**：在项目仓库中创建问题报告
3. **联系开发团队**：通过项目群组或邮件联系
4. **代码审查**：请求资深开发者进行代码审查

---

*最后更新：2025年1月*