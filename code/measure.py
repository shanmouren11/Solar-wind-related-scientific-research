# -*- coding: utf-8 -*-
"""参数测量：把候选事件量成事件表里的一行。

与 docs/喷流判据与测量手册 一一对应，手册改了这里必须跟着改。
"""
import argparse


def measure_width(cube, event):
    """半高全宽 -> width_km。TODO: 与手册第 3 节一致。"""
    raise NotImplementedError


def measure_lifetime(cube, event, threshold):
    raise NotImplementedError


def measure_velocity(td_map, event):
    """时间-距离图斜率 -> v_km_s。"""
    raise NotImplementedError


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", default="events/jet_events_v0.csv")
    ap.add_argument("--fill-missing", action="store_true", help="只补空着的列")
    ap.parse_args()
    print("TODO")


if __name__ == "__main__":
    main()
