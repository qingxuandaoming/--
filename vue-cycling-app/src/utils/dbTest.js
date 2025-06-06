import Database from './database.js';

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
        const result = await Database.query('SELECT 1 as test');
        console.log('✅ 数据库查询测试成功:', result);
        
        // 测试数据库和表是否存在
        const tables = await Database.query('SHOW TABLES');
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
    // 测试查询路线数据
    const routes = await Database.query('SELECT * FROM cycling_routes LIMIT 3');
    console.log('✅ 查询路线数据成功:', routes);
    
    // 测试插入操作（示例）
    const testData = {
      subject: '数据库连接测试',
      message: '这是一条测试反馈信息',
      contact_email: 'test@example.com',
      status: 'pending'
    };
    
    const insertResult = await Database.insert('feedback', testData);
    console.log('✅ 插入测试数据成功:', insertResult);
    
    // 删除测试数据
    await Database.delete('feedback', 'id = ?', [insertResult.insertId]);
    console.log('✅ 删除测试数据成功');
    
    return true;
  } catch (error) {
    console.error('❌ 数据库操作测试失败:', error.message);
    return false;
  }
}

// 在开发环境中自动运行测试
if (import.meta.env.DEV) {
  // 延迟执行，确保应用初始化完成
  setTimeout(async () => {
    await testDatabaseConnection();
    await testDatabaseOperations();
  }, 1000);
}