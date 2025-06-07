package com.ljxz.cycling;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.CrossOrigin;

/**
 * 灵境行者路径规划后端服务启动类
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@SpringBootApplication

public class CyclingRouteApplication {

    public static void main(String[] args) {
        SpringApplication.run(CyclingRouteApplication.class, args);
        System.out.println("\n" +
                "  ██╗     ██╗██╗  ██╗███████╗    ██████╗  ██████╗ ██╗   ██╗████████╗███████╗\n" +
                "  ██║     ██║╚██╗██╔╝╚══███╔╝    ██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██╔════╝\n" +
                "  ██║     ██║ ╚███╔╝   ███╔╝     ██████╔╝██║   ██║██║   ██║   ██║   █████╗  \n" +
                "  ██║██   ██║ ██╔██╗  ███╔╝      ██╔══██╗██║   ██║██║   ██║   ██║   ██╔══╝  \n" +
                "  ╚█████████║██╔╝ ██╗███████╗    ██║  ██║╚██████╔╝╚██████╔╝   ██║   ███████╗\n" +
                "   ╚════════╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝\n" +
                "\n" +
                "  :: 灵境行者路径规划服务 ::                    (v1.0.0)\n");
    }
}