#!/usr/bin/env python3
"""
八字系统示例程序
演示如何使用八字排盘功能
"""
from bazi import BaZiResult
from ganzhi import shi_shen_to_zh


def display_result(result: BaZiResult):
    """显示八字排盘结果"""
    print("=" * 60)
    print("【八字排盘】")
    print("=" * 60)
    print()
    
    # 基本信息
    print("【基本信息】")
    print(f"性别: {'男' if result.is_male else '女'}")
    print(f"出生: {result.birth_year}年{result.birth_month}月{result.birth_day}日 {result.birth_hour}时")
    print()
    
    # 四柱八字
    print("【四柱八字】")
    bazi = result.ba_zi
    print(f"{'年柱':>8} {'月柱':>8} {'日柱':>8} {'时柱':>8}")
    print(f"{str(bazi.year):>8} {str(bazi.month):>8} {str(bazi.day):>8} {str(bazi.hour):>8}")
    
    # 十神
    shi_shen_list = result.get_si_zhu_shi_shen()
    print(f"{shi_shen_to_zh(shi_shen_list[0]):>8} {shi_shen_to_zh(shi_shen_list[1]):>8} {shi_shen_to_zh(shi_shen_list[2]):>8} {shi_shen_to_zh(shi_shen_list[3]):>8}")
    
    # 旬空
    if bazi.xun_kong_1:
        print(f"\n旬空: {bazi.xun_kong_1}{bazi.xun_kong_2}")
    
    print()


def display_da_yun(result: BaZiResult, max_count: int = 5):
    """显示大运信息"""
    print("=" * 60)
    print("【大运信息】")
    print("=" * 60)
    print()
    
    da_yun_system = result.da_yun_system
    print(f"起运年龄: {da_yun_system.qi_yun_age}岁")
    print(f"排运方式: {'顺排' if da_yun_system.shun_pai else '逆排'}")
    print()
    
    da_yun_list = da_yun_system.da_yun_list[:max_count]
    
    print(f"{'干支':<10} {'年龄':<15} {'年份':<20} {'天干十神':<10} {'地支十神':<10}")
    print("-" * 68)
    
    for da_yun in da_yun_list:
        print(f"{str(da_yun.pillar):<10} {da_yun.start_age:>2}-{da_yun.end_age:>2}岁{'':<8} "
              f"{da_yun.start_year}-{da_yun.end_year}年{'':<8} "
              f"{shi_shen_to_zh(da_yun.gan_shi_shen):<10} "
              f"{shi_shen_to_zh(da_yun.zhi_shi_shen):<10}")
    
    print()


def display_liu_nian(result: BaZiResult, start_year: int, count: int):
    """显示流年信息"""
    print("=" * 60)
    print("【流年信息】")
    print("=" * 60)
    print()
    
    print(f"{'年份':<8} {'干支':<8} {'年龄':<8} {'天干十神':<10} {'地支十神':<10}")
    print("-" * 50)
    
    for i in range(count):
        year = start_year + i
        liu_nian = result.get_liu_nian(year)
        
        print(f"{year:<8} {str(liu_nian.pillar):<8} {liu_nian.age}岁{'':<5} "
              f"{shi_shen_to_zh(liu_nian.gan_shi_shen):<10} "
              f"{shi_shen_to_zh(liu_nian.zhi_shi_shen):<10}")
    
    print()


def main():
    """主函数"""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 20 + "八字系统示例演示" + " " * 22 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    try:
        # 示例1：公历排盘
        print("【示例1】公历排盘：2000年7月15日16时（男）")
        print("─" * 60)
        result = BaZiResult.from_solar(2000, 7, 15, 16, is_male=True)
        display_result(result)
        print()
        
        # 示例2：查看详细信息
        print("【示例2】查看八字详细信息")
        print("─" * 60)
        bazi = result.ba_zi
        print(f"年柱：{bazi.year}")
        print(f"月柱：{bazi.month}")
        print(f"日柱：{bazi.day}")
        print(f"时柱：{bazi.hour}")
        print()
        
        # 示例3：查看十神关系
        print("【示例3】十神关系分析")
        print("─" * 60)
        from ganzhi import get_shi_shen
        print(f"年干对日干：{shi_shen_to_zh(get_shi_shen(bazi.day.gan, bazi.year.gan))}")
        print(f"月干对日干：{shi_shen_to_zh(get_shi_shen(bazi.day.gan, bazi.month.gan))}")
        print(f"时干对日干：{shi_shen_to_zh(get_shi_shen(bazi.day.gan, bazi.hour.gan))}")
        print()
        
        # 示例4：查看大运信息
        print("【示例4】大运信息")
        print("─" * 60)
        display_da_yun(result, 5)
        
        # 示例5：查看流年信息
        print("【示例5】流年信息（2020-2025）")
        print("─" * 60)
        display_liu_nian(result, 2020, 6)
        
        # 示例6：不同日期测试
        print("【示例6】不同日期测试：1990年3月5日8时（女）")
        print("─" * 60)
        result2 = BaZiResult.from_solar(1990, 3, 5, 8, is_male=False)
        display_result(result2)
        display_da_yun(result2, 3)
        
        print("✅ 八字系统示例演示完成！")
        print()
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

