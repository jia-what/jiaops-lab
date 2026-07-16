import json
import os
from datetime import datetime

import pymysql
import redis
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)

PRIORITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "in_progress", "resolved", "closed")
TICKETS_CACHE_KEY = "jiaops:tickets:list"
TICKETS_CACHE_TTL = 30


def get_db():
    """每次请求新建连接，MVP 够用；以后可换成连接池。"""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "jiaops"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "jiaops"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def get_redis():
    """REDIS_HOST 为空时不连 Redis（裸机 / 未启 redis profile 时兼容）。"""
    host = (os.getenv("REDIS_HOST") or "").strip()
    if not host:
        return None
    return redis.Redis(
        host=host,
        port=int(os.getenv("REDIS_PORT", "6379")),
        decode_responses=True,
        socket_connect_timeout=2,
    )


def redis_status():
    client = get_redis()
    if client is None:
        return "skipped"
    try:
        client.ping()
        return "ok"
    except Exception as exc:
        return f"error: {exc}"


def invalidate_tickets_cache():
    client = get_redis()
    if client is None:
        return
    try:
        client.delete(TICKETS_CACHE_KEY)
    except Exception:
        pass


def fetch_tickets_from_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, title, description, priority, status, created_at, updated_at
            FROM tickets
            ORDER BY id DESC
            """
        )
        tickets = cur.fetchall()
    conn.close()
    return tickets


def fetch_tickets():
    """有 Redis 时缓存工单列表 30 秒；建单/改状态后会删缓存。"""
    client = get_redis()
    if client is not None:
        try:
            cached = client.get(TICKETS_CACHE_KEY)
            if cached:
                return json.loads(cached)
        except Exception:
            pass

    tickets = fetch_tickets_from_db()

    if client is not None:
        try:
            client.setex(
                TICKETS_CACHE_KEY,
                TICKETS_CACHE_TTL,
                json.dumps(tickets, default=str),
            )
        except Exception:
            pass

    return tickets


@app.get("/health")
def health():
    """给以后监控 / Nginx / Compose 探活用。"""
    body = {"time": datetime.now().isoformat()}
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        conn.close()
        body["db"] = row["ok"]
    except Exception as exc:
        body["status"] = "error"
        body["detail"] = str(exc)
        return body, 500

    body["redis"] = redis_status()
    if body["redis"].startswith("error"):
        body["status"] = "error"
        return body, 500

    body["status"] = "ok"
    return body, 200


@app.get("/")
def index():
    tickets = fetch_tickets()
    return render_template(
        "index.html",
        tickets=tickets,
        priorities=PRIORITIES,
        statuses=STATUSES,
    )


@app.post("/tickets")
def create_ticket():
    title = (request.form.get("title") or "").strip()
    description = (request.form.get("description") or "").strip()
    priority = request.form.get("priority") or "medium"

    if not title:
        return "title is required", 400
    if priority not in PRIORITIES:
        return "invalid priority", 400

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO tickets (title, description, priority, status)
            VALUES (%s, %s, %s, 'open')
            """,
            (title, description, priority),
        )
    conn.close()
    invalidate_tickets_cache()
    return redirect(url_for("index"))


@app.post("/tickets/<int:ticket_id>/status")
def update_status(ticket_id):
    status = request.form.get("status")
    if status not in STATUSES:
        return "invalid status", 400

    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tickets SET status=%s WHERE id=%s",
            (status, ticket_id),
        )
    conn.close()
    invalidate_tickets_cache()
    return redirect(url_for("index"))


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
