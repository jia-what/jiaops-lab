# Deploy · Jenkins

Jenkins 在 JiaOps Lab 的同一台 CentOS 7 实验机中以 Docker 运行。它使用宿主机 Docker Socket 来构建应用镜像、更新 Compose 栈和执行容器内健康检查。

> 这是单机实验方案。能访问 `/var/run/docker.sock` 的进程等同于拥有宿主机 Docker 管理权限，不应直接用于生产环境。

## 前置条件

- Docker Engine 与 Compose V2 已可用
- 业务 Compose 栈已在 `/opt/jiaops-compose` 运行
- 宿主机 `8081` 未被占用
- Docker 可拉取 `jenkins/jenkins:lts-jdk21` 和 Docker Debian 软件源

## 安装

在实验机执行（Phase 4 开发期间仓库分支为 `phase4`）：

```bash
cd /opt/jiaops-compose
# 旧 Git：git fetch origin phase4 && git merge FETCH_HEAD

cd deploy/jenkins
cp .env.example .env
# 确认 DOCKER_GID（本机：stat -c '%g' /var/run/docker.sock）

df -h /
free -h
ss -lntp | grep -E ':8081[[:space:]]' || true
test -S /var/run/docker.sock && echo "Docker Socket OK"
docker compose up -d --build
docker compose ps
```

首次构建需下载 Jenkins 基础镜像、Docker CLI 与 Compose 插件，时间会比普通容器启动更长。

## 初始化 Jenkins

```bash
cd /opt/jiaops-compose/deploy/jenkins
docker compose exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

浏览器打开 `http://192.168.153.8:8081`：

1. 粘贴初始管理员密码。
2. 选择「Install suggested plugins」。
3. 创建管理员账号；密码保存在密码管理器，不写入仓库。
4. 在「Manage Jenkins」确认系统 URL 为 `http://192.168.153.8:8081/`。
5. 在「Plugins」确认 Pipeline、Git、GitHub、Credentials Binding 已安装。

## 创建流水线任务

1. New Item → Pipeline，任务名 `jiaops-main`。
2. Pipeline definition 选 **Pipeline script from SCM**。
3. SCM 选 Git；仓库 URL：`https://github.com/jia-what/jiaops-lab.git`。
4. Branch Specifier：`*/phase4`（合并 main 后改为 `*/main`）。
5. Script Path：`cicd/Jenkinsfile`。
6. 保存后点击 Build Now。

公开仓库的只读检出不需要凭据。

## 自动触发

- **GitHub Webhook**：`http://192.168.153.8:8081/github-webhook/`。私网地址时 GitHub 通常 `failed to connect to host`。
- **Poll SCM**（本实验采用）：勾选后 Schedule 填 `* * * * *`，远程对应分支有新 commit 即构建。

## 验收与排查

```bash
cd /opt/jiaops-compose/deploy/jenkins
docker compose ps
docker compose logs --tail 100 jenkins

docker exec jiaops-jenkins id
docker exec jiaops-jenkins docker version
docker exec jiaops-jenkins docker compose version
docker exec jiaops-nginx wget -qO- http://127.0.0.1/health
```

- Jenkins 使用 `group_add` + 宿主机 docker 组 GID，而不是以 root 跑进程。
- Pipeline 的 `COMPOSE_FILE` 必须指向 `/opt/jiaops-compose/deploy/compose/docker-compose.yml`。
- `jenkins_home` volume 会保留管理员、插件和任务配置。
