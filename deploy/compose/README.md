# Deploy · Docker Compose

一键拉起：`nginx` → `app` → `mysql`（可选 `redis`）。

## 文件

| 文件 | 作用 |
|------|------|
| `docker-compose.yml` | 编排定义 |
| `.env.example` | 环境变量模板 → 复制为 `.env` |
| `../nginx/jiaops-docker.conf` | 容器内 Nginx 反代（upstream=`app:5000`） |
| `../../app/Dockerfile` | 工单应用镜像 |
| `../../app/schema.sql` | MySQL 首次初始化建表 |

## 与裸机 Phase 2 的关系

| | 裸机 MVP | Compose 栈 |
|--|----------|------------|
| 访问 | `http://IP/`（:80） | 正式运行也是 `http://IP/`（容器 Nginx 接管 :80） |
| MySQL | 宿主机 `mysqld` | 容器 `jiaops-mysql`（数据在 volume `mysql_data`） |
| 端口冲突 | 占 80 / 5000 / 3306 | **不占** 80/3306；只占宿主机 `8080` |

并行验证阶段可把 `NGINX_HOST_PORT` 设为 `8080`；当前正式运行已设为 `80`。

## 启动

```bash
cd /opt/jiaops-lab/deploy/compose   # 或你的仓库路径
cp .env.example .env               # 按需改密码
docker compose up -d --build

docker compose ps
curl -s http://127.0.0.1/health
```

可选 Redis（app 会连 Redis 缓存工单列表，`/health` 含 redis 状态）：

```bash
# .env 中需有 REDIS_HOST=redis（.env.example 已含）
docker compose --profile with-redis up -d --build
curl -s http://127.0.0.1/health
# 期望：{"status":"ok","db":1,"redis":"ok",...}
```

## 常用命令

```bash
docker compose logs -f
docker compose logs -f app
docker compose restart app
docker compose down          # 停栈，保留 volume
docker compose down -v       # 停栈并删数据（慎用）
```

## 验收

- [ ] `docker compose ps` 中 mysql / app / nginx 为 healthy 或 running
- [ ] `curl http://127.0.0.1/health` → `status: ok`
- [ ] 浏览器能建单、改状态
- [ ] 容器 Nginx 已监听宿主机 `:80`

## Jenkins 部署使用的镜像 tag

默认应用镜像是 `jiaops-app:local`。Jenkins Pipeline 构建时会设置 `APP_TAG=build-<构建号>-<Git SHA>`，Compose 因而使用对应的本地镜像：

```bash
APP_TAG=build-12-a1b2c3d docker compose --profile with-redis up -d --no-build
```

正式运行时的密码和端口仍来自本目录 `.env`，不要把它提交到 Git。
