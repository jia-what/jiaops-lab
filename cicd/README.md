# CI/CD · Jenkins Pipeline

[`Jenkinsfile`](Jenkinsfile) 是 JiaOps Lab 的单机 CI/CD 流水线定义。

```text
GitHub main
  ↓
Jenkins Checkout
  ↓
Build jiaops-app:build-<build-number>-<git-sha>
  ↓
docker compose up -d --no-build
  ↓
容器 Nginx /health 验证
```

## 前置条件

- Jenkins 按 [`deploy/jenkins/README.md`](../deploy/jenkins/README.md) 部署。
- Jenkins 容器已挂载宿主机 `/var/run/docker.sock`，并且镜像内有 Docker CLI 与 Compose 插件。
- 业务运行时环境文件位于 VM：`/opt/jiaops-compose/deploy/compose/.env`。
- 业务栈的 Compose project name 保持 `jiaops`，容器名保持 `jiaops-nginx`、`jiaops-app` 等。

## 阶段

| 阶段 | 作用 |
|---|---|
| Checkout | 从 SCM 拉取触发构建的提交，并生成短 SHA |
| Verify Docker access | 检查 Docker Socket、Compose 插件和 VM 的运行时 `.env` |
| Build image | 构建可追溯的本地镜像 tag |
| Deploy Compose stack | 以 `APP_TAG` 选择新镜像，更新现有 Compose 服务 |
| Health check | 在 `jiaops-nginx` 容器中请求 `/health`，失败会使构建失败 |

第一版不推送镜像仓库：构建和部署均在同一台实验机进行。后续上 Kubernetes 或多机部署时，再加入 Harbor、Docker Hub 或云镜像仓库。

## 运行时配置和密钥

- `deploy/compose/.env` 不提交；它包含 MySQL 密码与正式端口。
- Jenkinsfile 不包含密码、token 或管理员初始密码。
- 公开仓库仅需匿名检出；私有仓库改用 Jenkins Credentials 保存 GitHub token/SSH key。
- Jenkins 读取运行时 `.env` 是为了让 Compose 保持与现网一致，不会把内容打印到构建日志。

## 本地排查

```bash
docker exec jiaops-jenkins docker version
docker exec jiaops-jenkins docker compose version
docker exec jiaops-nginx wget -qO- http://127.0.0.1/health
docker logs --tail 100 jiaops-app
```

Webhook 仅在手动构建通过后启用。私网实验机不能被 GitHub 直接访问时，Webhook 不会送达；需要安全的公网入口、VPN 或反向隧道。
