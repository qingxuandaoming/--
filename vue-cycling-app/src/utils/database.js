import mysql from 'mysql2/promise';
import dbConfig from '../config/database.js';

// 创建连接池
const pool = mysql.createPool({
  host: dbConfig.host,
  user: dbConfig.user,
  password: dbConfig.password,
  port: dbConfig.port,
  database: dbConfig.database,
  waitForConnections: true,
  connectionLimit: dbConfig.connectionLimit,
  queueLimit: 0,
  acquireTimeout: dbConfig.acquireTimeout,
  timeout: dbConfig.timeout,
  reconnect: dbConfig.reconnect
});

// 数据库操作类
class Database {
  // 执行查询
  static async query(sql, params = []) {
    try {
      const [rows] = await pool.execute(sql, params);
      return rows;
    } catch (error) {
      console.error('数据库查询错误:', error);
      throw error;
    }
  }

  // 执行插入操作
  static async insert(table, data) {
    try {
      const keys = Object.keys(data);
      const values = Object.values(data);
      const placeholders = keys.map(() => '?').join(', ');
      const sql = `INSERT INTO ${table} (${keys.join(', ')}) VALUES (${placeholders})`;
      
      const [result] = await pool.execute(sql, values);
      return result;
    } catch (error) {
      console.error('数据库插入错误:', error);
      throw error;
    }
  }

  // 执行更新操作
  static async update(table, data, where, whereParams = []) {
    try {
      const keys = Object.keys(data);
      const values = Object.values(data);
      const setClause = keys.map(key => `${key} = ?`).join(', ');
      const sql = `UPDATE ${table} SET ${setClause} WHERE ${where}`;
      
      const [result] = await pool.execute(sql, [...values, ...whereParams]);
      return result;
    } catch (error) {
      console.error('数据库更新错误:', error);
      throw error;
    }
  }

  // 执行删除操作
  static async delete(table, where, whereParams = []) {
    try {
      const sql = `DELETE FROM ${table} WHERE ${where}`;
      const [result] = await pool.execute(sql, whereParams);
      return result;
    } catch (error) {
      console.error('数据库删除错误:', error);
      throw error;
    }
  }

  // 测试数据库连接
  static async testConnection() {
    try {
      const connection = await pool.getConnection();
      console.log('数据库连接成功!');
      connection.release();
      return true;
    } catch (error) {
      console.error('数据库连接失败:', error);
      return false;
    }
  }

  // 关闭连接池
  static async close() {
    try {
      await pool.end();
      console.log('数据库连接池已关闭');
    } catch (error) {
      console.error('关闭数据库连接池错误:', error);
    }
  }
}

export default Database;