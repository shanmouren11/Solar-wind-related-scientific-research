# -*- coding: utf-8 -*-
"""数据下载骨架。

当前状态：只搭好参数与目录，真正的检索需装好 sunpy / sunpy-soar 后补全。
用法：
    python code/download.py --region R1_CH --instrument SDO_AIA --date 2021-01-10
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.config import REGIONS, INSTRUMENTS, raw_dir  # noqa: E402


def build_query(region, instrument, date):
    """返回 sunpy.net.Fido 的检索结果（延迟导入，避免没装 sunpy 就跑不起来）。"""
    try:
        from sunpy.net import Fido, attrs as a
    except ImportError:
        raise SystemExit("未安装 sunpy。请先 conda env create -f environment.yml")

    from astropy import units as u

    if instrument == "EUI_HRIEUV":
        try:
            import sunpy_soar  # noqa: F401  注册 SOAR client
        except ImportError:
            raise SystemExit("未安装 sunpy-soar，无法检索 Solar Orbiter 数据")
        q = Fido.search(
            a.Time(date, date + " 23:59:59"),
            a.Instrument("EUI"),
            a.Wavelength(174 * u.angstrom),
        )
    elif instrument == "SDO_AIA":
        q = Fido.search(
            a.Time(date, date + " 23:59:59"),
            a.Instrument("AIA"),
            a.Wavelength(193 * u.angstrom),
        )
    else:
        raise SystemExit("尚未实现: %s（先做 EUI 与 AIA）" % instrument)

    print("检索完成，命中 %d 条记录" % len(q))
    out = raw_dir(region, instrument, date)
    os.makedirs(out, exist_ok=True)
    Fido.fetch(q, path=os.path.join(out, "{file}"))
    print("已下载到", out)


def main():
    ap = argparse.ArgumentParser(description="按源区/仪器/日期下载观测数据")
    ap.add_argument("--region", required=True, choices=sorted(REGIONS))
    ap.add_argument("--instrument", required=True, choices=sorted(INSTRUMENTS))
    ap.add_argument("--date", required=True, help="UTC 日期，YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不下载")
    args = ap.parse_args()

    out = raw_dir(args.region, args.instrument, args.date)
    print("[计划] 源区=%s(%s)  仪器=%s  日期=%s" % (
        args.region, REGIONS[args.region]["name"], args.instrument, args.date))
    print("[计划] 输出目录 =", out)
    if args.dry_run:
        print("[dry-run] 未执行下载")
        return
    build_query(args.region, args.instrument, args.date)


if __name__ == "__main__":
    main()
