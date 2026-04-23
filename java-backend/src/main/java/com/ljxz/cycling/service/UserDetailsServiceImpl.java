package com.ljxz.cycling.service;

import com.ljxz.cycling.entity.User;
import com.ljxz.cycling.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * 用户详情服务实现类
 * 
 * @author LJXZ Team
 * @version 1.0.0
 */
@Service
@RequiredArgsConstructor
public class UserDetailsServiceImpl implements UserDetailsService {
    
    private final UserRepository userRepository;
    
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userRepository.findByUsernameOrEmail(username, username)
                .orElseThrow(() -> new UsernameNotFoundException("用户不存在: " + username));
        
        if (Boolean.FALSE.equals(user.getIsActive())) {
            throw new UsernameNotFoundException("用户已被禁用: " + username);
        }
        
        return user;
    }
}