# -*- coding: utf-8 -*-
"""预处理骨架：校准 -> 去尖峰 -> 对齐 -> 裁剪。

顺序不能乱：先去尖峰再对齐，否则尖峰会污染互相关。
用法：
    python code/preprocess.py --region R1_CH --date 2021-01-10
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.config import REGIONS, raw_dir, DATA_INTERIM  # noqa: E402


def despike(frames):
    """去宇宙线尖峰（TODO：3x3 中值滤波 + sigma 阈值，或 eui_cal 官方流程）。"""
    raise NotImplementedError("TODO: 张晋辅负责，第 2—3 周完成")


def align(frames, reference_time):
    """差分旋转对齐到参考时刻（TODO：sunpy DifferentialRotate）。"""
    raise NotImplementedError("TODO")


def crop(frames, region):
    """裁剪到源区视场（TODO：用 REGIONS 里的经纬度换算成视场中心与大小）。"""
    raise NotImplementedError("TODO")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--region", required=True, choices=sorted(REGIONS))
    ap.add_argument("--date", required=True)
    args = ap.parse_args()
    src = raw_dir(args.region, "EUI_HRIEUV", args.date)
    dst = os.path.join(DATA_INTERIM, args.region, args.date)
    print("输入:", src)
    print("输出:", dst)
    print("TODO: 按 despike -> align -> crop 顺序实现，每步落一个文件")


if __name__ == "__main__":
    main()
