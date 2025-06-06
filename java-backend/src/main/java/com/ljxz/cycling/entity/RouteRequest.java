package com.ljxz.cycling.entity;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import lombok.Builder;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import java.util.List;

/**
 * 路径规划请求实体
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RouteRequest {

    /**
     * 起点地址或坐标
     * 支持格式：
     * 1. 地址描述："石家庄市长安区"
     * 2. 坐标格式："114.502461,38.045474"
     */
    @NotBlank(message = "起点不能为空")
    @Size(max = 200, message = "起点描述不能超过200个字符")
    private String origin;

    /**
     * 终点地址或坐标
     * 支持格式：
     * 1. 地址描述："石家庄市裕华区"
     * 2. 坐标格式："114.522461,38.065474"
     */
    @NotBlank(message = "终点不能为空")
    @Size(max = 200, message = "终点描述不能超过200个字符")
    private String destination;

    /**
     * 途经点列表（可选）
     * 最多支持16个途经点
     */
    @Size(max = 16, message = "途经点最多支持16个")
    private List<String> waypoints;

    /**
     * 交通方式
     * driving: 驾车
     * walking: 步行
     * transit: 公交
     * riding: 骑行
     */
    @NotBlank(message = "交通方式不能为空")
    @Pattern(regexp = "^(driving|walking|transit|riding)$", 
             message = "交通方式只能是：driving(驾车)、walking(步行)、transit(公交)、riding(骑行)")
    private String transportMode;

    /**
     * 城市编码或名称（可选）
     * 默认为石家庄
     */
    private String city;

    /**
     * 路径规划策略（可选）
     * 0: 速度优先（时间）
     * 1: 费用优先（金钱）
     * 2: 距离优先
     * 3: 不走快速路
     * 4: 躲避拥堵
     * 5: 多策略（同时使用速度优先、费用优先、距离优先三个策略）
     * 6: 不走高速
     * 7: 不走高速且避免收费
     * 8: 躲避收费和拥堵
     * 9: 不走高速且躲避收费和拥堵
     */
    @Builder.Default
    private Integer strategy = 0;

    /**
     * 是否返回路径详细信息
     * true: 返回详细路径点
     * false: 只返回基本信息
     */
    @Builder.Default
    private Boolean showSteps = true;

    /**
     * 坐标系类型
     * gcj02: 国测局坐标系（默认）
     * wgs84: GPS坐标系
     * bd09ll: 百度坐标系
     */
    @Builder.Default
    private String coordType = "gcj02";

    /**
     * 是否避开限行
     * 0: 不考虑限行
     * 1: 避开限行
     */
    @Builder.Default
    private Integer avoidRestriction = 0;

    /**
     * 车牌号（用于限行判断，可选）
     */
    private String plateNumber;

    /**
     * 请求时间戳
     */
    private Long timestamp;

    /**
     * 用户ID（可选，用于个性化推荐）
     */
    private String userId;

    /**
     * 验证坐标格式
     * @param coordinate 坐标字符串
     * @return 是否为有效坐标格式
     */
    public static boolean isValidCoordinate(String coordinate) {
        if (coordinate == null || coordinate.trim().isEmpty()) {
            return false;
        }
        // 匹配经纬度格式：longitude,latitude
        String pattern = "^-?\\d+\\.\\d+,-?\\d+\\.\\d+$";
        return coordinate.matches(pattern);
    }

    /**
     * 获取格式化的途经点字符串
     * @return 途经点字符串，用分号分隔
     */
    public String getFormattedWaypoints() {
        if (waypoints == null || waypoints.isEmpty()) {
            return null;
        }
        return String.join(";", waypoints);
    }
}