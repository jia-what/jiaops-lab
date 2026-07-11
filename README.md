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
├── app/                 # 运维工单业务应用（后续实现）
├── deploy/
│   ├── compose/         # Docker Compose 编排
│   ├── nginx/           # 反向代理配置
│   └── k8s/             # Kubernetes 清单（第四阶段）
├── monitoring/          # Prometheus / Grafana / Alertmanager
├── cicd/                # Jenkinsfile 与流水线说明
├── scripts/             # 运维脚本（备份、巡检、初始化等）
└── docs/                # 架构、部署、学习记录
```

## 分阶段计划

1. **基线**：仓库骨架 + CentOS 虚拟机环境 + 知识库笔记  
2. **容器化**：工单应用 + Nginx + MySQL + Redis，Compose 一键启动  
3. **交付与可观测**：Jenkins 流水线 + Prometheus / Grafana 监控告警  
4. **云原生**：迁移到 Kubernetes，补充 Terraform 与 AI 运维能力  

## 当前进度

- [x] 确定业务载体：运维工单  
- [x] 初始化仓库与目录骨架  
- [ ] CentOS 7 虚拟机基线检查与文档化  
- [ ] 工单应用最小可运行版本（MVP）  

## 本地开发（占位）

后续第二阶段会提供：

```bash
docker compose -f deploy/compose/docker-compose.yml up -d
```

## 知识库

学习笔记存放在 Obsidian：`Jia's DevOps Knowledge Base` → `03 Projects`。

## License

MIT
