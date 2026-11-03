# -*- coding: utf-8 -*-
"""全局常量：路径、源区、仪器、事件编号规则。

改这里的任何值，必须同步改 docs/ 下对应的说明文档。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(ROOT, "data", "raw")
DATA_INTERIM = os.path.join(ROOT, "data", "interim")
DATA_CUBES = os.path.join(ROOT, "data", "cubes")
FIGURES = os.path.join(ROOT, "figures")
EVENTS_CSV = os.path.join(ROOT, "events", "jet_events_v0.csv")
SCHEMA_JSON = os.path.join(ROOT, "events", "schema.json")

# 三个源区：坐标取自 Sun et al. 2026 (ApJ 997:191) 图 5 / 图 7
REGIONS = {
    "R1_CH": {"type": "CH", "lon": [50, 100],  "lat": [10, 45],  "wind": "FSW",  "name": "冕洞"},
    "R2_AR": {"type": "AR", "lon": [60, 135],  "lat": [-50, 10], "wind": "ASSW", "name": "活动区 AR 12796 西侧"},
    "R3_QS": {"type": "QS", "lon": [120, 170], "lat": [10, 50],  "wind": "MVAS", "name": "宁静区"},
}

INSTRUMENTS = {
    "EUI_HRIEUV": {"wavelength_A": 174.0, "desc": "Solar Orbiter / EUI 高分辨 174 A"},
    "SDO_AIA":    {"wavelength_A": 193.0, "desc": "SDO/AIA 193 A（另有 171/304/94）"},
    "HINODE_EIS": {"wavelength_A": 195.12, "desc": "Hinode/EIS Fe XII 195.12 A 光谱"},
    "IRIS":       {"wavelength_A": None,  "desc": "IRIS 色球-过渡区光谱"},
}

PREFIX_BY_REGION = {"R1_CH": "R1", "R2_AR": "R2", "R3_QS": "R3", "UNK": "UNK"}


def make_event_id(region, seq):
    """生成事件编号，例：make_event_id('R1_CH', 7) -> 'R1-0007'。"""
    region = region.upper()
    if region not in PREFIX_BY_REGION:
        raise ValueError("未知源区: %s（可选 %s）" % (region, list(PREFIX_BY_REGION)))
    if not isinstance(seq, int) or seq < 1:
        raise ValueError("序号必须是正整数")
    return "%s-%04d" % (PREFIX_BY_REGION[region], seq)


def raw_dir(region, instrument, date):
    """原始数据目录：data/raw/{region}/{instrument}/{date}/"""
    return os.path.join(DATA_RAW, region, instrument, date)


def cube_path(region):
    """数据立方路径：data/cubes/{region}/"""
    return os.path.join(DATA_CUBES, region)
