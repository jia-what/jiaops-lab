-- 工单表结构（Navicat / mysql 客户端执行）
-- 库：jiaops

CREATE TABLE IF NOT EXISTS tickets (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '工单ID',
  title VARCHAR(200) NOT NULL COMMENT '标题',
  description TEXT COMMENT '描述',
  priority ENUM('low', 'medium', 'high', 'critical') NOT NULL DEFAULT 'medium' COMMENT '优先级',
  status ENUM('open', 'in_progress', 'resolved', 'closed') NOT NULL DEFAULT 'open' COMMENT '状态',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (id),
  KEY idx_status (status),
  KEY idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='运维工单';
