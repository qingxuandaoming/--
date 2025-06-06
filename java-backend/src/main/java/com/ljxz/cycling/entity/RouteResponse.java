package com.ljxz.cycling.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;
import com.fasterxml.jackson.annotation.JsonFormat;

import java.time.LocalDateTime;
import java.util.List;

/**
 * 路径规划响应实体
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RouteResponse {

    /**
     * 响应状态码
     * 1: 成功
     * 0: 失败
     */
    private Integer status;

    /**
     * 响应信息
     */
    private String message;

    /**
     * 路径规划结果
     */
    private RouteResult route;

    /**
     * 响应时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime timestamp;

    /**
     * 请求处理耗时（毫秒）
     */
    private Long processingTime;

    /**
     * 路径规划结果详情
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class RouteResult {

        /**
         * 起点坐标
         */
        private Coordinate origin;

        /**
         * 终点坐标
         */
        private Coordinate destination;

        /**
         * 总距离（米）
         */
        private Integer distance;

        /**
         * 总时长（秒）
         */
        private Integer duration;

        /**
         * 预计费用（元，仅驾车路径）
         */
        private Double cost;

        /**
         * 红绿灯数量
         */
        private Integer trafficLights;

        /**
         * 路径几何信息（编码后的路径点）
         */
        private String polyline;

        /**
         * 详细路径步骤
         */
        private List<RouteStep> steps;

        /**
         * 交通方式
         */
        private String transportMode;

        /**
         * 路径策略
         */
        private Integer strategy;

        /**
         * 限行信息
         */
        private RestrictionInfo restriction;

        /**
         * 获取格式化距离
         * @return 格式化的距离字符串
         */
        public String getFormattedDistance() {
            if (distance == null) return "未知";
            if (distance < 1000) {
                return distance + "米";
            } else {
                return String.format("%.1f公里", distance / 1000.0);
            }
        }

        /**
         * 获取格式化时长
         * @return 格式化的时长字符串
         */
        public String getFormattedDuration() {
            if (duration == null) return "未知";
            int hours = duration / 3600;
            int minutes = (duration % 3600) / 60;
            if (hours > 0) {
                return hours + "小时" + minutes + "分钟";
            } else {
                return minutes + "分钟";
            }
        }
    }

    /**
     * 坐标信息
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class Coordinate {
        /**
         * 经度
         */
        private Double longitude;

        /**
         * 纬度
         */
        private Double latitude;

        /**
         * 地址描述
         */
        private String address;

        /**
         * 获取坐标字符串
         * @return 经度,纬度格式的字符串
         */
        public String getCoordinateString() {
            return longitude + "," + latitude;
        }
    }

    /**
     * 路径步骤详情
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class RouteStep {
        /**
         * 步骤序号
         */
        private Integer stepIndex;

        /**
         * 步骤描述
         */
        private String instruction;

        /**
         * 道路名称
         */
        private String roadName;

        /**
         * 步骤距离（米）
         */
        private Integer distance;

        /**
         * 步骤时长（秒）
         */
        private Integer duration;

        /**
         * 步骤起点坐标
         */
        private Coordinate startLocation;

        /**
         * 步骤终点坐标
         */
        private Coordinate endLocation;

        /**
         * 步骤路径点
         */
        private String polyline;

        /**
         * 转向动作
         * 如：直行、左转、右转等
         */
        private String action;

        /**
         * 辅助动作
         */
        private String assistantAction;
    }

    /**
     * 限行信息
     */
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class RestrictionInfo {
        /**
         * 是否有限行
         */
        private Boolean hasRestriction;

        /**
         * 限行描述
         */
        private String description;

        /**
         * 限行时间段
         */
        private String timeRange;

        /**
         * 限行区域
         */
        private String area;
    }

    /**
     * 创建成功响应
     * @param route 路径结果
     * @param processingTime 处理时间
     * @return 成功响应
     */
    public static RouteResponse success(RouteResult route, Long processingTime) {
        return RouteResponse.builder()
                .status(1)
                .message("路径规划成功")
                .route(route)
                .timestamp(LocalDateTime.now())
                .processingTime(processingTime)
                .build();
    }

    /**
     * 创建失败响应
     * @param message 错误信息
     * @param processingTime 处理时间
     * @return 失败响应
     */
    public static RouteResponse failure(String message, Long processingTime) {
        return RouteResponse.builder()
                .status(0)
                .message(message)
                .timestamp(LocalDateTime.now())
                .processingTime(processingTime)
                .build();
    }
}