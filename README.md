# JiaOps Lab

面向中小型业务系统的 **云原生自动化运维实验平台**。  
业务载体是一个极简的 **运维工单系统**；简历上真正体现的是外围能力：容器化、CI/CD、监控告警、Kubernetes 与 AI 运维。

> 仓库：https://github.com/jia-what/jiaops-lab · 当前默认分支 **`main`**（已含 Phase 5，PR #3）

## 项目定位

| 层次 | 内容 |
|------|------|
| 业务层 | 运维工单：提交故障 → 处理 → 关单 |
| 平台层 | Docker / Compose / Nginx / MySQL / Redis |
| 交付层 | Git + Jenkins CI/CD |
| 可观测 | Prometheus + Grafana + Alertmanager（含节点/容器/应用指标） |
| 编排层 | Kubernetes（Phase 6） |
| 智能层 | AI 辅助故障诊断（后期） |

## 目录结构

```text
jiaops-lab/
├── app/                 # 运维工单业务应用（Flask MVP · /health · /metrics）
├── deploy/
│   ├── compose/         # Docker Compose 编排（Phase 3）
│   ├── jenkins/         # Jenkins Docker 部署（Phase 4）
│   ├── nginx/           # 反向代理（裸机 + Compose）
│   └── k8s/             # Kubernetes 清单（Phase 6）
├── monitoring/          # Prometheus / Grafana / Alertmanager（Phase 5）
├── cicd/                # Jenkinsfile 与流水线说明
├── scripts/             # 运维脚本（备份、巡检、初始化等）
└── docs/                # 架构、部署、学习记录
```

## 分阶段计划

1. **基线**：仓库骨架 + CentOS 虚拟机环境 + 知识库笔记  
2. **工单 MVP（已完成）**：App + MySQL + Nginx 反代  
3. **容器化（已完成）**：Compose 一键启动，Nginx / Flask / MySQL / Redis 正式运行  
4. **交付（已完成）**：Jenkins CI/CD（PR #2）  
5. **可观测性（已完成）**：Prometheus / Grafana / Alertmanager（PR #3）  
6. **云原生（进行中）**：Kubernetes；其后上云 / Terraform / AIOps  

## 当前进度

- [x] 确定业务载体：运维工单  
- [x] 初始化仓库与目录骨架  
- [x] CentOS 7 虚拟机基线检查与文档化（见 `docs/vm-setup.md`）  
- [x] 裸机安装 MySQL / Nginx / Redis  
- [x] 工单应用 MVP（Flask + MySQL）  
- [x] Nginx 反代到应用（`:80` → `:5000`）  
- [x] Docker Engine + Compose 插件  
- [x] Docker Compose 一键部署，容器 Nginx 已接管宿主机 `:80`  
- [x] Jenkins 容器部署与管理员初始化（`:8081`）  
- [x] Jenkinsfile：检出 → 本机镜像构建 → Compose 更新 → `/health` 验证  
- [x] 自动触发：私网 Webhook 不可达，已用 Poll SCM 验证  
- [x] 监控栈：Prometheus / Grafana / Alertmanager（独立 Compose）  
- [x] Node Exporter + cAdvisor 抓取；Grafana 看板（如 1860）  
- [x] 基础告警规则 + Mailpit / webhook 外发沙箱（真邮箱 SMTP 可另配，勿提交授权码）  
- [x] 应用 `GET /metrics` 与建单计数器 `jiaops_tickets_created_total`  
- [ ] Phase 6：Kubernetes 部署工单应用（与 Compose 对照）  

实验机常用入口（示例 IP `192.168.153.8`）：

| 入口 | 地址 |
|------|------|
| 工单 | http://192.168.153.8/ |
| Jenkins | http://192.168.153.8:8081 |
| Prometheus | http://192.168.153.8:9090 |
| Grafana | http://192.168.153.8:3000 |
| Alertmanager | http://192.168.153.8:9093 |
| Mailpit（告警邮件沙箱） | http://192.168.153.8:8025 |

## 手动运行（Phase 2 裸机 MVP）

虚拟机上（示例）：

```bash
cd /opt/jiaops-lab/app
source ../.venv/bin/activate
cp .env.example .env   # 填写数据库密码
python app.py          # 默认 0.0.0.0:5000
```

Nginx 配置见 `deploy/nginx/jiaops.conf`。  
访问：`http://<虚拟机IP>/` ，健康检查：`/health`

## Docker Compose（Phase 3）

正式运行时映射 **宿主机 80 → 容器 Nginx 80**。Jenkins Web UI 使用 `:8081`，不与业务入口冲突。

```bash
cd deploy/compose
cp .env.example .env
docker compose up -d --build

docker compose --profile with-redis ps
curl -s http://127.0.0.1/health
# 浏览器：http://192.168.153.8/
```

可选 Redis：`docker compose --profile with-redis up -d`  
说明见 [`deploy/compose/README.md`](deploy/compose/README.md)。

## Jenkins CI/CD（Phase 4）

Jenkins 部署文件在 [`deploy/jenkins/`](deploy/jenkins/)，流水线定义在 [`cicd/Jenkinsfile`](cicd/Jenkinsfile)。

```text
GitHub main → Jenkins 检出 → 构建本地 app 镜像 → 更新 Compose 栈 → /health 验证
```

首次部署和 Jenkins 任务配置见 [`deploy/jenkins/README.md`](deploy/jenkins/README.md)。  
自动触发说明见 [`cicd/README.md`](cicd/README.md)。该单机实验方案会挂载宿主机 Docker Socket，具有宿主机 Docker 管理权限，仅限受控实验环境。

## 监控与告警（Phase 5）

监控为**独立 Compose 项目**（`monitoring/`），与业务栈、Jenkins 分离；说明见 [`monitoring/README.md`](monitoring/README.md)。

```bash
cd monitoring
cp .env.example .env          # 修改 Grafana 初始密码
docker compose up -d
docker compose ps
```

主要能力：

- 抓取：Prometheus 自身、Node Exporter、cAdvisor、工单应用 `/metrics`  
- 看板：Grafana（数据源 provisioning；可导入社区看板 1860 或自建业务 Panel）  
- 告警：`prometheus/rules/base.yml` → Alertmanager → Mailpit（邮件沙箱）+ webhook-echo  
- 仓库默认使用 Mailpit；真 SMTP（如 QQ）仅在实验机本地配置，**授权码勿提交 Git**

架构要点：Prometheus 同时加入 `jiaops-monitor-net` 与外部网络 `jiaops-net`，以便抓取 `jiaops-app:5000/metrics`。

## 知识库

学习笔记存放在 Obsidian：`Jia's DevOps Knowledge Base` → `03 Projects` / `02 Learning`（含 Docker、Jenkins、Prometheus-Grafana 等）。

## License

MIT
