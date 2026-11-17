# -*- coding: utf-8 -*-
"""报时鸟 总指挥（Agent）：把 规划器 + 调度器 串起来。"""
from planner import Planner
from scheduler import Scheduler


class Agent:
    def __init__(self):
        self.scheduler = Scheduler()
        self.planner = Planner(self.scheduler)

    def chat(self, text):
        return self.planner.respond(text)


if __name__ == "__main__":
    agent = Agent()
    for q in ["我叫刘浩彬", "我是谁", "提醒我 交软工作业 22:00"]:
        print("用户:", q)
        print("报时鸟:", agent.chat(q))
    print("扫描到期提醒…")
    agent.scheduler.tick()
