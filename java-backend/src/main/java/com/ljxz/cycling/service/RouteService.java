package com.ljxz.cycling.service;

import com.ljxz.cycling.entity.RouteRequest;
import com.ljxz.cycling.entity.RouteResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.time.LocalDateTime;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.TimeUnit;

/**
 * 路径规划服务
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Slf4j
@Service
public class RouteService {

    @Autowired
    private AmapService amapService;

    @Value("${route.default-city:石家庄}")
    private String defaultCity;

    @Value("${route.cache-expire-minutes:30}")
    private int cacheExpireMinutes;

    // 简单的内存缓存，生产环境建议使用Redis
    private final ConcurrentHashMap<String, CacheEntry> routeCache = new ConcurrentHashMap<>();

    /**
     * 路径规划主方法
     * 
     * @param request 路径规划请求
     * @return 路径规划响应
     */
    public RouteResponse planRoute(RouteRequest request) {
        long startTime = System.currentTimeMillis();
        
        try {
            // 参数验证和预处理
            validateAndPreprocessRequest(request);
            
            // 检查缓存
            String cacheKey = generateCacheKey(request);
            CacheEntry cachedResult = getFromCache(cacheKey);
            if (cachedResult != null) {
                log.info("从缓存获取路径规划结果: {}", cacheKey);
                long processingTime = System.currentTimeMillis() - startTime;
                return RouteResponse.success(cachedResult.getRouteResult(), processingTime);
            }
            
            // 调用高德API进行路径规划
            RouteResponse.RouteResult routeResult = amapService.planRoute(request);
            
            if (routeResult == null) {
                long processingTime = System.currentTimeMillis() - startTime;
                return RouteResponse.failure("路径规划失败，请检查起终点地址是否正确", processingTime);
            }
            
            // 补充坐标信息
            enrichRouteResult(routeResult, request);
            
            // 缓存结果
            putToCache(cacheKey, routeResult);
            
            long processingTime = System.currentTimeMillis() - startTime;
            log.info("路径规划成功: 距离={}米, 时长={}秒, 耗时={}ms", 
                    routeResult.getDistance(), routeResult.getDuration(), processingTime);
            
            return RouteResponse.success(routeResult, processingTime);
            
        } catch (IllegalArgumentException e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.warn("路径规划参数错误: {}", e.getMessage());
            return RouteResponse.failure(e.getMessage(), processingTime);
            
        } catch (Exception e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.error("路径规划异常: {}", e.getMessage(), e);
            return RouteResponse.failure("系统异常，请稍后重试", processingTime);
        }
    }

    /**
     * 地理编码 - 地址转坐标
     * 
     * @param address 地址
     * @param city 城市
     * @return 坐标响应
     */
    public RouteResponse geocode(String address, String city) {
        long startTime = System.currentTimeMillis();
        
        try {
            if (!StringUtils.hasText(address)) {
                throw new IllegalArgumentException("地址不能为空");
            }
            
            String cityParam = StringUtils.hasText(city) ? city : defaultCity;
            String coordinate = amapService.geocode(address, cityParam);
            
            if (coordinate == null) {
                long processingTime = System.currentTimeMillis() - startTime;
                return RouteResponse.failure("地址解析失败，请检查地址是否正确", processingTime);
            }
            
            // 解析坐标
            String[] coords = coordinate.split(",");
            if (coords.length != 2) {
                long processingTime = System.currentTimeMillis() - startTime;
                return RouteResponse.failure("坐标格式错误", processingTime);
            }
            
            RouteResponse.Coordinate coord = RouteResponse.Coordinate.builder()
                    .longitude(Double.parseDouble(coords[0]))
                    .latitude(Double.parseDouble(coords[1]))
                    .address(address)
                    .build();
            
            RouteResponse.RouteResult result = RouteResponse.RouteResult.builder()
                    .origin(coord)
                    .build();
            
            long processingTime = System.currentTimeMillis() - startTime;
            return RouteResponse.success(result, processingTime);
            
        } catch (Exception e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.error("地理编码异常: address={}, city={}, error={}", address, city, e.getMessage());
            return RouteResponse.failure("地理编码失败: " + e.getMessage(), processingTime);
        }
    }

    /**
     * 逆地理编码 - 坐标转地址
     * 
     * @param longitude 经度
     * @param latitude 纬度
     * @return 地址响应
     */
    public RouteResponse reverseGeocode(double longitude, double latitude) {
        long startTime = System.currentTimeMillis();
        
        try {
            validateCoordinate(longitude, latitude);
            
            String address = amapService.reverseGeocode(longitude, latitude);
            
            if (address == null) {
                long processingTime = System.currentTimeMillis() - startTime;
                return RouteResponse.failure("坐标解析失败，请检查坐标是否正确", processingTime);
            }
            
            RouteResponse.Coordinate coord = RouteResponse.Coordinate.builder()
                    .longitude(longitude)
                    .latitude(latitude)
                    .address(address)
                    .build();
            
            RouteResponse.RouteResult result = RouteResponse.RouteResult.builder()
                    .origin(coord)
                    .build();
            
            long processingTime = System.currentTimeMillis() - startTime;
            return RouteResponse.success(result, processingTime);
            
        } catch (Exception e) {
            long processingTime = System.currentTimeMillis() - startTime;
            log.error("逆地理编码异常: lng={}, lat={}, error={}", longitude, latitude, e.getMessage());
            return RouteResponse.failure("逆地理编码失败: " + e.getMessage(), processingTime);
        }
    }

    /**
     * 验证和预处理请求参数
     */
    private void validateAndPreprocessRequest(RouteRequest request) {
        if (!StringUtils.hasText(request.getOrigin())) {
            throw new IllegalArgumentException("起点不能为空");
        }
        
        if (!StringUtils.hasText(request.getDestination())) {
            throw new IllegalArgumentException("终点不能为空");
        }
        
        if (!StringUtils.hasText(request.getTransportMode())) {
            throw new IllegalArgumentException("交通方式不能为空");
        }
        
        // 设置默认城市
        if (!StringUtils.hasText(request.getCity())) {
            request.setCity(defaultCity);
        }
        
        // 设置默认策略
        if (request.getStrategy() == null) {
            request.setStrategy(0);
        }
        
        // 设置时间戳
        if (request.getTimestamp() == null) {
            request.setTimestamp(System.currentTimeMillis());
        }
    }

    /**
     * 验证坐标有效性
     */
    private void validateCoordinate(double longitude, double latitude) {
        if (longitude < -180 || longitude > 180) {
            throw new IllegalArgumentException("经度必须在-180到180之间");
        }
        
        if (latitude < -90 || latitude > 90) {
            throw new IllegalArgumentException("纬度必须在-90到90之间");
        }
    }

    /**
     * 补充路径结果信息
     */
    private void enrichRouteResult(RouteResponse.RouteResult routeResult, RouteRequest request) {
        try {
            // 解析起点坐标
            String originCoord = getCoordinateString(request.getOrigin(), request.getCity());
            if (originCoord != null) {
                String[] coords = originCoord.split(",");
                if (coords.length == 2) {
                    RouteResponse.Coordinate origin = RouteResponse.Coordinate.builder()
                            .longitude(Double.parseDouble(coords[0]))
                            .latitude(Double.parseDouble(coords[1]))
                            .address(request.getOrigin())
                            .build();
                    routeResult.setOrigin(origin);
                }
            }
            
            // 解析终点坐标
            String destCoord = getCoordinateString(request.getDestination(), request.getCity());
            if (destCoord != null) {
                String[] coords = destCoord.split(",");
                if (coords.length == 2) {
                    RouteResponse.Coordinate destination = RouteResponse.Coordinate.builder()
                            .longitude(Double.parseDouble(coords[0]))
                            .latitude(Double.parseDouble(coords[1]))
                            .address(request.getDestination())
                            .build();
                    routeResult.setDestination(destination);
                }
            }
            
        } catch (Exception e) {
            log.warn("补充路径结果信息失败: {}", e.getMessage());
        }
    }

    /**
     * 获取坐标字符串
     */
    private String getCoordinateString(String location, String city) {
        if (RouteRequest.isValidCoordinate(location)) {
            return location;
        }
        return amapService.geocode(location, city);
    }

    /**
     * 生成缓存键
     */
    private String generateCacheKey(RouteRequest request) {
        StringBuilder key = new StringBuilder();
        key.append(request.getOrigin()).append("|");
        key.append(request.getDestination()).append("|");
        key.append(request.getTransportMode()).append("|");
        key.append(request.getStrategy()).append("|");
        if (request.getFormattedWaypoints() != null) {
            key.append(request.getFormattedWaypoints()).append("|");
        }
        key.append(request.getCity());
        return key.toString();
    }

    /**
     * 从缓存获取结果
     */
    private CacheEntry getFromCache(String key) {
        CacheEntry entry = routeCache.get(key);
        if (entry != null && !entry.isExpired()) {
            return entry;
        }
        if (entry != null) {
            routeCache.remove(key); // 移除过期缓存
        }
        return null;
    }

    /**
     * 将结果放入缓存
     */
    private void putToCache(String key, RouteResponse.RouteResult result) {
        long expireTime = System.currentTimeMillis() + TimeUnit.MINUTES.toMillis(cacheExpireMinutes);
        routeCache.put(key, new CacheEntry(result, expireTime));
    }

    /**
     * 缓存条目
     */
    private static class CacheEntry {
        private final RouteResponse.RouteResult routeResult;
        private final long expireTime;

        public CacheEntry(RouteResponse.RouteResult routeResult, long expireTime) {
            this.routeResult = routeResult;
            this.expireTime = expireTime;
        }

        public RouteResponse.RouteResult getRouteResult() {
            return routeResult;
        }

        public boolean isExpired() {
            return System.currentTimeMillis() > expireTime;
        }
    }

    /**
     * 清理过期缓存（可以通过定时任务调用）
     */
    public void cleanExpiredCache() {
        routeCache.entrySet().removeIf(entry -> entry.getValue().isExpired());
        log.info("清理过期缓存完成，当前缓存大小: {}", routeCache.size());
    }
}