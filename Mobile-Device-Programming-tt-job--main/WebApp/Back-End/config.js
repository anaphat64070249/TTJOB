const mysql = require('mysql2/promise');

// config your database

const pool = mysql.createPool({
  host: 'your host name',
  user: 'username',
  password: '',
  database: '',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool;