# Deploy · Nginx

当前阶段：把 80 端口流量反代到本机 Flask（`127.0.0.1:5000`）。

## 文件

- `jiaops.conf` → 复制到虚拟机 `/etc/nginx/conf.d/jiaops.conf`

## 操作摘要

```bash
nginx -t
systemctl reload nginx
curl -I http://127.0.0.1/
curl -I http://192.168.153.8/
```

浏览器访问：`http://192.168.153.8/`（不必再写 :5000）
