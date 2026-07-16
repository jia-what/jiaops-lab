# 虚拟机环境

## 当前设备

| 项 | 值 |
|----|-----|
| 主机名 | `jiawhat` |
| 系统 | CentOS Linux 7 (Core) |
| 内核 | `3.10.0-1160.71.1.el7.x86_64` |
| 虚拟化 | VMware |
| 资源 | 4 核 / 7.6G 内存 / 根分区约 35G |
| IP | `192.168.153.8/24`（网卡 `ens33`） |
| 网关 | `192.168.153.2` |
| DNS | `223.5.5.5` / `114.114.114.114` |
| 连接 | MobaXterm（SSH，`root`） |

## 基线检查结果（2026-07-11）

脚本：`scripts/vm_baseline_check.sh`

| 检查项 | 结果 |
|--------|------|
| 主机名 / 时区 | `jiawhat`，CST，时间正常 |
| 外网 ICMP | OK（8.8.8.8） |
| DNS（github.com） | OK |
| 内存 | 可用约 7.1G，充足 |
| 磁盘 `/` | 已用 6%（1.9G / 35G），充足 |
| Swap | 4G，未使用 |
| 基础工具 | bash / vim / git / curl / wget / ss / systemctl 均有 |
| Docker | 未安装（当时）→ **2026-07-14 已装** Engine 26.1.4 + Compose v2.27.1 |
| firewalld | 未处于 active（记录为 unknown/inactive） |
| SELinux | Permissive |

## 结论

虚拟机适合作为 JiaOps Lab 实验机：资源够用、网络与 DNS 正常、工具齐全。  
Docker 已安装并配置镜像加速；下一步用 Compose 一键部署（见 `deploy/compose/`）。

## 复跑基线

```bash
bash ~/jiaops-lab/scripts/vm_baseline_check.sh
# 或：bash /opt/jiaops-lab/scripts/vm_baseline_check.sh
```

## Docker 备注（2026-07-14）

- 镜像加速：`/etc/docker/daemon.json`（DaoCloud 等）
- 裸机 MVP 与 Docker **并存**：Compose 验证用宿主机端口 `8080`
- 安装笔记见 Obsidian：`02 Learning/Docker/安装Docker.md`

## 注意

CentOS 7 已 EOL，学习阶段可用；正式对外服务时优先考虑 Rocky / Alma / 云厂商 Linux。