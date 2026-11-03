# 太阳风源区小尺度喷流特征的观测研究

> 2026 年大学生创新创业训练计划（编号 2025302163017）
> 武汉大学 地球与空间科学技术学院 · 地球物理学
> 负责人：韩裕祥　成员：杜芊萱、张晋辅　指导教师：吴红红（特聘研究员）
> 起止时间：2026 年 9 月 — 2027 年 8 月

## 这个项目在做什么

用 Solar Orbiter / SDO 的高分辨率极紫外成像，在三个太阳源区（冕洞、活动区边界、宁静区）识别并统计小尺度喷流，
检验「喷流活动是否是慢速太阳风不同种群残余能量差异的物理来源」。

前序工作：Sun et al. 2026, ApJ 997:191（本组），用 PFSS + 弹道回映证明 ASSW 来自活动区、MVAS 来自宁静区。

## 现在到哪一步

启动期（2026 年 11 月）：**锁定三个源区 → 锁定喷流判据 → 跑通端到端流水线**。
三件事没做完之前，不要开始大规模下数据。

## 快速开始

```bash
# 1. 建环境（conda）
conda env create -f environment.yml
conda activate solar-jet

# 2. 校验事件表格式
python scripts/validate_events.py

# 3. 跑一个最小示例
python code/download.py --help
```

## 目录结构

| 路径 | 放什么 | 进 Git 吗 |
|---|---|---|
| `code/` | 处理脚本（下载、预处理、检测、测量） | 进 |
| `scripts/` | 运维与校验脚本 | 进 |
| `events/` | 喷流事件表（CSV）+ 字段定义 | 进 |
| `docs/` | 源区定义、判据手册、命名规范 | 进 |
| `notebooks/` | 探索性分析（只提交结论性 notebook） | 进 |
| `figures/` | 出图（小图可进，大图不进） | 部分 |
| `data/raw/` | 原始 FITS，只读，按 `{源区}/{仪器}/{日期}/` | **不进** |
| `data/interim/` | 中间产物（校准后、裁剪后） | **不进** |
| `data/cubes/` | 数据立方 | **不进** |

## 三条红线

1. **数据不进 Git。** FITS / HDF5 / 压缩包一律被 `.gitignore` 挡住。谁把数据提交上去，仓库会立刻胀到几个 GB。
2. **原始数据只读。** `data/raw/` 下的文件不许改名、不许覆盖、不许在脚本里写回。所有处理结果写到 `data/interim/` 或 `data/cubes/`。
3. **任何数字必须可复现。** 论文里/汇报里的每一张图、每一个统计量，都要能由 `events/jet_events_v0.csv` 加一个脚本重跑出来。做不到的图，不许进汇报。

## 事件表

所有喷流样本记录在 `events/jet_events_v0.csv`，字段定义见 [events/README.md](events/README.md)，
机器可读的字段约束在 `events/schema.json`。

新增或修改事件后，**必须**跑一次：

```bash
python scripts/validate_events.py
```

格式不对就提交，等于给全组埋雷。

## 分工

| 人 | 负责线 | 启动期主交付 |
|---|---|---|
| 韩裕祥 | 检测与机器学习线 + 总体协调 | 仓库与 schema、端到端 demo、检测器 v1 |
| 张晋辅 | 数据工程线 | 三源区数据立方、预处理流水线、质量报告 |
| 杜芊萱 | 科学判据与统计线 | 喷流判据手册、形态分类、双人量测与统计口径 |

## 每周节奏

- 周会 60—90 分钟：每人 5 分钟，只讲「本周交了什么实物 + 卡在哪」。
- 提交信息前缀：`feat:` 新功能 / `fix:` 修 bug / `docs:` 文档 / `data:` 事件表或数据清单 / `chore:` 杂项。
- 分支：`main` 保持可运行；个人干活开 `dev-姓名`，完成后提 PR 合回。

## 相关文档

- [docs/源区定义表.csv](docs/源区定义表.csv) — 三个源区的坐标、窗口、归属
- [docs/喷流判据与测量手册-模板.md](docs/喷流判据与测量手册-模板.md) — 判据与公式（杜芊萱主笔）
- [docs/数据目录与命名规范.md](docs/数据目录与命名规范.md) — 目录与文件命名

## 引用

```bibtex
@ARTICLE{Sun2026,
  author  = {{Sun}, Z. and {Wu}, H. and {Huang}, S. and {He}, J. and {Tian}, H. and
             {Yang}, L. and {Badman}, S. T. and {Yuan}, Z. and {Chen}, Y. and {Hou}, C.},
  title   = {{Distinct Source Regions for Slow Solar Wind Populations
             Differentiated by Residual Energy during Parker Solar Probe Encounter 7}},
  journal = {The Astrophysical Journal},
  year    = {2026},
  volume  = {997},
  pages   = {191},
  doi     = {10.3847/1538-4357/ae21b7}
}
```
