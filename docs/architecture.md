# 架构概览

```text
用户 / 运维
    │
    ▼
  Nginx（Compose · :80）
    │
    ▼
  工单应用 (app)
    ├── MySQL   （工单数据）
    ├── Redis   （缓存，可选 profile）
    └── /metrics ←── Prometheus 抓取（业务指标）
    │
Prometheus（独立 Compose · monitoring/）
    ← node-exporter / cAdvisor / app
    │
    ├── Grafana（看板）
    └── Alertmanager → Mailpit / webhook（告警外发）
    │
Jenkins 容器（:8081 · Docker Socket）
    │
    ▼
Docker Compose（现阶段） → Kubernetes（Phase 6）
```

业务本身保持简单，复杂度放在部署、流水线与可观测性上。  
三套 Compose 同机并行：业务 `jiaops`、Jenkins `jiaops-jenkins`、监控 `jiaops-monitor`。

## Phase 4 · Jenkins CI/CD

Jenkins 与业务 Compose 栈同机运行：Jenkins 容器挂载宿主机 Docker Socket，构建带有构建号和 Git SHA 的 `jiaops-app` 本地镜像，再用 `APP_TAG` 更新 Compose 中的 app 服务；最后从 `jiaops-nginx` 容器请求 `/health`。

```text
GitHub main → Jenkins → Docker Socket → 本地 app 镜像
                                  ↓
                         JiaOps Compose 栈 → /health
```

该 Docker Socket 权限只适合受控单机实验环境；生产环境应使用隔离的构建 Agent、最小权限凭据和镜像仓库。

## Phase 5 · 可观测性

监控栈独立于业务编排，目录 `monitoring/`。Prometheus 同时加入监控网络与业务网络 `jiaops-net`，以抓取 `jiaops-app:5000/metrics`。

```text
Exporters / app:/metrics → Prometheus → Grafana
                              ↓
                         Alertmanager → Mailpit / webhook-echo
```

详情见 [`monitoring/README.md`](../monitoring/README.md)。
