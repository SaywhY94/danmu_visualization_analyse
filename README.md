## 对弹幕数据实现可视化分析

### 使用方法：

1、调用visualization_analyse_danmu.py脚本后会自动对当前目录下的csv弹幕数据文件进行数据处理，可视化分析内容包含有：发送弹幕TOP5用户统计、用户发送弹幕数量百分比分布图、用户发送弹幕长度百分比分布图、时间轴弹幕密度变化统计
2、调用visualization_analyse_type.py脚本后会自动对当前目录下的csv弹幕数据文件进行数据处理，可视化分析内容包含有：每类弹幕数量统计、每类用户发送弹幕数量百分比分布图、每类用户发送弹幕长度百分比分布图、每类时间轴弹幕密度变化统计

```bash
python visualization_analyse_danmu.py
python visualization_analyse_type.py
```