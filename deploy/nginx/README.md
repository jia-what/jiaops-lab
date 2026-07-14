# Deploy · Nginx

## 文件

| 文件 | 用途 |
|------|------|
| `jiaops.conf` | **裸机 Phase 2**：复制到 `/etc/nginx/conf.d/jiaops.conf`，反代 `127.0.0.1:5000` |
| `jiaops-docker.conf` | **Compose Phase 3**：挂载为容器 `default.conf`，反代 `app:5000` |

## 裸机操作摘要

```bash
nginx -t
systemctl reload nginx
curl -I http://127.0.0.1/
curl -I http://192.168.153.8/
```

浏览器：`http://192.168.153.8/`（不必写 :5000）

## Compose

见 `deploy/compose/README.md`。默认对外 `http://IP:8080/`。
