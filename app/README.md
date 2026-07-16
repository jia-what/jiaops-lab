# 运维工单应用（MVP）

最小功能：创建工单、列表、改状态；数据存 MySQL；提供 `/health`。

## 结构

```text
app/
├── app.py              # Flask 主程序
├── Dockerfile          # 容器镜像（Phase 3）
├── .dockerignore
├── requirements.txt    # 依赖
├── .env.example        # 环境变量模板
├── .env                # 本地密钥（勿提交）
├── schema.sql          # 建表（Compose 首次初始化也会挂载）
└── templates/
    └── index.html      # 简单页面
```

容器运行见仓库根目录 README 与 `deploy/compose/README.md`。
## 在 CentOS 上运行

```bash
cd /opt/jiaops-lab
source .venv/bin/activate   # 若 venv 不在此目录，先进入正确 venv

# 放入代码后：
cd /opt/jiaops-lab/app      # 或你放置 app.py 的目录
cp .env.example .env        # 按需改密码
pip install -r requirements.txt
python app.py
```

访问：

- 本机：`http://127.0.0.1:5000/`
- 局域网：`http://192.168.153.8:5000/`
- 健康检查：`http://192.168.153.8:5000/health`

## 接口一览

| 方法 | 路径 | 作用 |
|------|------|------|
| GET | `/health` | 健康检查（含数据库） |
| GET | `/` | 工单页 |
| POST | `/tickets` | 创建工单 |
| POST | `/tickets/<id>/status` | 更新状态 |
