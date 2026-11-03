# -*- coding: utf-8 -*-
"""校验事件表是否符合 events/schema.json。

用法：
    python scripts/validate_events.py                 # 校验主表
    python scripts/validate_events.py --file events/jet_events_example.csv

退出码：0 全部通过；1 有错误。CI 会跑这个脚本，所以格式错了 PR 过不去。
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "events", "schema.json")
DEFAULT_CSV = os.path.join(ROOT, "events", "jet_events_v0.csv")


def parse_time(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return datetime.fromisoformat(s)


def load_schema():
    with open(SCHEMA, encoding="utf-8") as f:
        return json.load(f)


def validate(path):
    schema = load_schema()
    cols = schema["columns"]
    names = [c["name"] for c in cols]
    errors = []

    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [u"文件是空的"], 0
        missing = [n for n in names if n not in reader.fieldnames]
        extra = [n for n in reader.fieldnames if n not in names]
        if missing:
            errors.append(u"缺少列: " + ", ".join(missing))
        if extra:
            errors.append(u"多出未知列: " + ", ".join(extra) + u"（改列名请先更新 schema.json）")
        rows = list(reader)

    seen = set()
    for i, row in enumerate(rows, start=2):
        for c in cols:
            n = c["name"]
            v = (row.get(n) or "").strip()
            if not v:
                if c.get("required"):
                    errors.append(u"第 %d 行：%s 为必填但为空" % (i, n))
                continue
            t = c["type"]
            if t == "enum":
                if v not in c.get("enum", []):
                    errors.append(u"第 %d 行：%s='%s' 不在允许值 %s" % (i, n, v, c.get("enum")))
            elif t in ("float", "int"):
                try:
                    x = float(v)
                except ValueError:
                    errors.append(u"第 %d 行：%s='%s' 不是数字" % (i, n, v))
                    continue
                if c.get("min") is not None and x < c["min"]:
                    errors.append(u"第 %d 行：%s=%s 小于 %s" % (i, n, x, c["min"]))
                if c.get("max") is not None and x > c["max"]:
                    errors.append(u"第 %d 行：%s=%s 大于 %s" % (i, n, x, c["max"]))
            elif t == "iso8601":
                try:
                    parse_time(v)
                except Exception:
                    errors.append(u"第 %d 行：%s='%s' 不是 ISO 8601 时间（例 2021-01-12T13:04:20Z）" % (i, n, v))
            elif c.get("pattern"):
                if not re.match(c["pattern"], v):
                    errors.append(u"第 %d 行：%s='%s' 不符合格式 %s" % (i, n, v, c["pattern"]))

        s = (row.get("date_obs_start") or "").strip()
        e = (row.get("date_obs_end") or "").strip()
        if s and e:
            try:
                if parse_time(e) < parse_time(s):
                    errors.append(u"第 %d 行：结束时间早于开始时间" % i)
            except Exception:
                pass

        reg = (row.get("source_region") or "").strip()
        rt = (row.get("region_type") or "").strip()
        m = schema.get("region_to_type", {})
        if reg in m and rt and rt != m[reg]:
            errors.append(u"第 %d 行：source_region=%s 应对应 region_type=%s，但填了 %s" % (i, reg, m[reg], rt))

        rid = (row.get("event_id") or "").strip().upper()
        if rid:
            if rid in seen:
                errors.append(u"第 %d 行：event_id '%s' 重复" % (i, rid))
            seen.add(rid)

    return errors, len(rows)


def main():
    ap = argparse.ArgumentParser(description="校验喷流事件表格式")
    ap.add_argument("--file", default=DEFAULT_CSV)
    args = ap.parse_args()
    if not os.path.exists(args.file):
        print(u"找不到文件: " + args.file)
        return 1
    errors, n = validate(args.file)
    if errors:
        print(u"校验未通过（%d 个问题）：" % len(errors))
        for e in errors[:40]:
            print("  - " + e)
        if len(errors) > 40:
            print(u"  ... 还有 %d 个" % (len(errors) - 40))
        return 1
    print(u"校验通过：%d 行，%s" % (n, os.path.basename(args.file)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
