# systemd 托管工单应用

把 Flask 从「手动 `python app.py`」变成系统服务：开机自启、挂了可重启、日志进 journald。

## 文件

- `jiaops.service` → 复制到 `/etc/systemd/system/jiaops.service`

## 操作摘要

```bash
# 若前台还在跑 python app.py，先 Ctrl+C 停掉
sudo cp deploy/systemd/jiaops.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jiaops
sudo systemctl status jiaops
curl http://127.0.0.1:5000/health
```

常用：

```bash
systemctl stop jiaops
systemctl start jiaops
systemctl restart jiaops
journalctl -u jiaops -f
```
