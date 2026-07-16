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
| 访问 | `http://IP/`（:80） | `http://IP:8080/`（默认 `NGINX_HOST_PORT=8080`） |
| MySQL | 宿主机 `mysqld` | 容器 `jiaops-mysql`（数据在 volume `mysql_data`） |
| 端口冲突 | 占 80 / 5000 / 3306 | **不占** 80/3306；只占宿主机 `8080` |

验证通过后再停裸机服务，把 `NGINX_HOST_PORT` 改成 `80` 做切换。

## 启动

```bash
cd /opt/jiaops-lab/deploy/compose   # 或你的仓库路径
cp .env.example .env               # 按需改密码
docker compose up -d --build

docker compose ps
curl -s http://127.0.0.1:8080/health
```

可选 Redis（app 会连 Redis 缓存工单列表，`/health` 含 redis 状态）：

```bash
# .env 中需有 REDIS_HOST=redis（.env.example 已含）
docker compose --profile with-redis up -d --build
curl -s http://127.0.0.1:8080/health
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
- [ ] `curl http://127.0.0.1:8080/health` → `status: ok`
- [ ] 浏览器能建单、改状态
- [ ] 裸机 `:80` 仍可访问（并行阶段）
