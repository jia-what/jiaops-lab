# Monitoring（Phase 5）

可观测性栈：Prometheus + Grafana + Alertmanager。  
与业务 Compose、Jenkins 分离，单独编排。

> 状态：Phase 5 含 7A/7B 已完成（应用指标 `jiaops-app` UP；建单计数验证；告警双通道已验）。

## 目录

```text
monitoring/
├── docker-compose.yml
├── .env.example
├── prometheus/
│   ├── prometheus.yml
│   └── rules/base.yml          # TargetDown / HostHighMemory / HostHighCpu
├── alertmanager/alertmanager.yml   # 仍为 null receiver
└── grafana/provisioning/datasources/datasource.yml
```

## 第 6 步：基础告警规则

同步（PowerShell）：

```powershell
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\docker-compose.yml" root@192.168.153.8:/opt/jiaops-compose/monitoring/docker-compose.yml
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\prometheus\prometheus.yml" root@192.168.153.8:/opt/jiaops-compose/monitoring/prometheus/prometheus.yml
scp -r "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\prometheus\rules" root@192.168.153.8:/opt/jiaops-compose/monitoring/prometheus/
```

实验机：

```bash
cd /opt/jiaops-compose/monitoring
docker compose up -d prometheus
docker compose restart prometheus

# 配置是否加载成功（应返回 success 或无 error）
curl -s -X POST http://127.0.0.1:9090/-/reload
```

验收：

1. 浏览器 http://192.168.153.8:9090/rules → 能看到 `TargetDown` / `HostHighMemory` / `HostHighCpu`
2. 演示触发（约等 1～2 分钟）：

```bash
docker stop jiaops-node-exporter
# 打开 http://192.168.153.8:9090/alerts 看 TargetDown 变为 Firing
# 打开 http://192.168.153.8:9093 看 Alertmanager 是否收到

docker start jiaops-node-exporter   # 测完务必恢复
```

## 第 7A 步：告警外发（Mailpit + Webhook）

| 服务 | 宿主机 | 作用 |
|------|--------|------|
| Mailpit UI | :8025 | 看「收到的告警邮件」 |
| Mailpit SMTP | :1025 | Alertmanager 发信目标（也在容器网 `mailpit:1025`） |
| webhook-echo | :8083 | 浏览器可看回显；日志里也有 POST |

同步后：

```bash
cd /opt/jiaops-compose/monitoring
# .env 可补：MAILPIT_UI_PORT=8025  WEBHOOK_ECHO_HOST_PORT=8083
docker compose up -d
docker compose restart alertmanager
docker compose ps
```

验收：

```bash
# 触发
docker stop jiaops-node-exporter
# 等 1～2 分钟后：
# 1) 浏览器 http://192.168.153.8:8025 应有邮件
# 2) docker logs --tail 50 jiaops-webhook-echo 应有 POST / JSON
# 3) http://192.168.153.8:9093 告警存在

docker start jiaops-node-exporter
```

## 第 7B 步：应用 `/metrics`

**1）同步代码到 VM（GitHub 不通时用 scp，PowerShell）：**

```powershell
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\app\app.py" root@192.168.153.8:/opt/jiaops-compose/app/app.py
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\app\requirements.txt" root@192.168.153.8:/opt/jiaops-compose/app/requirements.txt
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\docker-compose.yml" root@192.168.153.8:/opt/jiaops-compose/monitoring/docker-compose.yml
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\prometheus\prometheus.yml" root@192.168.153.8:/opt/jiaops-compose/monitoring/prometheus/prometheus.yml
```

**2）重建业务 app（新依赖要进镜像）：**

```bash
cd /opt/jiaops-compose/deploy/compose
docker compose --profile with-redis build app
docker compose --profile with-redis up -d app
curl -s http://127.0.0.1/health
# 经 Nginx 反代即可看到指标（app 镜像无 wget）
curl -s http://127.0.0.1/metrics | head -20
```

**3）让 Prometheus 接入业务网并重载：**

```bash
cd /opt/jiaops-compose/monitoring
docker compose up -d prometheus
docker compose restart prometheus
```

**4）验收：** Targets 中 `jiaops-app` 为 UP；网页建一张工单后：

```bash
curl -s http://127.0.0.1/metrics | grep jiaops_tickets_created
# Prometheus 图形界面查询：jiaops_tickets_created_total
```

## 第 5 步：Grafana 数据源 + 导入看板

同步到 VM（PowerShell 示例）：

```powershell
scp "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\docker-compose.yml" root@192.168.153.8:/opt/jiaops-compose/monitoring/docker-compose.yml
scp -r "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\grafana" root@192.168.153.8:/opt/jiaops-compose/monitoring/
```

实验机：

```bash
cd /opt/jiaops-compose/monitoring
docker compose up -d grafana
docker compose restart grafana
```

浏览器 http://192.168.153.8:3000 ：

1. 登录（`.env` 里的 admin / 密码）
2. **Connections → Data sources** → 应有 **Prometheus**，点进去 **Save & test** 应成功  
3. **Dashboards → New → Import** → 输入 **1860** → Load  
4. Prometheus 数据源选刚配的 **Prometheus** → Import  
5. 打开看板，确认有 CPU / Memory 等曲线（job 选 `node` 相关实例）

## 架构结论（2026-07-18 盘点）

```text
业务栈（jiaops · jiaops-net）     监控栈（jiaops-monitor · jiaops-monitor-net）
  jiaops-nginx  :80                 Prometheus     :9090
  jiaops-app                        Grafana        :3000
  jiaops-mysql                      Alertmanager   :9093
  jiaops-redis                      node-exporter  :9100
Jenkins（独立）:8081                cadvisor       :8082
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
| Node Exporter | 9100 | 空闲（第 1 步盘点） |
| cAdvisor | 8082 | 空闲（避开 Jenkins `:8081`） |

## 第 4 步：同步到实验机并验收抓取

GitHub 出网不通时可用 scp（在 Windows PowerShell）：

```powershell
scp -r "E:\VM\jiawhat虚拟机\jiawhat项目.worktrees\phase5\monitoring\*" root@192.168.153.8:/opt/jiaops-compose/monitoring/
```

实验机：

```bash
cd /opt/jiaops-compose/monitoring
# 若还没有 .env：cp .env.example .env
# 若已有 .env，可手动补上 NODE_EXPORTER_HOST_PORT / CADVISOR_HOST_PORT（或重新对照 .env.example）

docker compose up -d
docker compose ps

# 配置已挂载进容器后，重启 Prometheus 以加载新 scrape
docker compose restart prometheus
```

验收：

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9100/metrics
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8082/metrics
```

浏览器打开 Prometheus → **Status → Targets**：`prometheus` / `node` / `cadvisor` 均为 **UP**。

> cAdvisor：实验机直连 `gcr.io` 超时，Compose 使用 `m.daocloud.io/gcr.io/cadvisor/cadvisor:v0.49.1`（同一镜像，代理拉取）。

## 启动三件套（回顾）

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

抓取目标：`prometheus`（自己）· `node` · `cadvisor`。  
Grafana 数据源与看板、告警规则在后续步骤配置。

## 现网基线（实验机）

盘点时业务四容器 + Jenkins 均在跑；`jiaops-net` 存在。  
内存 available ≈ 6.1G；`/` 可用 ≈ 28G。

## 分步计划

1. [x] 定架构、端口、目录；盘点现网占用  
2. [x] 最小 Compose + Prometheus / Grafana / Alertmanager 配置  
3. [x] 实验机启动与三端 Web UI 验收（2026-07-19；VM 曾用 scp，GitHub 出网恢复后再 git 对齐）  
4. [x] Node Exporter / cAdvisor 与抓取（2026-07-19；gcr 超时改用 m.daocloud.io 代理）  
5. [x] Grafana 数据源与基础看板（1860 · job=node · instance=node-exporter:9100）  
6. [x] 基础告警规则（TargetDown 演示 FIRING 后已恢复）  
7A. [x] 告警外发：Mailpit + webhook-echo（TargetDown 双通道已验）  
7B. [x] 应用 `/metrics` + 建单计数器（`jiaops-app` Targets UP；`jiaops_tickets_created_total` 验证）  
