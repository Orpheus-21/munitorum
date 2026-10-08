#!/usr/bin/env python3
"""Production planner for Call of War: tell when a build order is ready."""
import json
import sys
from datetime import datetime, timedelta


def plan(units, stock, income, sites, orders):
    """Return the need, the wait per resource, and the build time of an order list."""
    need = {}
    build_s = 0
    for name, count in orders.items():
        u = units[name]
        for res, amount in u["cost"].items():
            need[res] = need.get(res, 0) + amount * count
        build_s += u["build_seconds"] * count
    wait_h = {}
    for res, amount in need.items():
        deficit = max(0, amount - stock.get(res, 0))
        rate = income.get(res, 0)
        wait_h[res] = 0 if deficit == 0 else (deficit / rate if rate > 0 else float("inf"))
    return need, wait_h, build_s / sites


def report(units, p, now):
    need, wait_h, build_s = plan(units, p["stock"], p["income_per_hour"], p["sites"], p["orders"])
    lines = ["Resource   need   have   wait (h)"]
    for res, amount in need.items():
        lines.append(f"{res:<10} {amount:>5} {p['stock'].get(res, 0):>6} {wait_h[res]:>10.2f}")
    worst = max(wait_h, key=wait_h.get)
    if wait_h[worst] == float("inf"):
        lines.append(f"Stop: {worst} has no income. The order can not finish.")
        return "\n".join(lines)
    start = now + timedelta(hours=wait_h[worst])
    done = start + timedelta(seconds=build_s)
    lines.append(f"Bottleneck: {worst}" if wait_h[worst] > 0 else "Bottleneck: none")
    lines.append(f"Start: {start:%a %H:%M}")
    lines.append(f"Done:  {done:%a %H:%M}")
    return "\n".join(lines)


def self_check():
    units = {"inf": {"cost": {"money": 10, "food": 5}, "build_seconds": 60}}
    need, wait_h, build_s = plan(units, {"money": 20, "food": 0}, {"money": 10, "food": 5}, 2, {"inf": 4})
    assert need == {"money": 40, "food": 20}
    assert wait_h == {"money": 2.0, "food": 4.0}
    assert build_s == 120
    assert plan(units, {}, {}, 1, {"inf": 1})[1]["money"] == float("inf")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--check":
        self_check()
        print("ok")
        sys.exit()
    if len(sys.argv) != 3:
        sys.exit("Usage: planner.py UNITS.json PLAN.json | planner.py --check")
    units = json.load(open(sys.argv[1]))
    p = json.load(open(sys.argv[2]))
    print(report(units, p, datetime.now()))
