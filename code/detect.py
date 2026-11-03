# -*- coding: utf-8 -*-
"""检测器 v1（传统方法）：差分图 + 时间-距离图亮脊检测。

思路（按顺序实现，每步单独可测）：
  1. 差分增强：running difference / base-difference
  2. 沿径向做时间-距离图（slit 固定，时间做纵轴）
  3. 亮脊检测：阈值 + 连通域 + 形态筛选（细长、沿径向）
  4. 输出候选事件 CSV（先不判形态，只给位置与时刻）
"""
import argparse
import sys


def running_difference(cube):
    raise NotImplementedError("TODO: 韩裕祥，第 3—4 周")


def make_time_distance(cube, slit):
    raise NotImplementedError("TODO")


def find_ridges(td_map, threshold_sigma=3.0):
    raise NotImplementedError("TODO")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True)
    ap.add_argument("--threshold", type=float, default=3.0, help="相对背景的 sigma 倍数")
    ap.parse_args()
    print("TODO: 输出 events/candidates_{region}.csv")


if __name__ == "__main__":
    main()
