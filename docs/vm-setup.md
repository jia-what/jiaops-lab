# 虚拟机环境

## 当前设备

| 项 | 值 |
|----|-----|
| 系统 | CentOS 7 |
| 资源 | 4 核 / 8G 内存 / 40G 磁盘 |
| 连接 | MobaXterm（SSH） |

## 基线检查清单（下一步要做）

在虚拟机上执行并记录结果：

- [ ] 主机名、时区、时间同步
- [ ] 网络连通（能否访问外网 / DNS）
- [ ] 磁盘与内存余量
- [ ] SSH 密钥登录是否可用
- [ ] 基础工具：`vim` `git` `curl` `wget` `net-tools`
- [ ] 防火墙 / SELinux 当前状态（先记录，后按需调整）

可使用仓库脚本（后续补充）：

```bash
bash scripts/vm_baseline_check.sh
```

## 注意

CentOS 7 已 EOL，学习阶段可用；正式对外服务时优先考虑 Rocky / Alma / 云厂商 Linux。
