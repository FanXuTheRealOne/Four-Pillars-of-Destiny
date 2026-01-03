"""
农历日期转换和八字计算
根据工程规范实现高精度月柱、日柱、时柱计算
"""
from datetime import datetime, timedelta
from typing import Tuple, Optional
import math
from ganzhi import TianGan, DiZhi, TIAN_GAN_ZH, DI_ZHI_ZH


# ==================== 六十甲子 ====================

def get_sixty_jiazi_index(gan: TianGan, zhi: DiZhi) -> int:
    """获取六十甲子索引（0-59）"""
    for i in range(gan, 60, 10):
        if i % 12 == zhi:
            return i
    return 0


def jiazi_from_index(index: int) -> Tuple[TianGan, DiZhi]:
    """从索引获取天干地支"""
    index = index % 60
    return (TianGan(index % 10), DiZhi(index % 12))


# ==================== 儒略日 (Julian Day) 计算 ====================

def gregorian_to_julian_day(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> float:
    """
    将公历日期时间转换为儒略日
    算法基于 Jean Meeus 的《天文算法》
    """
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + a // 4
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    
    # 添加时分秒
    jd += hour / 24.0 + minute / 1440.0 + second / 86400.0
    
    return jd


def julian_day_to_gregorian(jd: float) -> Tuple[int, int, int, int, int, int]:
    """
    将儒略日转换为公历日期时间
    """
    jd += 0.5
    Z = int(jd)
    F = jd - Z
    
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - alpha // 4
    
    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)
    
    day = B - D - int(30.6001 * E) + F
    if E < 14:
        month = E - 1
    else:
        month = E - 13
    
    if month > 2:
        year = C - 4716
    else:
        year = C - 4715
    
    # 提取时分秒
    hours = F * 24
    hour = int(hours)
    minutes = (hours - hour) * 60
    minute = int(minutes)
    second = int((minutes - minute) * 60)
    
    return (year, month, int(day), hour, minute, second)


# ==================== 高精度节气计算 ====================

def calculate_solar_term(year: int, term_index: int) -> datetime:
    """
    计算指定年份的节气时刻
    term_index: 0=立春, 1=惊蛰, 2=清明, ..., 11=小寒
    使用高精度天文算法（基于太阳黄经）
    """
    # 各节气的太阳黄经（度）
    target_longitude = [
        315.0,  # 立春
        330.0,  # 惊蛰
        0.0,    # 清明
        15.0,   # 立夏
        45.0,   # 芒种
        75.0,   # 小暑
        105.0,  # 立秋
        135.0,  # 白露
        165.0,  # 寒露
        195.0,  # 立冬
        225.0,  # 大雪
        255.0   # 小寒
    ][term_index]
    
    # 基准日期（立春约在2月4日）
    approx_month = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1][term_index]
    approx_day = [4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6][term_index]
    
    # 处理小寒（在次年1月）
    if term_index == 11:  # 小寒
        approx_year = year + 1
    else:
        approx_year = year
    
    # 初始近似日期
    approx_date = datetime(approx_year, approx_month, approx_day, 12, 0, 0)
    
    # 迭代计算精确时刻
    for _ in range(3):  # 迭代3次通常足够精确
        jd = gregorian_to_julian_day(approx_date.year, approx_date.month, approx_date.day, 
                                     approx_date.hour, approx_date.minute, approx_date.second)
        
        # 计算太阳黄经
        T = (jd - 2451545.0) / 36525.0
        
        # 太阳平黄经（度）
        L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T * T
        
        # 太阳平近点角（度）
        M = 357.52911 + 35999.05029 * T - 0.0001537 * T * T
        
        # 太阳黄经修正（简化版）
        C = (1.914602 - 0.004817 * T - 0.000014 * T * T) * math.sin(math.radians(M)) + \
            (0.019993 - 0.000101 * T) * math.sin(math.radians(2 * M)) + \
            0.000289 * math.sin(math.radians(3 * M))
        
        # 真太阳黄经
        L = L0 + C
        
        # 归一化到0-360度
        L = L % 360
        
        # 计算目标黄经与当前黄经的差值
        delta_L = (target_longitude - L + 360) % 360
        if delta_L > 180:
            delta_L -= 360
        
        # 转换为时间修正（每度约1天/360度）
        delta_days = delta_L / 360.0 * 365.2422
        
        # 修正日期
        jd_corrected = jd + delta_days
        
        # 转换回公历
        year_c, month_c, day_c, hour_c, minute_c, second_c = julian_day_to_gregorian(jd_corrected)
        approx_date = datetime(year_c, month_c, day_c, hour_c, minute_c, second_c)
    
    return approx_date


def get_solar_terms(year: int) -> list:
    """
    获取指定年份的所有24节气时刻
    返回：12个"节"的时刻列表（立春、惊蛰、清明...小寒）
    """
    terms = []
    for i in range(12):
        term_time = calculate_solar_term(year, i)
        terms.append(term_time)
    return terms


def get_month_branch_by_solar_term(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> DiZhi:
    """
    根据精确的节气时刻确定月支
    """
    birth_time = datetime(year, month, day, hour, minute, second)
    
    # 获取当前年份和前一年的节气
    terms_this_year = get_solar_terms(year)
    terms_last_year = get_solar_terms(year - 1)
    
    # 构建完整的节气序列（从去年小寒开始）
    # 顺序：去年小寒 -> 今年立春 -> 今年惊蛰 -> ... -> 今年小寒
    all_terms = [terms_last_year[11]]  # 去年小寒
    all_terms.extend(terms_this_year)   # 今年12个节气
    
    # 月支映射（对应节气区间）
    # 索引0: 去年小寒-今年立春 -> 丑月
    # 索引1: 今年立春-今年惊蛰 -> 寅月
    # 索引2: 今年惊蛰-今年清明 -> 卯月
    # ...
    month_branches = [
        DiZhi.CHOU,  # 去年小寒-今年立春：丑月
        DiZhi.YIN,   # 今年立春-今年惊蛰：寅月
        DiZhi.MAO,   # 今年惊蛰-今年清明：卯月
        DiZhi.CHEN,  # 今年清明-今年立夏：辰月
        DiZhi.SI,    # 今年立夏-今年芒种：巳月
        DiZhi.WU,    # 今年芒种-今年小暑：午月
        DiZhi.WEI,   # 今年小暑-今年立秋：未月
        DiZhi.SHEN,  # 今年立秋-今年白露：申月
        DiZhi.YOU,   # 今年白露-今年寒露：酉月
        DiZhi.XU,    # 今年寒露-今年立冬：戌月
        DiZhi.HAI,   # 今年立冬-今年大雪：亥月
        DiZhi.ZI,    # 今年大雪-今年小寒：子月
        DiZhi.CHOU,  # 今年小寒-明年立春：丑月（如果超出范围）
    ]
    
    # 判断出生时间在哪个节气区间
    for i in range(len(all_terms) - 1):
        if all_terms[i] <= birth_time < all_terms[i + 1]:
            return month_branches[i]
    
    # 如果在小寒之前（应该不会发生，但保险起见）
    if birth_time < all_terms[0]:
        return DiZhi.CHOU  # 丑月
    
    # 如果在小寒之后（今年小寒之后，应该是子月或丑月）
    return DiZhi.ZI  # 子月


# ==================== 年柱计算 ====================

def get_year_pillar(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> Tuple[TianGan, DiZhi]:
    """
    获取年柱
    注意：立春前算上一年
    """
    # 获取立春时刻
    spring_start = calculate_solar_term(year, 0)  # 立春
    
    birth_time = datetime(year, month, day, hour, minute, second)
    
    # 如果在立春前，算上一年
    if birth_time < spring_start:
        year -= 1
    
    # 年干计算：(阳历年份 - 3) / 10 的余数，对应的天干 index 是年干
    # 注意：算法从1开始（甲=1），但enum从0开始（甲=0），需要减1
    year_gan_index = ((year - 3) % 10 - 1) % 10
    year_gan = TianGan(year_gan_index)
    
    # 年支计算：(阳历年份 - 3) / 12 的余数，对应的地支 index 是年支
    # 注意：算法从1开始（子=1），但enum从0开始（子=0），需要减1
    year_zhi_index = ((year - 3) % 12 - 1) % 12
    year_zhi = DiZhi(year_zhi_index)
    
    return (year_gan, year_zhi)


# ==================== 月柱计算 ====================

def get_month_pillar(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> Tuple[TianGan, DiZhi]:
    """
    获取月柱
    使用精确节气判断月支，使用五虎遁规则计算月干
    """
    # 获取年干（立春后的年份）
    year_gan, _ = get_year_pillar(year, month, day, hour, minute, second)
    
    # 使用精确节气确定月支
    month_zhi = get_month_branch_by_solar_term(year, month, day, hour, minute, second)
    
    # 五虎遁规则计算月干
    # 公式：StartStemIndex = (YearStemIndex * 2 + 2) % 10
    year_stem_index = year_gan % 10
    start_stem_index = (year_stem_index * 2 + 2) % 10
    
    # 计算月干：MonthStemIndex = (StartStemIndex + MonthBranchIndex - 2) % 10
    month_branch_index = month_zhi % 12
    month_stem_index = (start_stem_index + month_branch_index - 2) % 10
    
    month_gan = TianGan(month_stem_index)
    
    return (month_gan, month_zhi)


# ==================== 日柱计算 ====================

def get_day_pillar(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> Tuple[TianGan, DiZhi]:
    """
    获取日柱
    使用儒略日算法，基准日：1900年1月1日00:00:00为甲戌
    重要：23:00:00-23:59:59之间的时间，日柱应取下一天的干支
    """
    # 处理早晚子时换日：23:00:00-23:59:59算下一天
    if hour >= 23:
        # 取下一天的日期
        birth_date = datetime(year, month, day, hour, minute, second)
        next_day = birth_date + timedelta(days=1)
        year = next_day.year
        month = next_day.month
        day = next_day.day
        # 时柱仍使用原时间，但日柱用下一天
    
    # 基准日：1900年1月1日00:00:00为甲戌
    epoch_year, epoch_month, epoch_day = 1900, 1, 1
    epoch_gan = TianGan.JIA  # 甲
    epoch_zhi = DiZhi.XU     # 戌
    epoch_jiazi_index = get_sixty_jiazi_index(epoch_gan, epoch_zhi)
    
    # 计算基准日的儒略日
    epoch_jd = gregorian_to_julian_day(epoch_year, epoch_month, epoch_day, 0, 0, 0)
    
    # 计算目标日期的儒略日
    target_jd = gregorian_to_julian_day(year, month, day, 0, 0, 0)
    
    # 计算天数差
    days_since_epoch = int(target_jd - epoch_jd)
    
    # 计算日柱干支索引
    day_ganzhi_index = (epoch_jiazi_index + days_since_epoch) % 60
    
    return jiazi_from_index(day_ganzhi_index)


# ==================== 时柱计算 ====================

def get_hour_pillar(day_gan: TianGan, hour: int, minute: int = 0, second: int = 0) -> Tuple[TianGan, DiZhi]:
    """
    获取时柱
    时支：23:00-00:59为子时，01:00-02:59为丑时，以此类推
    时干：使用五鼠遁规则
    """
    # 确定时支（23:00-00:59为子时）
    if hour == 23:
        hour_zhi = DiZhi.ZI
    elif hour == 0:
        hour_zhi = DiZhi.ZI  # 00:00-00:59也是子时
    elif hour == 1 or hour == 2:
        hour_zhi = DiZhi.CHOU
    elif hour == 3 or hour == 4:
        hour_zhi = DiZhi.YIN
    elif hour == 5 or hour == 6:
        hour_zhi = DiZhi.MAO
    elif hour == 7 or hour == 8:
        hour_zhi = DiZhi.CHEN
    elif hour == 9 or hour == 10:
        hour_zhi = DiZhi.SI
    elif hour == 11 or hour == 12:
        hour_zhi = DiZhi.WU
    elif hour == 13 or hour == 14:
        hour_zhi = DiZhi.WEI
    elif hour == 15 or hour == 16:
        hour_zhi = DiZhi.SHEN
    elif hour == 17 or hour == 18:
        hour_zhi = DiZhi.YOU
    elif hour == 19 or hour == 20:
        hour_zhi = DiZhi.XU
    elif hour == 21 or hour == 22:
        hour_zhi = DiZhi.HAI
    else:
        hour_zhi = DiZhi.ZI  # 默认子时
    
    # 五鼠遁规则计算时干
    # 公式：StartStemIndex = (DayStemIndex * 2 + 0) % 10
    day_stem_index = day_gan % 10
    start_stem_index = (day_stem_index * 2 + 0) % 10
    
    # 计算时干：HourStemIndex = (StartStemIndex + HourBranchIndex) % 10
    hour_branch_index = hour_zhi % 12
    hour_stem_index = (start_stem_index + hour_branch_index) % 10
    
    hour_gan = TianGan(hour_stem_index)
    
    return (hour_gan, hour_zhi)


# ==================== 真太阳时校正 ====================

def apply_solar_time_correction(year: int, month: int, day: int, hour: int, minute: int, second: int, 
                                longitude: float = 120.0) -> Tuple[int, int, int, int, int, int]:
    """
    真太阳时校正
    longitude: 出生地经度（东经为正，西经为负），默认120.0（北京时间）
    返回：校正后的年月日时分秒
    """
    # 时区标准经度（北京时间）
    standard_longitude = 120.0
    
    # 经度差
    longitude_diff = longitude - standard_longitude
    
    # 时间修正量（分钟）：每度经度相差4分钟
    time_correction_minutes = longitude_diff * 4
    
    # 应用修正
    birth_time = datetime(year, month, day, hour, minute, second)
    corrected_time = birth_time + timedelta(minutes=time_correction_minutes)
    
    return (corrected_time.year, corrected_time.month, corrected_time.day,
            corrected_time.hour, corrected_time.minute, corrected_time.second)


# ==================== 八字计算 ====================

def calculate_bazi(year: int, month: int, day: int, hour: int, 
                   minute: int = 0, second: int = 0,
                   longitude: Optional[float] = None) -> dict:
    """
    计算完整八字
    参数：
        year, month, day, hour, minute, second: 出生时间（北京时间）
        longitude: 出生地经度（可选，用于真太阳时校正）
    返回: {
        'year': (天干, 地支),
        'month': (天干, 地支),
        'day': (天干, 地支),
        'hour': (天干, 地支)
    }
    """
    # 真太阳时校正（如果提供了经度）
    if longitude is not None:
        year, month, day, hour, minute, second = apply_solar_time_correction(
            year, month, day, hour, minute, second, longitude
        )
    
    year_pillar = get_year_pillar(year, month, day, hour, minute, second)
    month_pillar = get_month_pillar(year, month, day, hour, minute, second)
    day_pillar = get_day_pillar(year, month, day, hour, minute, second)
    hour_pillar = get_hour_pillar(day_pillar[0], hour, minute, second)
    
    return {
        'year': year_pillar,
        'month': month_pillar,
        'day': day_pillar,
        'hour': hour_pillar
    }
