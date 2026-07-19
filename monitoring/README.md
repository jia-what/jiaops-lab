# Monitoring（Phase 5）

可观测性栈：Prometheus + Grafana + Alertmanager。  
与业务 Compose、Jenkins 分离，单独编排。

> 状态：第 2 步已写入最小配置。实验机启动与 Web UI 验收见第 3 步。

## 目录

```text
monitoring/
├── docker-compose.yml
├── .env.example          # 复制为 .env 后改 Grafana 密码
├── prometheus/
│   └── prometheus.yml    # 本步只抓 Prometheus 自己
└── alertmanager/
    └── alertmanager.yml  # null receiver（先不外发通知）
```

## 架构结论（2026-07-18 盘点）

```text
业务栈（jiaops · jiaops-net）     监控栈（jiaops-monitor · jiaops-monitor-net）
  jiaops-nginx  :80                 Prometheus   :9090
  jiaops-app                        Grafana      :3000
  jiaops-mysql                      Alertmanager :9093
  jiaops-redis                      （稍后）node-exporter :9100
Jenkins（独立）:8081                （稍后）cadvisor     :8082
```

| 决策 | 结论 |
|------|------|
| 编排方式 | 独立 Compose，目录本目录 `monitoring/` |
| Docker 网络 | 本步用 `jiaops-monitor-net`；业务 `jiaops-net` 后续按需接入 |
| 业务 / Jenkins | 不改动现有 compose |

## 端口（宿主机）

| 服务 | 端口 | 盘点结果 |
|------|------|----------|
| Prometheus | 9090 | 空闲 |
| Grafana | 3000 | 空闲 |
| Alertmanager | 9093 | 空闲 |
| Node Exporter（后续） | 9100 | 空闲 |
| cAdvisor（后续） | 8082 | 空闲（避开 Jenkins `:8081`） |

## 本地 / 实验机启动（第 3 步再用）

```bash
cd /opt/jiaops-compose/monitoring   # 或仓库里的 monitoring/
cp .env.example .env
# 编辑 .env：把 GRAFANA_ADMIN_PASSWORD 改成自己的

docker compose up -d
docker compose ps
```

浏览器（实验机 IP `192.168.153.8`）：

| 服务 | URL |
|------|-----|
| Prometheus | http://192.168.153.8:9090 |
| Grafana | http://192.168.153.8:3000 （`.env` 里的账号密码） |
| Alertmanager | http://192.168.153.8:9093 |

本步抓取目标：Prometheus → 自己（`job=prometheus`）。  
Grafana 数据源与看板、告警规则在后续步骤配置。

## 现网基线（实验机）

盘点时业务四容器 + Jenkins 均在跑；`jiaops-net` 存在。  
内存 available ≈ 6.1G；`/` 可用 ≈ 28G。

## 分步计划

1. [x] 定架构、端口、目录；盘点现网占用  
2. [x] 最小 Compose + Prometheus / Grafana / Alertmanager 配置  
3. [ ] 实验机启动与三端 Web UI 验收  
4. [ ] Node Exporter / cAdvisor 与抓取  
5. [ ] Grafana 数据源与基础看板  
6. [ ] Alertmanager 基础告警规则  
7. [ ]（可选）应用指标 / 告警联动工单  
