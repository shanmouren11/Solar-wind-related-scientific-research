# 事件表（喷流样本库）

- 主表：[jet_events_v0.csv](jet_events_v0.csv)
- 字段约束：[schema.json](schema.json)（机器可读，校验脚本读它）
- 示例：[jet_events_example.csv](jet_events_example.csv)（**不是真数据**，看完就删）

## 怎么加一条事件

1. 在 `jet_events_v0.csv` 末尾加一行，列数必须与表头一致。
2. `event_id` 用「源区前缀-4 位序号」，例：`R1-0001`。同一前缀不许重复。
3. 时间一律 UTC + ISO 8601，结尾带 `Z`，例：`2021-01-12T13:04:20Z`。**不许写成本地时间。**
4. 量不了的列**留空**，不要填 0、不要填 -999。
5. 提交前跑：`python scripts/validate_events.py`

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `event_id` | str | 是 | `R1/R2/R3/UNK` + `-` + 4 位序号 |
| `source_region` | 枚举 | 是 | `R1_CH` / `R2_AR` / `R3_QS` / `UNK` |
| `region_type` | 枚举 | 是 | `CH` / `AR` / `QS` / `BOUNDARY` / `UNK` |
| `instrument` | 枚举 | 是 | `EUI_HRIEUV` / `SDO_AIA` / `HINODE_EIS` / `IRIS` / `OTHER` |
| `wavelength_A` | float | 是 | 观测波长，单位埃（174 / 193 …） |
| `date_obs_start` | 时间 | 是 | 事件起始，UTC |
| `date_obs_end` | 时间 | 是 | 事件结束，UTC，必须晚于起始 |
| `x_arcsec` / `y_arcsec` | float | 否 | 日面投影坐标 |
| `cr_lon_deg` / `cr_lat_deg` | float | 否 | Carrington 经纬度，做回映后填 |
| `width_km` | float | 否 | 宽度，半高全宽 |
| `length_km` | float | 否 | 长度 |
| `lifetime_s` | float | 否 | 寿命 |
| `v_km_s` | float | 否 | 速度 |
| `accel_km_s2` | float | 否 | 加速度 |
| `peak_intensity` | float | 否 | 相对背景的峰值增强 |
| `morphology_class` | 枚举 | 是 | `single` / `multi` / `loop` / `point` / `unknown` |
| `energy_erg` | float | 否 | 估计能量 |
| `confidence` | float | 否 | 0—1，人工置信度 |
| `measured_by` | str | 是 | 谁量的 |
| `reviewed_by` | str | 否 | 谁复核的 |
| `note` | str | 否 | 备注（含逗号时整格加双引号） |

## 两条约定

1. **不许删行**。判错的样本把 `confidence` 设 0 并在 `note` 里写原因，保留痕迹。
2. **不许改列名**。要加列先在 schema.json 里加，再同步三处：本文件、`code/config.py`、校验脚本。
