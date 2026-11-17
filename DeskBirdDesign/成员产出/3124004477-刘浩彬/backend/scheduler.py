# -*- coding: utf-8 -*-
"""报时鸟 提醒调度器（核心）：存 SQLite、定时扫描、到点触发、周期提醒。"""
import sqlite3
import datetime


class Scheduler:
    def __init__(self, db="deskbird.db"):
        self.db = db
        conn = sqlite3.connect(db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminder (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                remind_at TEXT NOT NULL,
                repeat_type TEXT NOT NULL DEFAULT 'once',
                repeat_interval INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        """)
        conn.commit()
        conn.close()

    def add_reminder(self, content, remind_at, repeat_type="once", repeat_interval=0):
        conn = sqlite3.connect(self.db)
        conn.execute(
            "INSERT INTO reminder(content, remind_at, repeat_type, repeat_interval, status) VALUES(?,?,?,?,?)",
            (content, remind_at, repeat_type, repeat_interval, "pending"),
        )
        conn.commit()
        conn.close()

    def check_due(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect(self.db)
        rows = conn.execute(
            "SELECT id, content, remind_at, repeat_type, repeat_interval "
            "FROM reminder WHERE remind_at <= ? AND status = 'pending'",
            (now,),
        ).fetchall()
        conn.close()
        return rows

    def mark_done(self, rid):
        conn = sqlite3.connect(self.db)
        conn.execute("UPDATE reminder SET status = 'done' WHERE id = ?", (rid,))
        conn.commit()
        conn.close()

    def _next_time(self, remind_at, repeat_type, interval):
        dt = datetime.datetime.strptime(remind_at, "%Y-%m-%d %H:%M")
        if repeat_type == "daily":
            dt += datetime.timedelta(days=1)
        elif repeat_type == "interval":
            dt += datetime.timedelta(minutes=interval or 45)
        return dt.strftime("%Y-%m-%d %H:%M")

    def _update_time(self, rid, next_at):
        conn = sqlite3.connect(self.db)
        conn.execute("UPDATE reminder SET remind_at = ? WHERE id = ?", (next_at, rid))
        conn.commit()
        conn.close()

    def tick(self):
        """每 5 秒调用一次：触发到期提醒，周期提醒自动排下一次。"""
        for rid, content, remind_at, repeat_type, interval in self.check_due():
            print("[到点提醒] %s（计划于 %s）" % (content, remind_at))
            if repeat_type == "once":
                self.mark_done(rid)
            else:
                self._update_time(rid, self._next_time(remind_at, repeat_type, interval))
