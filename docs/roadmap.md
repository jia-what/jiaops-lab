# 项目路线图

对齐学习阶段，边学边往平台上叠能力。

## Phase 0 — 基线

- 仓库与目录骨架
- 知识库项目页
- CentOS 虚拟机基线检查与笔记

## Phase 1 — Linux 收尾

- 权限 / 用户 / systemd / 网络 笔记入库
- 虚拟机初始化脚本固化

## Phase 2 — 工单 MVP

- 工单应用 MVP
- MySQL + Nginx + systemd

## Phase 3 — 容器化

- Docker + Compose + Nginx + MySQL + Redis
- 一键启动与健康检查

## Phase 4 — CI/CD

- Jenkins Docker 部署
- Jenkins 流水线：检出 → 构建本地镜像 → Compose 部署 → `/health`
- 自动触发：Webhook（需公网）或 Poll SCM（私网实验采用）

## Phase 5 — 监控（当前）

- [x] 架构 / 端口 / 目录定稿；现网盘点（独立 `monitoring/` Compose）
- [x] 仓库写入最小 Compose + Prometheus / Grafana / Alertmanager 配置
- [ ] 实验机启动与三端 Web UI 验收
- [ ] 节点 / 容器抓取与 Grafana 看板
- [ ] Alertmanager 基础告警规则

详见 [`monitoring/README.md`](../monitoring/README.md)。

## Phase 6 — 云原生与 AIOps

- Kubernetes 部署
- Terraform 基础
- AI 辅助故障诊断
- 云厂商实践（阿里云 / 腾讯云）
