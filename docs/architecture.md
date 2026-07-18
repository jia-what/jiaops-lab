# 架构概览（草案）

```text
用户 / 运维
    │
    ▼
  Nginx
    │
    ▼
  工单应用 (app)
    ├── MySQL   （工单数据）
    └── Redis   （缓存 / 限流，可选）
    │
    ▼
Prometheus ←── 抓取 app / node / 容器指标
    │
    ├── Grafana（看板）
    └── Alertmanager（告警）
    │
    ▼
Jenkins 容器（检出、构建镜像、部署）
    │
    ▼
Docker Compose（现阶段） → Kubernetes（后期）
```

业务本身保持简单，复杂度放在部署、流水线与可观测性上。

## Phase 4 · Jenkins CI/CD

Jenkins 与业务 Compose 栈同机运行：Jenkins 容器挂载宿主机 Docker Socket，构建带有构建号和 Git SHA 的 `jiaops-app` 本地镜像，再用 `APP_TAG` 更新 Compose 中的 app 服务；最后从 `jiaops-nginx` 容器请求 `/health`。

```text
GitHub main → Jenkins → Docker Socket → 本地 app 镜像
                                  ↓
                         JiaOps Compose 栈 → /health
```

该 Docker Socket 权限只适合受控单机实验环境；生产环境应使用隔离的构建 Agent、最小权限凭据和镜像仓库。
