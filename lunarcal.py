"""
农历日期转换和八字计算
使用简化的算法实现农历转换
"""
from datetime import datetime
from typing import Tuple
from ganzhi import TianGan, DiZhi, TIAN_GAN_ZH, DI_ZHI_ZH


# ==================== 节气表（简化版）====================
# 每个月的节气大致日期（2000年前后）

JIEQI_BASE_DATES = [
    # (节气月份, 节气大致日期)
    (2, 4),   # 立春 (约2月4日)
    (3, 6),   # 惊蛰 (约3月6日)
    (4, 5),   # 清明 (约4月5日)
    (5, 6),   # 立夏 (约5月6日)
    (6, 6),   # 芒种 (约6月6日)
    (7, 7),   # 小暑 (约7月7日)
    (8, 8),   # 立秋 (约8月8日)
    (9, 8),   # 白露 (约9月8日)
    (10, 8),  # 寒露 (约10月8日)
    (11, 7),  # 立冬 (约11月7日)
    (12, 7),  # 大雪 (约12月7日)
    (1, 6),   # 小寒 (约1月6日，次年)
]


# ==================== 六十甲子 ====================

def get_sixty_jiazi_index(gan: TianGan, zhi: DiZhi) -> int:
    """获取六十甲子索引（0-59）"""
    # 使用中国剩余定理求解
    for i in range(gan, 60, 10):
        if i % 12 == zhi:
            return i
    return 0


def jiazi_from_index(index: int) -> Tuple[TianGan, DiZhi]:
    """从索引获取天干地支"""
    index = index % 60
    return (TianGan(index % 10), DiZhi(index % 12))


# ==================== 年柱计算 ====================

def get_year_pillar(year: int, month: int, day: int) -> Tuple[TianGan, DiZhi]:
    """
    获取年柱
    注意：立春前算上一年
    """
    # 简化处理：如果在立春(约2月4日)前，算上一年
    if month < 2 or (month == 2 and day < 4):
        year -= 1
    
    # 从1984年甲子年开始计算（1984年是甲子年）
    # 1984 = 甲子年（索引0）
    base_year = 1984
    offset = (year - base_year) % 60
    return jiazi_from_index(offset)


# ==================== 月柱计算 ====================

def get_month_pillar(year: int, month: int, day: int) -> Tuple[TianGan, DiZhi]:
    """
    获取月柱
    五虎遁月诀：甲己之年丙作首，乙庚之岁戊为头，丙辛必定寻庚起，丁壬壬位顺行流，更有戊癸何方觅，甲寅之上好追求
    """
    # 先获取年干（立春后的年份）
    year_gan, _ = get_year_pillar(year, month, day)
    
    # 确定节气月（寅月=正月，从立春开始）
    # 简化：根据公历月份粗略对应
    jieqi_month_map = [
        (1, 1, 6, DiZhi.CHOU),   # 1月前6天为子月，6日后为丑月
        (2, 2, 4, DiZhi.YIN),    # 2月4日立春后为寅月
        (3, 3, 6, DiZhi.MAO),    # 3月6日惊蛰后为卯月
        (4, 4, 5, DiZhi.CHEN),   # 4月5日清明后为辰月
        (5, 5, 6, DiZhi.SI),     # 5月6日立夏后为巳月
        (6, 6, 6, DiZhi.WU),     # 6月6日芒种后为午月
        (7, 7, 7, DiZhi.WEI),    # 7月7日小暑后为未月
        (8, 8, 8, DiZhi.SHEN),   # 8月8日立秋后为申月
        (9, 9, 8, DiZhi.YOU),    # 9月8日白露后为酉月
        (10, 10, 8, DiZhi.XU),   # 10月8日寒露后为戌月
        (11, 11, 7, DiZhi.HAI),  # 11月7日立冬后为亥月
        (12, 12, 7, DiZhi.ZI),   # 12月7日大雪后为子月
    ]
    
    # 确定月支
    month_zhi = DiZhi.YIN  # 默认寅月
    for m, jie_m, jie_d, zhi in jieqi_month_map:
        if month == jie_m:
            if day >= jie_d:
                month_zhi = zhi
            else:
                # 使用上一个月的地支
                month_zhi = DiZhi((zhi - 1 + 12) % 12)
            break
        elif month == m:
            month_zhi = zhi
            break
    
    # 五虎遁月诀确定月干
    # 甲己丙作首：甲年、己年，寅月从丙开始
    # 乙庚戊为头：乙年、庚年，寅月从戊开始
    # 丙辛庚起：丙年、辛年，寅月从庚开始
    # 丁壬壬位：丁年、壬年，寅月从壬开始
    # 戊癸甲寅：戊年、癸年，寅月从甲开始
    
    yg = year_gan % 10
    if yg in [0, 5]:  # 甲、己
        yin_month_gan = TianGan.BING
    elif yg in [1, 6]:  # 乙、庚
        yin_month_gan = TianGan.WU
    elif yg in [2, 7]:  # 丙、辛
        yin_month_gan = TianGan.GENG
    elif yg in [3, 8]:  # 丁、壬
        yin_month_gan = TianGan.REN
    else:  # 戊、癸
        yin_month_gan = TianGan.JIA
    
    # 从寅月(2)开始偏移
    month_offset = (month_zhi - DiZhi.YIN + 12) % 12
    month_gan = TianGan((yin_month_gan + month_offset) % 10)
    
    return (month_gan, month_zhi)


# ==================== 日柱计算 ====================

def get_day_pillar(year: int, month: int, day: int) -> Tuple[TianGan, DiZhi]:
    """
    获取日柱
    使用简化公式计算日柱（基于公历）
    """
    # 计算从2000年1月1日（甲辰日）到目标日期的天数
    base_date = datetime(2000, 1, 1)  # 2000年1月1日为甲辰日
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    # 2000年1月1日是甲辰日（甲=0，辰=4）
    # 六十甲子索引 = 40
    base_jiazi = get_sixty_jiazi_index(TianGan.JIA, DiZhi.CHEN)
    
    # 计算目标日期的六十甲子索引
    target_jiazi = (base_jiazi + days_diff) % 60
    
    return jiazi_from_index(target_jiazi)


# ==================== 时柱计算 ====================

def get_hour_pillar(day_gan: TianGan, hour: int) -> Tuple[TianGan, DiZhi]:
    """
    获取时柱
    五鼠遁日起时诀：甲己还加甲，乙庚丙作初，丙辛从戊起，丁壬庚子居，戊癸何方发，壬子是真途
    """
    # 确定时支（23-1点为子时）
    hour_zhi_map = [
        DiZhi.ZI,    # 23-1点
        DiZhi.CHOU,  # 1-3点
        DiZhi.YIN,   # 3-5点
        DiZhi.MAO,   # 5-7点
        DiZhi.CHEN,  # 7-9点
        DiZhi.SI,    # 9-11点
        DiZhi.WU,    # 11-13点
        DiZhi.WEI,   # 13-15点
        DiZhi.SHEN,  # 15-17点
        DiZhi.YOU,   # 17-19点
        DiZhi.XU,    # 19-21点
        DiZhi.HAI,   # 21-23点
    ]
    
    # 23点算次日子时
    if hour == 23:
        hour_zhi = DiZhi.ZI
    else:
        hour_idx = (hour + 1) // 2
        hour_zhi = hour_zhi_map[hour_idx]
    
    # 五鼠遁日起时诀确定时干
    dg = day_gan % 10
    if dg in [0, 5]:  # 甲、己
        zi_hour_gan = TianGan.JIA
    elif dg in [1, 6]:  # 乙、庚
        zi_hour_gan = TianGan.BING
    elif dg in [2, 7]:  # 丙、辛
        zi_hour_gan = TianGan.WU
    elif dg in [3, 8]:  # 丁、壬
        zi_hour_gan = TianGan.GENG
    else:  # 戊、癸
        zi_hour_gan = TianGan.REN
    
    # 从子时开始偏移
    hour_offset = (hour_zhi - DiZhi.ZI + 12) % 12
    hour_gan = TianGan((zi_hour_gan + hour_offset) % 10)
    
    return (hour_gan, hour_zhi)


# ==================== 八字计算 ====================

def calculate_bazi(year: int, month: int, day: int, hour: int) -> dict:
    """
    计算完整八字
    返回: {
        'year': (天干, 地支),
        'month': (天干, 地支),
        'day': (天干, 地支),
        'hour': (天干, 地支)
    }
    """
    year_pillar = get_year_pillar(year, month, day)
    month_pillar = get_month_pillar(year, month, day)
    day_pillar = get_day_pillar(year, month, day)
    hour_pillar = get_hour_pillar(day_pillar[0], hour)
    
    return {
        'year': year_pillar,
        'month': month_pillar,
        'day': day_pillar,
        'hour': hour_pillar
    }

