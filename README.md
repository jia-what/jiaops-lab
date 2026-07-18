# JiaOps Lab

面向中小型业务系统的 **云原生自动化运维实验平台**。  
业务载体是一个极简的 **运维工单系统**；简历上真正体现的是外围能力：容器化、CI/CD、监控告警、Kubernetes 与 AI 运维。

> 仓库：https://github.com/jia-what/jiaops-lab

## 项目定位

| 层次 | 内容 |
|------|------|
| 业务层 | 运维工单：提交故障 → 处理 → 关单 |
| 平台层 | Docker / Compose / Nginx / MySQL / Redis |
| 交付层 | Git + Jenkins CI/CD |
| 可观测 | Prometheus + Grafana + Alertmanager |
| 编排层 | Kubernetes |
| 智能层 | AI 辅助故障诊断（后期） |

## 目录结构

```text
jiaops-lab/
├── app/                 # 运维工单业务应用（Flask MVP）
├── deploy/
│   ├── compose/         # Docker Compose 编排（Phase 3）
│   ├── jenkins/         # Jenkins Docker 部署（Phase 4）
│   ├── nginx/           # 反向代理（裸机 + Compose）
│   └── k8s/             # Kubernetes 清单（后期）
├── monitoring/          # Prometheus / Grafana / Alertmanager
├── cicd/                # Jenkinsfile 与流水线说明
├── scripts/             # 运维脚本（备份、巡检、初始化等）
└── docs/                # 架构、部署、学习记录
```

## 分阶段计划

1. **基线**：仓库骨架 + CentOS 虚拟机环境 + 知识库笔记  
2. **工单 MVP（已完成手动部署）**：App + MySQL + Nginx 反代  
3. **容器化（已完成）**：Compose 一键启动，Nginx / Flask / MySQL / Redis 正式运行
4. **交付（进行中）**：Jenkins CI/CD
5. **可观测性**：Prometheus / Grafana / Alertmanager
6. **云原生 / 上云 / AIOps**：Kubernetes、云厂商、AI 辅助排障

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
GitHub phase4 → Jenkins 检出 → 构建本地 app 镜像 → 更新 Compose 栈 → /health 验证
```

首次部署和 Jenkins 任务配置见 [`deploy/jenkins/README.md`](deploy/jenkins/README.md)。  
自动触发说明见 [`cicd/README.md`](cicd/README.md)。该单机实验方案会挂载宿主机 Docker Socket，具有宿主机 Docker 管理权限，仅限受控实验环境。

## 知识库

学习笔记存放在 Obsidian：`Jia's DevOps Knowledge Base` → `03 Projects`。

## License

MIT
