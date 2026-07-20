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
- 已合并 `main`（PR #2）

## Phase 5 — 监控（已完成）

- [x] 架构 / 端口 / 目录定稿；现网盘点（独立 `monitoring/` Compose）
- [x] Prometheus + Grafana + Alertmanager 最小部署与验收
- [x] Node Exporter / cAdvisor 抓取（Targets UP）
- [x] Grafana 数据源与看板（导入 1860；可自建业务 Panel）
- [x] 基础告警规则（TargetDown 等）
- [x] 告警外发沙箱：Mailpit + webhook-echo（真邮箱 SMTP 可另配）
- [x] 应用 `/metrics` + 建单计数器；Prometheus 接入 `jiaops-net`
- 已合并 `main`（PR #3 · `c04139e`）

详见 [`monitoring/README.md`](../monitoring/README.md)。

## Phase 6 — Kubernetes（当前）

- [ ] 本地集群（建议 kind）与最小清单
- [ ] 先迁 app；MySQL / Redis 暂留 Compose
- [ ] Service / NodePort → Ingress；探针与配置
- [ ] 与 Compose 版对照文档

其后：上云、Terraform、AIOps（原 Phase 6/7/8 能力继续后移）。
