package com.ljxz.cycling.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ljxz.cycling.entity.RouteRequest;
import com.ljxz.cycling.entity.RouteResponse;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.HttpEntity;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

/**
 * 高德地图API服务
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Slf4j
@Service
public class AmapService {

    @Value("${amap.web-api-key}")
    private String webApiKey;

    @Value("${amap.base-url}")
    private String baseUrl;

    @Value("${amap.timeout:10000}")
    private int timeout;

    @Value("${amap.retry-count:3}")
    private int retryCount;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private final CloseableHttpClient httpClient;

    public AmapService() {
        // 配置HTTP客户端
        RequestConfig requestConfig = RequestConfig.custom()
                .setConnectTimeout(timeout)
                .setSocketTimeout(timeout)
                .setConnectionRequestTimeout(timeout)
                .build();

        this.httpClient = HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .setMaxConnTotal(100)
                .setMaxConnPerRoute(20)
                .build();
    }

    /**
     * 地理编码 - 将地址转换为坐标
     * 
     * @param address 地址
     * @param city 城市
     * @return 坐标字符串 "longitude,latitude"
     */
    public String geocode(String address, String city) {
        try {
            String url = buildGeocodeUrl(address, city);
            String response = executeHttpRequest(url);
            return parseGeocodeResponse(response);
        } catch (Exception e) {
            log.error("地理编码失败: address={}, city={}, error={}", address, city, e.getMessage());
            return null;
        }
    }

    /**
     * 逆地理编码 - 将坐标转换为地址
     * 
     * @param longitude 经度
     * @param latitude 纬度
     * @return 地址描述
     */
    public String reverseGeocode(double longitude, double latitude) {
        try {
            String url = buildReverseGeocodeUrl(longitude, latitude);
            String response = executeHttpRequest(url);
            return parseReverseGeocodeResponse(response);
        } catch (Exception e) {
            log.error("逆地理编码失败: lng={}, lat={}, error={}", longitude, latitude, e.getMessage());
            return null;
        }
    }

    /**
     * 路径规划
     * 
     * @param request 路径规划请求
     * @return 路径规划结果
     */
    public RouteResponse.RouteResult planRoute(RouteRequest request) {
        try {
            // 转换起终点为坐标
            String originCoord = convertToCoordinate(request.getOrigin(), request.getCity());
            String destCoord = convertToCoordinate(request.getDestination(), request.getCity());

            if (originCoord == null || destCoord == null) {
                log.error("起终点坐标转换失败: origin={}, destination={}", request.getOrigin(), request.getDestination());
                return null;
            }

            // 构建路径规划URL
            String url = buildRouteUrl(request, originCoord, destCoord);
            String response = executeHttpRequest(url);
            return parseRouteResponse(response, request.getTransportMode());

        } catch (Exception e) {
            log.error("路径规划失败: request={}, error={}", request, e.getMessage());
            return null;
        }
    }

    /**
     * 将地址或坐标转换为标准坐标格式
     */
    private String convertToCoordinate(String location, String city) {
        if (StringUtils.isEmpty(location)) {
            return null;
        }

        // 如果已经是坐标格式，直接返回
        if (RouteRequest.isValidCoordinate(location)) {
            return location;
        }

        // 否则进行地理编码
        return geocode(location, city);
    }

    /**
     * 构建地理编码URL
     */
    private String buildGeocodeUrl(String address, String city) {
        StringBuilder url = new StringBuilder(baseUrl + "/geocode/geo");
        url.append("?key=").append(webApiKey);
        url.append("&address=").append(URLEncoder.encode(address, StandardCharsets.UTF_8));
        if (StringUtils.hasText(city)) {
            url.append("&city=").append(URLEncoder.encode(city, StandardCharsets.UTF_8));
        }
        url.append("&output=json");
        return url.toString();
    }

    /**
     * 构建逆地理编码URL
     */
    private String buildReverseGeocodeUrl(double longitude, double latitude) {
        StringBuilder url = new StringBuilder(baseUrl + "/geocode/regeo");
        url.append("?key=").append(webApiKey);
        url.append("&location=").append(longitude).append(",").append(latitude);
        url.append("&output=json");
        url.append("&radius=1000");
        url.append("&extensions=base");
        return url.toString();
    }

    /**
     * 构建路径规划URL
     */
    private String buildRouteUrl(RouteRequest request, String origin, String destination) {
        String endpoint = getRouteEndpoint(request.getTransportMode());
        StringBuilder url = new StringBuilder(baseUrl + endpoint);
        url.append("?key=").append(webApiKey);
        url.append("&origin=").append(origin);
        url.append("&destination=").append(destination);
        
        // 添加途经点
        if (request.getFormattedWaypoints() != null) {
            url.append("&waypoints=").append(URLEncoder.encode(request.getFormattedWaypoints(), StandardCharsets.UTF_8));
        }
        
        // 添加策略
        url.append("&strategy=").append(request.getStrategy());
        
        // 添加其他参数
        url.append("&output=json");
        url.append("&extensions=all");
        
        if (StringUtils.hasText(request.getCity())) {
            url.append("&city=").append(URLEncoder.encode(request.getCity(), StandardCharsets.UTF_8));
        }
        
        return url.toString();
    }

    /**
     * 获取路径规划API端点
     */
    private String getRouteEndpoint(String transportMode) {
        switch (transportMode) {
            case "driving":
                return "/direction/driving";
            case "walking":
                return "/direction/walking";
            case "transit":
                return "/direction/transit/integrated";
            case "riding":
                return "/direction/bicycling";
            default:
                return "/direction/driving";
        }
    }

    /**
     * 执行HTTP请求
     */
    private String executeHttpRequest(String url) throws IOException {
        HttpGet httpGet = new HttpGet(url);
        httpGet.setHeader("User-Agent", "LJXZ-Cycling-Route/1.0");
        
        for (int i = 0; i < retryCount; i++) {
            try (CloseableHttpResponse response = httpClient.execute(httpGet)) {
                HttpEntity entity = response.getEntity();
                if (entity != null) {
                    String result = EntityUtils.toString(entity, StandardCharsets.UTF_8);
                    log.debug("高德API响应: {}", result);
                    return result;
                }
            } catch (IOException e) {
                log.warn("HTTP请求失败，第{}次重试: {}", i + 1, e.getMessage());
                if (i == retryCount - 1) {
                    throw e;
                }
                try {
                    Thread.sleep(1000 * (i + 1)); // 递增延迟
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new IOException("请求被中断", ie);
                }
            }
        }
        throw new IOException("HTTP请求失败，已重试" + retryCount + "次");
    }

    /**
     * 解析地理编码响应
     */
    private String parseGeocodeResponse(String response) throws Exception {
        JsonNode root = objectMapper.readTree(response);
        String status = root.path("status").asText();
        
        if (!"1".equals(status)) {
            log.error("地理编码API返回错误: {}", response);
            return null;
        }
        
        JsonNode geocodes = root.path("geocodes");
        if (geocodes.isArray() && geocodes.size() > 0) {
            String location = geocodes.get(0).path("location").asText();
            return location;
        }
        
        return null;
    }

    /**
     * 解析逆地理编码响应
     */
    private String parseReverseGeocodeResponse(String response) throws Exception {
        JsonNode root = objectMapper.readTree(response);
        String status = root.path("status").asText();
        
        if (!"1".equals(status)) {
            log.error("逆地理编码API返回错误: {}", response);
            return null;
        }
        
        JsonNode regeocode = root.path("regeocode");
        String address = regeocode.path("formatted_address").asText();
        return address;
    }

    /**
     * 解析路径规划响应
     */
    private RouteResponse.RouteResult parseRouteResponse(String response, String transportMode) throws Exception {
        JsonNode root = objectMapper.readTree(response);
        String status = root.path("status").asText();
        
        if (!"1".equals(status)) {
            log.error("路径规划API返回错误: {}", response);
            return null;
        }
        
        JsonNode route = root.path("route");
        if (route.isMissingNode()) {
            log.error("路径规划响应中缺少route字段: {}", response);
            return null;
        }
        
        return parseRouteData(route, transportMode);
    }

    /**
     * 解析路径数据
     */
    private RouteResponse.RouteResult parseRouteData(JsonNode route, String transportMode) {
        JsonNode paths = route.path("paths");
        if (!paths.isArray() || paths.size() == 0) {
            return null;
        }
        
        JsonNode path = paths.get(0); // 取第一条路径
        
        return RouteResponse.RouteResult.builder()
                .distance(path.path("distance").asInt())
                .duration(path.path("duration").asInt())
                .cost(path.path("tolls").asDouble(0.0))
                .trafficLights(path.path("traffic_lights").asInt(0))
                .polyline(path.path("polyline").asText())
                .transportMode(transportMode)
                .steps(parseRouteSteps(path.path("steps")))
                .build();
    }

    /**
     * 解析路径步骤
     */
    private List<RouteResponse.RouteStep> parseRouteSteps(JsonNode steps) {
        List<RouteResponse.RouteStep> stepList = new ArrayList<>();
        
        if (steps.isArray()) {
            for (int i = 0; i < steps.size(); i++) {
                JsonNode step = steps.get(i);
                RouteResponse.RouteStep routeStep = RouteResponse.RouteStep.builder()
                        .stepIndex(i + 1)
                        .instruction(step.path("instruction").asText())
                        .roadName(step.path("road").asText())
                        .distance(step.path("distance").asInt())
                        .duration(step.path("duration").asInt())
                        .polyline(step.path("polyline").asText())
                        .action(step.path("action").asText())
                        .assistantAction(step.path("assistant_action").asText())
                        .build();
                stepList.add(routeStep);
            }
        }
        
        return stepList;
    }
}