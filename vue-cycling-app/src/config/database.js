// 数据库配置文件
const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: '123456',
  port: 3306,
  database: 'ljxz', // 数据库名称
  connectionLimit: 10,
  acquireTimeout: 60000,
  timeout: 60000,
  reconnect: true
};

export default dbConfig;