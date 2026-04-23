package com.ljxz.cycling.controller;

import com.ljxz.cycling.entity.RouteRequest;
import com.ljxz.cycling.entity.RouteResponse;
import com.ljxz.cycling.service.RouteService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import jakarta.validation.constraints.DecimalMax;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * 路径规划控制器
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Slf4j
@RestController
@RequestMapping("/")
@Validated
public class RouteController {

    @Autowired
    private RouteService routeService;

    /**
     * 路径规划接口
     * 
     * @param request 路径规划请求
     * @return 路径规划响应
     */
    @PostMapping("/route/plan")
    public ResponseEntity<RouteResponse> planRoute(@Valid @RequestBody RouteRequest request) {
        log.info("收到路径规划请求: origin={}, destination={}, transportMode={}", 
                request.getOrigin(), request.getDestination(), request.getTransportMode());
        
        RouteResponse response = routeService.planRoute(request);
        
        if (response.getStatus() == 1) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }

    /**
     * 快速路径规划接口（简化参数）
     * 
     * @param origin 起点
     * @param destination 终点
     * @param transportMode 交通方式
     * @param city 城市（可选）
     * @return 路径规划响应
     */
    @GetMapping("/route/quick-plan")
    public ResponseEntity<RouteResponse> quickPlanRoute(
            @RequestParam @NotBlank(message = "起点不能为空") @Size(max = 200) String origin,
            @RequestParam @NotBlank(message = "终点不能为空") @Size(max = 200) String destination,
            @RequestParam @NotBlank(message = "交通方式不能为空") String transportMode,
            @RequestParam(required = false) String city) {
        
        log.info("收到快速路径规划请求: origin={}, destination={}, transportMode={}, city={}", 
                origin, destination, transportMode, city);
        
        RouteRequest request = RouteRequest.builder()
                .origin(origin)
                .destination(destination)
                .transportMode(transportMode)
                .city(city)
                .strategy(0)
                .showSteps(true)
                .build();
        
        RouteResponse response = routeService.planRoute(request);
        
        if (response.getStatus() == 1) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }

    /**
     * 地理编码接口 - 地址转坐标
     * 
     * @param address 地址
     * @param city 城市（可选）
     * @return 坐标响应
     */
    @GetMapping("/route/geocode")
    public ResponseEntity<RouteResponse> geocode(
            @RequestParam @NotBlank(message = "地址不能为空") @Size(max = 200) String address,
            @RequestParam(required = false) String city) {
        
        log.info("收到地理编码请求: address={}, city={}", address, city);
        
        RouteResponse response = routeService.geocode(address, city);
        
        if (response.getStatus() == 1) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }

    /**
     * 逆地理编码接口 - 坐标转地址
     * 
     * @param longitude 经度
     * @param latitude 纬度
     * @return 地址响应
     */
    @GetMapping("/route/reverse-geocode")
    public ResponseEntity<RouteResponse> reverseGeocode(
            @RequestParam @DecimalMin(value = "-180.0", message = "经度必须在-180到180之间") 
                         @DecimalMax(value = "180.0", message = "经度必须在-180到180之间") Double longitude,
            @RequestParam @DecimalMin(value = "-90.0", message = "纬度必须在-90到90之间") 
                         @DecimalMax(value = "90.0", message = "纬度必须在-90到90之间") Double latitude) {
        
        log.info("收到逆地理编码请求: longitude={}, latitude={}", longitude, latitude);
        
        RouteResponse response = routeService.reverseGeocode(longitude, latitude);
        
        if (response.getStatus() == 1) {
            return ResponseEntity.ok(response);
        } else {
            return ResponseEntity.badRequest().body(response);
        }
    }

    /**
     * 获取支持的交通方式
     * 
     * @return 交通方式列表
     */
    @GetMapping("/route/transport-modes")
    public ResponseEntity<?> getTransportModes() {
        return ResponseEntity.ok(new Object() {
            public final String[] transportModes = {"driving", "walking", "transit", "riding"};
            public final Object[] descriptions = {
                new Object() {
                    public final String mode = "driving";
                    public final String name = "驾车";
                    public final String description = "适用于汽车出行，提供最优驾车路线";
                    
                    // 重写toString方法以使用字段
                    @Override
                    public String toString() {
                        return mode + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final String mode = "walking";
                    public final String name = "步行";
                    public final String description = "适用于步行出行，提供步行路线";
                    
                    @Override
                    public String toString() {
                        return mode + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final String mode = "transit";
                    public final String name = "公交";
                    public final String description = "适用于公共交通出行，包括公交、地铁等";
                    
                    @Override
                    public String toString() {
                        return mode + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final String mode = "riding";
                    public final String name = "骑行";
                    public final String description = "适用于自行车出行，提供骑行路线";
                    
                    @Override
                    public String toString() {
                        return mode + ": " + name + " - " + description;
                    }
                }
            };
            
            // 使用字段的方法
            @Override
            public String toString() {
                StringBuilder sb = new StringBuilder();
                for (Object desc : descriptions) {
                    sb.append(desc.toString()).append("\n");
                }
                return sb.toString();
            }
        });
    }

    /**
     * 获取路径规划策略说明
     * 
     * @return 策略说明
     */
    @GetMapping("/route/strategies")
    public ResponseEntity<?> getStrategies() {
        return ResponseEntity.ok(new Object() {
            public final Object[] strategies = {
                new Object() {
                    public final Integer code = 0;
                    public final String name = "速度优先";
                    public final String description = "时间最短路线";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final Integer code = 1;
                    public final String name = "费用优先";
                    public final String description = "费用最少路线";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final Integer code = 2;
                    public final String name = "距离优先";
                    public final String description = "距离最短路线";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final Integer code = 3;
                    public final String name = "不走快速路";
                    public final String description = "避开快速路的路线";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final Integer code = 4;
                    public final String name = "躲避拥堵";
                    public final String description = "避开拥堵路段";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                },
                new Object() {
                    public final Integer code = 5;
                    public final String name = "多策略";
                    public final String description = "综合速度、费用、距离的路线";
                    
                    @Override
                    public String toString() {
                        return code + ": " + name + " - " + description;
                    }
                }
            };
            
            // 使用字段的方法
            @Override
            public String toString() {
                StringBuilder sb = new StringBuilder();
                for (Object strategy : strategies) {
                    sb.append(strategy.toString()).append("\n");
                }
                return sb.toString();
            }
        });
    }

    /**
     * 健康检查接口
     * 
     * @return 服务状态
     */
    @GetMapping({"/health", "/route/health"})
    public ResponseEntity<?> health() {
        return ResponseEntity.ok(new Object() {
            public final String status = "UP";
            public final String message = "服务运行正常";
            public final String service = "灵境行者路径规划服务";
            public final String version = "1.0.0";
            public final long timestamp = System.currentTimeMillis();
        });
    }

    /**
     * 测试接口
     * 
     * @return 测试响应
     */
    @GetMapping("/test")
    public ResponseEntity<?> test() {
        return ResponseEntity.ok(new Object() {
            public final String status = "success";
            public final String message = "测试接口正常";
            public final String service = "灵境行者路径规划服务";
            public final long timestamp = System.currentTimeMillis();
        });
    }

    /**
     * 获取数据库表列表
     * 
     * @return 数据库表列表
     */
    @GetMapping("/tables")
    public ResponseEntity<?> getTables() {
        log.info("获取数据库表列表");
        
        return ResponseEntity.ok(new Object() {
            public final boolean success = true;
            public final String[] tables = {
                "cycling_routes", "users", "route_history", "equipment", 
                "weather_data", "poi_data", "route_points"
            };
            public final String message = "获取数据库表列表成功";
            public final long timestamp = System.currentTimeMillis();
        });
    }

    /**
     * 提交用户反馈
     * 
     * @param feedbackData 反馈数据
     * @return 反馈提交结果
     */
    @PostMapping("/feedback")
    public ResponseEntity<?> submitFeedback(@RequestBody java.util.Map<String, Object> feedbackData) {
        log.info("收到用户反馈: {}", feedbackData);
        
        try {
            // 这里可以添加反馈数据的处理逻辑，比如保存到数据库
            java.util.Map<String, Object> response = new java.util.HashMap<>();
            response.put("success", true);
            response.put("message", "反馈提交成功");
            response.put("timestamp", System.currentTimeMillis());
            response.put("feedbackId", java.util.UUID.randomUUID().toString());
            
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("处理反馈时发生错误", e);
            java.util.Map<String, Object> errorResponse = new java.util.HashMap<>();
            errorResponse.put("success", false);
            errorResponse.put("message", "反馈提交失败: " + e.getMessage());
            errorResponse.put("timestamp", System.currentTimeMillis());
            
            return ResponseEntity.status(500).body(errorResponse);
        }
    }

    /**
     * 获取骑行路线列表
     * 
     * @param limit 限制返回数量
     * @return 骑行路线列表
     */
    @GetMapping("/cycling-routes")
    public ResponseEntity<?> getCyclingRoutes(
            @RequestParam(name = "limit", defaultValue = "10") @jakarta.validation.constraints.Min(value = 1, message = "限制数量必须大于0") 
            @jakarta.validation.constraints.Max(value = 100, message = "限制数量不能超过100") int limit) {
        
        log.info("获取骑行路线列表，限制数量: {}", limit);
        
        // 模拟骑行路线数据
        java.util.List<Object> routes = new java.util.ArrayList<>();
        
        for (int i = 1; i <= Math.min(limit, 10); i++) {
            final int routeId = i; // 声明为final以在匿名内部类中使用
            routes.add(new Object() {
                public final int id = routeId;
                public final String name = "骑行路线 " + routeId;
                public final String distance = (routeId * 5.2) + " km";
                public final String duration = (routeId * 25) + " 分钟";
                public final String difficulty = routeId % 3 == 0 ? "困难" : routeId % 2 == 0 ? "中等" : "简单";
                public final String startPoint = "起点 " + routeId;
                public final String endPoint = "终点 " + routeId;
                public final String description = "这是一条优美的骑行路线，适合" + (routeId % 3 == 0 ? "经验丰富" : "初学者") + "的骑行爱好者。";
                public final long createdAt = System.currentTimeMillis();
            });
        }
        
        return ResponseEntity.ok(new Object() {
            public final boolean success = true;
            public final java.util.List<Object> data = routes;
            public final int total = routes.size();
            public final String message = "获取骑行路线列表成功";
        });
    }

    /**
     * 获取API使用说明
     * 
     * @return API文档
     */
    @GetMapping("/docs")
    public ResponseEntity<?> getDocs() {
        return ResponseEntity.ok(new Object() {
            public final String title = "灵境行者路径规划API";
            public final String version = "1.0.0";
            public final String description = "提供路径规划、地理编码等服务";
            public final Object[] endpoints = {
                new Object() {
                    public final String method = "POST";
                    public final String path = "/api/route/plan";
                    public final String description = "路径规划（完整参数）";
                },
                new Object() {
                    public final String method = "GET";
                    public final String path = "/api/route/quick-plan";
                    public final String description = "快速路径规划（简化参数）";
                },
                new Object() {
                    public final String method = "GET";
                    public final String path = "/api/route/geocode";
                    public final String description = "地理编码（地址转坐标）";
                },
                new Object() {
                    public final String method = "GET";
                    public final String path = "/api/route/reverse-geocode";
                    public final String description = "逆地理编码（坐标转地址）";
                },
                new Object() {
                    public final String method = "GET";
                    public final String path = "/api/route/transport-modes";
                    public final String description = "获取支持的交通方式";
                },
                new Object() {
                    public final String method = "GET";
                    public final String path = "/api/route/strategies";
                    public final String description = "获取路径规划策略";
                }
            };
        });
    }
}