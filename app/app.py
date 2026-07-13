import os
from datetime import datetime

import pymysql
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for

load_dotenv()

app = Flask(__name__)

PRIORITIES = ("low", "medium", "high", "critical")
STATUSES = ("open", "in_progress", "resolved", "closed")


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


@app.get("/health")
def health():
    """给以后监控 / Nginx / Compose 探活用。"""
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        conn.close()
        return {"status": "ok", "db": row["ok"], "time": datetime.now().isoformat()}, 200
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}, 500


@app.get("/")
def index():
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
    return redirect(url_for("index"))


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
