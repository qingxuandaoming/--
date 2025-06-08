import Database from './database.js';
import { DB_TEST_CONFIG } from './dbTestConfig.js';

// 数据库连接测试函数
export async function testDatabaseConnection() {
  console.log('开始测试数据库连接...');
  
  try {
    // 测试连接
    const isConnected = await Database.testConnection();
    
    if (isConnected) {
      console.log('✅ 数据库连接测试成功!');
      
      // 测试基本查询
      try {
        const result = await Database.query('/test');
        console.log('✅ 数据库查询测试成功:', result);
        
        // 测试数据库和表是否存在
        const tables = await Database.query('/tables');
        console.log('📋 数据库中的表:', tables);
        
        return true;
      } catch (queryError) {
        console.error('❌ 数据库查询测试失败:', queryError.message);
        return false;
      }
    } else {
      console.error('❌ 数据库连接测试失败');
      return false;
    }
  } catch (error) {
    console.error('❌ 数据库连接测试出错:', error.message);
    return false;
  }
}

// 测试数据库操作
export async function testDatabaseOperations() {
  console.log('开始测试数据库操作...');
  
  try {
    // 测试Python后端 - 装备分类查询
    console.log('🔧 测试Python后端装备API...');
    const categories = await Database.queryPython('/equipment/categories');
    console.log('✅ Python后端装备分类查询成功:', categories);
    
    // 测试Python后端 - 装备搜索
    const equipment = await Database.queryPython('/equipment/search', { 
      keyword: '自行车', 
      page: 1, 
      per_page: 3 
    });
    console.log('✅ Python后端装备搜索成功:', equipment);
    
    // 测试智能查询 - 会自动选择合适的后端
    console.log('🧠 测试智能查询...');
    const smartResult = await Database.smartQuery('/equipment/categories');
    console.log('✅ 智能查询装备分类成功:', smartResult);
    
    console.log('✅ 数据库操作测试完成');
    return true;
  } catch (error) {
    console.error('❌ 数据库操作测试失败:', error.message);
    return false;
  }
}

// 在开发环境中自动运行测试
if (import.meta.env.DEV && DB_TEST_CONFIG.enableAutoTest) {
  // 延迟执行，确保应用初始化完成
  setTimeout(async () => {
    console.log('🔧 开始数据库连接测试...');
    await testDatabaseConnection();
    await testDatabaseOperations();
  }, DB_TEST_CONFIG.testDelay);
} else if (import.meta.env.DEV) {
  console.log('ℹ️ 数据库自动测试已禁用。如需测试，请手动调用 testDatabaseConnection() 和 testDatabaseOperations()');
}