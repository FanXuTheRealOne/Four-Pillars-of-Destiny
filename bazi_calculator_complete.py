#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字计算完整模块
提供年柱、月柱、日柱、时柱的精确计算
基于 cnlunar 库实现
"""

import datetime
from typing import Dict, Tuple
from cnlunar import Lunar


class Pillar:
    """柱（干支对）类"""
    
    def __init__(self, gan: str, zhi: str):
        """
        初始化柱
        :param gan: 天干
        :param zhi: 地支
        """
        self.gan = gan
        self.zhi = zhi
        self.ganzhi = gan + zhi
    
    def __str__(self):
        return self.ganzhi
    
    def __repr__(self):
        return f"Pillar('{self.gan}', '{self.zhi}')"
    
    def to_dict(self) -> Dict[str, str]:
        """转换为字典"""
        return {
            "天干": self.gan,
            "地支": self.zhi,
            "干支": self.ganzhi
        }


class BaZi:
    """八字类"""
    
    def __init__(self, year_pillar: Pillar, month_pillar: Pillar, 
                 day_pillar: Pillar, hour_pillar: Pillar):
        """
        初始化八字
        :param year_pillar: 年柱
        :param month_pillar: 月柱
        :param day_pillar: 日柱
        :param hour_pillar: 时柱
        """
        self.year_pillar = year_pillar
        self.month_pillar = month_pillar
        self.day_pillar = day_pillar
        self.hour_pillar = hour_pillar
    
    def __str__(self):
        return f"{self.year_pillar} {self.month_pillar} {self.day_pillar} {self.hour_pillar}"
    
    def __repr__(self):
        return f"BaZi({self.year_pillar!r}, {self.month_pillar!r}, {self.day_pillar!r}, {self.hour_pillar!r})"
    
    def to_dict(self) -> Dict[str, any]:
        """转换为字典"""
        return {
            "年柱": self.year_pillar.to_dict(),
            "月柱": self.month_pillar.to_dict(),
            "日柱": self.day_pillar.to_dict(),
            "时柱": self.hour_pillar.to_dict(),
            "八字": str(self)
        }
    
    def get_eight_chars(self) -> Tuple[str, str, str, str, str, str, str, str]:
        """
        获取八个字（天干地支分开）
        :return: (年干, 年支, 月干, 月支, 日干, 日支, 时干, 时支)
        """
        return (
            self.year_pillar.gan, self.year_pillar.zhi,
            self.month_pillar.gan, self.month_pillar.zhi,
            self.day_pillar.gan, self.day_pillar.zhi,
            self.hour_pillar.gan, self.hour_pillar.zhi
        )


class BaZiCalculator:
    """
    八字计算器
    
    使用 cnlunar 库进行精确的八字计算
    支持：
    - 年柱计算（基于立春节气）
    - 月柱计算（基于节气）
    - 日柱计算（基于儒略日）
    - 时柱计算（基于五鼠遁，支持早晚子时）
    """
    
    # 天干地支常量
    TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    def __init__(self, birth_datetime: datetime.datetime):
        """
        初始化八字计算器
        :param birth_datetime: 出生时间（公历）
        """
        self.birth_datetime = birth_datetime
        self.lunar = Lunar(birth_datetime)
    
    def calculate_year_pillar(self) -> Pillar:
        """
        计算年柱
        年柱以立春为界，立春前算上一年
        """
        year_gan = self.lunar.year8Char[0]
        year_zhi = self.lunar.year8Char[1]
        return Pillar(year_gan, year_zhi)
    
    def calculate_month_pillar(self) -> Pillar:
        """
        计算月柱
        月柱以节气为界（立春、惊蛰、清明等）
        """
        month_gan = self.lunar.month8Char[0]
        month_zhi = self.lunar.month8Char[1]
        return Pillar(month_gan, month_zhi)
    
    def calculate_day_pillar(self) -> Pillar:
        """
        计算日柱
        日柱基于儒略日计算，从子时开始算新的一天
        """
        day_gan = self.lunar.day8Char[0]
        day_zhi = self.lunar.day8Char[1]
        return Pillar(day_gan, day_zhi)
    
    def calculate_hour_pillar(self) -> Pillar:
        """
        计算时柱
        时柱基于五鼠遁推算
        23:00-00:59 为子时（需要特别处理早晚子时）
        """
        hour_gan = self.lunar.twohour8Char[0]
        hour_zhi = self.lunar.twohour8Char[1]
        return Pillar(hour_gan, hour_zhi)
    
    def calculate(self) -> BaZi:
        """
        计算完整的八字
        :return: BaZi 对象
        """
        year_pillar = self.calculate_year_pillar()
        month_pillar = self.calculate_month_pillar()
        day_pillar = self.calculate_day_pillar()
        hour_pillar = self.calculate_hour_pillar()
        
        return BaZi(year_pillar, month_pillar, day_pillar, hour_pillar)


def calculate_bazi(year: int, month: int, day: int, hour: int, minute: int = 0) -> BaZi:
    """
    便捷函数：计算八字
    
    :param year: 年份
    :param month: 月份 (1-12)
    :param day: 日期 (1-31)
    :param hour: 小时 (0-23)
    :param minute: 分钟 (0-59)，默认为 0
    :return: BaZi 对象
    """
    birth_datetime = datetime.datetime(year, month, day, hour, minute)
    calculator = BaZiCalculator(birth_datetime)
    return calculator.calculate()


def main():
    """主函数：演示和测试"""
    
    print("=" * 80)
    print("八字计算器 - 完整版")
    print("=" * 80)
    
    # 测试案例（50个）
    test_cases = [
        # 原有测试案例
        (1996, 6, 22, 0, 0, "1996-06-22 00:00"),
        (2000, 10, 25, 0, 0, "2000-10-25 00:00"),
        (1996, 6, 22, 12, 30, "1996-06-22 12:30 (中午)"),
        (2000, 1, 1, 12, 0, "2000-01-01 12:00"),
        (2026, 1, 3, 0, 5, "2026-01-03 00:05 (早子时)"),
        (2026, 1, 3, 23, 30, "2026-01-03 23:30 (晚子时)"),
        (1995, 6, 15, 14, 30, "1995-06-15 14:30"),
        (2024, 2, 4, 16, 27, "2024-02-04 16:27 (立春节气)"),
        
        # 不同年份测试
        (1900, 1, 1, 0, 0, "1900-01-01 00:00 (世纪初)"),
        (1950, 5, 15, 10, 30, "1950-05-15 10:30"),
        (1970, 7, 20, 15, 45, "1970-07-20 15:45"),
        (1980, 3, 10, 8, 15, "1980-03-10 08:15"),
        (1990, 9, 25, 18, 0, "1990-09-25 18:00"),
        (2005, 11, 30, 20, 30, "2005-11-30 20:30"),
        (2010, 4, 1, 6, 0, "2010-04-01 06:00"),
        (2015, 8, 15, 12, 0, "2015-08-15 12:00"),
        (2020, 12, 31, 23, 59, "2020-12-31 23:59 (年末)"),
        (2025, 6, 1, 9, 30, "2025-06-01 09:30"),
        
        # 不同月份测试
        (2000, 1, 15, 14, 0, "2000-01-15 14:00 (一月)"),
        (2000, 2, 14, 16, 0, "2000-02-14 16:00 (二月)"),
        (2000, 3, 15, 10, 0, "2000-03-15 10:00 (三月)"),
        (2000, 4, 15, 11, 0, "2000-04-15 11:00 (四月)"),
        (2000, 5, 15, 13, 0, "2000-05-15 13:00 (五月)"),
        (2000, 7, 15, 15, 0, "2000-07-15 15:00 (七月)"),
        (2000, 8, 15, 17, 0, "2000-08-15 17:00 (八月)"),
        (2000, 9, 15, 19, 0, "2000-09-15 19:00 (九月)"),
        (2000, 10, 15, 21, 0, "2000-10-15 21:00 (十月)"),
        (2000, 11, 15, 22, 0, "2000-11-15 22:00 (十一月)"),
        (2000, 12, 15, 7, 0, "2000-12-15 07:00 (十二月)"),
        
        # 特殊日期测试
        (2000, 2, 29, 12, 0, "2000-02-29 12:00 (闰年2月29日)"),
        (2004, 2, 29, 14, 30, "2004-02-29 14:30 (闰年)"),
        (2000, 1, 31, 18, 0, "2000-01-31 18:00 (月末)"),
        (2000, 4, 30, 20, 0, "2000-04-30 20:00 (月末)"),
        (2000, 6, 30, 22, 0, "2000-06-30 22:00 (月末)"),
        
        # 不同时辰测试
        (2000, 6, 15, 1, 0, "2000-06-15 01:00 (丑时)"),
        (2000, 6, 15, 3, 0, "2000-06-15 03:00 (寅时)"),
        (2000, 6, 15, 5, 0, "2000-06-15 05:00 (卯时)"),
        (2000, 6, 15, 7, 0, "2000-06-15 07:00 (辰时)"),
        (2000, 6, 15, 9, 0, "2000-06-15 09:00 (巳时)"),
        (2000, 6, 15, 11, 0, "2000-06-15 11:00 (午时)"),
        (2000, 6, 15, 13, 0, "2000-06-15 13:00 (未时)"),
        (2000, 6, 15, 15, 0, "2000-06-15 15:00 (申时)"),
        (2000, 6, 15, 17, 0, "2000-06-15 17:00 (酉时)"),
        (2000, 6, 15, 19, 0, "2000-06-15 19:00 (戌时)"),
        (2000, 6, 15, 21, 0, "2000-06-15 21:00 (亥时)"),
        (2000, 6, 15, 23, 0, "2000-06-15 23:00 (晚子时)"),
        
        # 节气边界测试
        (2024, 2, 3, 23, 59, "2024-02-03 23:59 (立春前)"),
        (2024, 2, 5, 0, 1, "2024-02-05 00:01 (立春后)"),
        (2024, 5, 5, 8, 10, "2024-05-05 08:10 (立夏)"),
        (2024, 8, 7, 14, 20, "2024-08-07 14:20 (立秋)"),
        (2024, 11, 7, 18, 30, "2024-11-07 18:30 (立冬)"),
        
        # 随机组合测试
        (1998, 3, 8, 9, 15, "1998-03-08 09:15"),
        (2002, 5, 12, 16, 45, "2002-05-12 16:45"),
        (2008, 8, 8, 8, 8, "2008-08-08 08:08 (特殊时间)"),
        (2012, 12, 21, 12, 0, "2012-12-21 12:00"),
        (2018, 6, 18, 18, 18, "2018-06-18 18:18"),
    ]
    
    for year, month, day, hour, minute, description in test_cases:
        print(f"\n【测试案例】{description}")
        print(f"公历时间: {year}年{month:02d}月{day:02d}日 {hour:02d}:{minute:02d}")
        
        try:
            bazi = calculate_bazi(year, month, day, hour, minute)
            
            print(f"\n八字结果:")
            print(f"  年柱: {bazi.year_pillar}")
            print(f"  月柱: {bazi.month_pillar}")
            print(f"  日柱: {bazi.day_pillar}")
            print(f"  时柱: {bazi.hour_pillar}")
            print(f"\n  完整八字: {bazi}")
            
            # 输出详细信息
            eight_chars = bazi.get_eight_chars()
            print(f"\n  八个字: {' '.join(eight_chars)}")
            
        except Exception as e:
            print(f"✗ 计算出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
