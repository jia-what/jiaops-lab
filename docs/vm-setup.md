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
| Docker | 未安装（第二阶段再装） |
| firewalld | 未处于 active（记录为 unknown/inactive） |
| SELinux | Permissive |

## 结论

虚拟机适合作为 JiaOps Lab 实验机：资源够用、网络与 DNS 正常、工具齐全。  
下一阶段再安装 Docker；当前继续完成 Linux 第一阶段笔记入库即可。

## 复跑基线

```bash
bash ~/jiaops-lab/scripts/vm_baseline_check.sh
```

## 注意

CentOS 7 已 EOL，学习阶段可用；正式对外服务时优先考虑 Rocky / Alma / 云厂商 Linux。
