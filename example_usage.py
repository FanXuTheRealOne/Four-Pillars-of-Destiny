#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字计算器使用示例
演示如何使用 bazi_calculator_complete 模块计算八字
"""

from bazi_calculator_complete import calculate_bazi, BaZiCalculator
import datetime


def example_1_basic_usage():
    """示例1：基础用法"""
    print("=" * 60)
    print("示例1：基础用法")
    print("=" * 60)
    
    # 计算八字：1990年1月1日 0时0分
    bazi = calculate_bazi(1990, 1, 1, 0, 0)
    
    print(f"出生时间: 1990年01月01日 00:00")
    print(f"完整八字: {bazi}")
    print(f"年柱: {bazi.year_pillar}")
    print(f"月柱: {bazi.month_pillar}")
    print(f"日柱: {bazi.day_pillar}")
    print(f"时柱: {bazi.hour_pillar}")
    print()


def example_2_datetime_object():
    """示例2：使用 datetime 对象"""
    print("=" * 60)
    print("示例2：使用 datetime 对象")
    print("=" * 60)
    
    # 使用 datetime 对象
    birth_datetime = datetime.datetime(2026, 1, 3, 0, 5)
    calculator = BaZiCalculator(birth_datetime)
    bazi = calculator.calculate()
    
    print(f"出生时间: {birth_datetime.strftime('%Y年%m月%d日 %H:%M')}")
    print(f"完整八字: {bazi}")
    print()


def example_3_detailed_info():
    """示例3：获取详细信息"""
    print("=" * 60)
    print("示例3：获取详细信息")
    print("=" * 60)
    
    bazi = calculate_bazi(1995, 6, 15, 14, 30)
    
    print(f"出生时间: 1995年06月15日 14:30")
    print(f"完整八字: {bazi}")
    print()
    
    # 获取八个字（天干地支分开）
    eight_chars = bazi.get_eight_chars()
    print(f"八个字: {' '.join(eight_chars)}")
    print()
    
    # 获取年柱详细信息
    year_pillar = bazi.year_pillar
    print(f"年柱详细信息:")
    print(f"  天干: {year_pillar.gan}")
    print(f"  地支: {year_pillar.zhi}")
    print(f"  干支: {year_pillar.ganzhi}")
    print()
    
    # 转换为字典
    bazi_dict = bazi.to_dict()
    print(f"八字字典:")
    for key, value in bazi_dict.items():
        print(f"  {key}: {value}")
    print()


def example_4_zishi_handling():
    """示例4：早晚子时处理"""
    print("=" * 60)
    print("示例4：早晚子时处理")
    print("=" * 60)
    
    # 早子时（00:05）
    bazi_early = calculate_bazi(2026, 1, 3, 0, 5)
    print(f"早子时 (2026-01-03 00:05):")
    print(f"  八字: {bazi_early}")
    print(f"  日柱: {bazi_early.day_pillar}")
    print()
    
    # 晚子时（23:30）
    bazi_late = calculate_bazi(2026, 1, 3, 23, 30)
    print(f"晚子时 (2026-01-03 23:30):")
    print(f"  八字: {bazi_late}")
    print(f"  日柱: {bazi_late.day_pillar}")
    print()
    
    print("注意：早子时和晚子时的日柱不同！")
    print()


def example_5_jieqi_boundary():
    """示例5：节气边界处理"""
    print("=" * 60)
    print("示例5：节气边界处理（立春）")
    print("=" * 60)
    
    # 2024年立春：2月4日 16:27
    # 立春前
    bazi_before = calculate_bazi(2024, 2, 4, 16, 0)
    print(f"立春前 (2024-02-04 16:00):")
    print(f"  八字: {bazi_before}")
    print(f"  年柱: {bazi_before.year_pillar}")
    print()
    
    # 立春后
    bazi_after = calculate_bazi(2024, 2, 4, 17, 0)
    print(f"立春后 (2024-02-04 17:00):")
    print(f"  八字: {bazi_after}")
    print(f"  年柱: {bazi_after.year_pillar}")
    print()
    
    print("注意：立春前后年柱可能不同！")
    print()


def main():
    """主函数"""
    print("\n")
    print("*" * 60)
    print("八字计算器 - 使用示例")
    print("*" * 60)
    print("\n")
    
    example_1_basic_usage()
    example_2_datetime_object()
    example_3_detailed_info()
    example_4_zishi_handling()
    example_5_jieqi_boundary()
    
    print("=" * 60)
    print("所有示例运行完毕")
    print("=" * 60)


if __name__ == "__main__":
    main()
