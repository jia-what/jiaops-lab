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
Jenkins（构建镜像并部署）
    │
    ▼
Docker Compose（现阶段） → Kubernetes（后期）
```

业务本身保持简单，复杂度放在部署、流水线与可观测性上。
