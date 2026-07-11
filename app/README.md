# 运维工单应用（占位）

本目录将实现 JiaOps Lab 的业务载体：**运维工单系统**。

## 计划中的最小功能（MVP）

- 创建工单（标题、描述、优先级）
- 工单列表与详情
- 更新状态：`open` → `in_progress` → `resolved` → `closed`
- 健康检查接口 `/health`（供监控与编排探活）

## 技术选型（第二阶段确定）

倾向：Python（Flask 或 FastAPI）+ MySQL + Redis。  
当前阶段先完成 Linux 基线与仓库结构，不急着写业务代码。

## 状态字段约定（草案）

| 字段 | 说明 |
|------|------|
| id | 工单 ID |
| title | 标题 |
| description | 描述 |
| priority | low / medium / high / critical |
| status | open / in_progress / resolved / closed |
| created_at / updated_at | 时间戳 |
