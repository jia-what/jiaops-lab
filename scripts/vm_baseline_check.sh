#!/usr/bin/env bash
# CentOS 虚拟机基线信息采集（只读，不改系统）
set -euo pipefail

echo "===== JiaOps Lab · VM Baseline ====="
echo "Time: $(date)"
echo

echo "----- Host -----"
hostnamectl 2>/dev/null || hostname
echo

echo "----- OS -----"
cat /etc/os-release 2>/dev/null || cat /etc/redhat-release
echo

echo "----- CPU / Memory / Disk -----"
nproc
free -h
df -hT
echo

echo "----- Network -----"
ip -br a 2>/dev/null || ifconfig
echo
echo "Default route:"
ip route 2>/dev/null | head -n 5 || route -n | head -n 5
echo

echo "----- DNS -----"
cat /etc/resolv.conf 2>/dev/null || true
echo

echo "----- Connectivity -----"
ping -c 2 -W 2 8.8.8.8 >/dev/null 2>&1 && echo "ICMP to 8.8.8.8: OK" || echo "ICMP to 8.8.8.8: FAIL"
getent hosts github.com >/dev/null 2>&1 && echo "DNS github.com: OK" || echo "DNS github.com: FAIL"
echo

echo "----- Common tools -----"
for cmd in bash vim git curl wget ss systemctl docker; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[OK] $cmd"
  else
    echo "[--] $cmd (not found)"
  fi
done
echo

echo "----- Firewall / SELinux -----"
systemctl is-active firewalld 2>/dev/null || echo "firewalld: unknown/inactive"
getenforce 2>/dev/null || echo "SELinux: not available"
echo

echo "===== Done ====="
