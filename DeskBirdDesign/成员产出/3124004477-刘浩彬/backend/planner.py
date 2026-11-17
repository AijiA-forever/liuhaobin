# -*- coding: utf-8 -*-
"""报时鸟 意图规划器：区分 记忆 / 询问身份 / 提醒 三类意图。"""
import re
import datetime


class Planner:
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.memory = {}

    def respond(self, text):
        t = (text or "").strip()
        m = re.search(r"我叫\s*([^\s，,。！!]+)", t)
        if m:
            self.memory["name"] = m.group(1)
            return "记住了，你叫%s。" % m.group(1)
        if re.search(r"我是谁|我叫什么|我的名字", t):
            return ("你叫%s。" % self.memory["name"]) if "name" in self.memory else "你还没告诉我你的名字。"
        m = re.search(r"提醒我\s*(.+?)\s*(\d{1,2}:\d{2})", t)
        if m:
            content, tm = m.group(1).strip(), m.group(2)
            day = datetime.date.today().isoformat()
            self.scheduler.add_reminder(content, "%s %s" % (day, tm))
            return "已记下提醒：%s（%s）" % (content, tm)
        if re.search(r"提醒我|记一下", t):
            return "请带上时间，例如：提醒我 交软工作业 22:00"
        return "我暂时没听懂，可以试试“我叫X”“我是谁”“提醒我 交软工作业 22:00”。"
