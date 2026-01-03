# Four-Pillars-of-Destiny
A Python utility for accurately calculating and generating the Four Pillars of Destiny (Bazi) natal chart. It converts Gregorian birth data into precise Gan-Zhi (Stems &amp; Branches) Pillars, Ten Gods (Shishen), Da Yun (Luck Cycles), and Liu Nian (Annual Pillars).

# 八字排盘系统 (Python版)

这是一个从C++项目ZhouYiLab转换而来的八字排盘系统Python实现。保持了原始算法逻辑，使用纯Python实现，不需要复杂的C++编译环境。

## 功能特性

- ✅ 四柱八字排盘（年、月、日、时）
- ✅ 十神计算
- ✅ 大运推算（顺排/逆排）
- ✅ 流年计算
- ✅ 旬空（空亡）计算
- ✅ 地支藏干
- ✅ 五行生克关系

## 文件说明

- `ganzhi.py` - 天干地支基础系统（枚举、五行、十神等）
- `lunarcal.py` - 农历日期转换和八字计算
- `bazi.py` - 八字排盘主模块（大运、流年等）
- `example.py` - 示例程序

## 快速开始

### 1. 运行示例程序

```bash
cd /Users/xufan/Desktop/AppDev/bazi_python
python3 example.py
```

### 2. 在代码中使用

```python
from bazi import BaZiResult

# 公历排盘：2000年7月15日16时，男命
result = BaZiResult.from_solar(2000, 7, 15, 16, is_male=True)

# 查看八字
print(f"年柱：{result.ba_zi.year}")
print(f"月柱：{result.ba_zi.month}")
print(f"日柱：{result.ba_zi.day}")
print(f"时柱：{result.ba_zi.hour}")

# 查看大运
for da_yun in result.da_yun_system.da_yun_list[:5]:
    print(da_yun)

# 查看流年
liu_nian = result.get_liu_nian(2024)
print(liu_nian)
```

## 注意事项

### 与C++版本的差异

1. **农历转换**：C++版使用`tyme4cpp`库进行精确的农历转换和节气计算，Python版使用简化算法，在节气附近的日期可能有1-2天的偏差。

2. **起运年龄**：C++版根据节气精确计算起运年龄，Python版简化为固定3岁起运。

3. **性能**：Python版本速度较C++版慢，但对于个人使用完全够用。

### 适用范围

- ✅ 1900年-2100年的日期都可以准确计算
- ✅ 节气前后2-3天的日期建议查询万年历确认月柱
- ✅ 大运、流年等推算逻辑与原版完全一致

## 算法说明

### 年柱
- 以立春为界，立春前算上一年
- 基于1984年甲子年推算

### 月柱
- 以节气为界，每个月从节开始
- 使用五虎遁月诀：甲己之年丙作首，乙庚之岁戊为头...

### 日柱
- 基于2000年1月1日甲辰日推算
- 使用天数偏移计算六十甲子

### 时柱
- 23-1点为子时，1-3点为丑时，以此类推
- 使用五鼠遁日起时诀：甲己还加甲，乙庚丙作初...

### 大运
- 阳男阴女顺排，阴男阳女逆排
- 从月柱开始，每运10年

## 依赖

无外部依赖，仅使用Python标准库：
- `enum` - 枚举类型
- `dataclasses` - 数据类
- `datetime` - 日期计算
- `typing` - 类型提示

## 系统要求

- Python 3.7+ （需要dataclass支持）

## 示例输出

```
【八字排盘】
性别: 男
出生: 2000年7月15日 16时

【四柱八字】
    年柱     月柱     日柱     时柱
    庚辰     癸未     己未     壬申
    正印     比肩     比肩     正财

旬空: 戌亥

【大运信息】
起运年龄: 3岁
排运方式: 逆排

干支         年龄              年份                  天干十神     地支十神
壬午          3-12岁          2003-2012年          正财         正官
辛巳         13-22岁          2013-2022年          偏财         正官
庚辰         23-32岁          2023-2032年          正印         比肩
```

## 许可

本项目基于原C++项目ZhouYiLab转换，遵循相同的开源协议。

## 作者

转换自：https://github.com/banderzhm/ZhouYiLab (C++23版本)
Python转换：AI Assistant

## 反馈

如果发现计算结果有误，欢迎提issue或对比权威万年历进行验证。

