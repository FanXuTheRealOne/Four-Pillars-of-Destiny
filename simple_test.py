#!/usr/bin/env python3
"""
简单的八字测试程序
直接修改下面的参数测试你的八字
"""
from bazi import BaZiResult
from ganzhi import shi_shen_to_zh


# ==================== 修改这里的参数 ====================
出生年 = 1996
出生月 = 6
出生日 = 21
出生时 = 21  # 24小时制，例如：16表示下午4点
性别 = True  # True=男，False=女
# ======================================================


def main():
    print()
    print("=" * 60)
    print(f"正在计算八字排盘...")
    print(f"出生日期：{出生年}年{出生月}月{出生日}日 {出生时}时")
    print(f"性别：{'男' if 性别 else '女'}")
    print("=" * 60)
    print()
    
    # 计算八字
    result = BaZiResult.from_solar(出生年, 出生月, 出生日, 出生时, is_male=性别)
    bazi = result.ba_zi
    
    # 显示四柱
    print("【四柱八字】")
    print(f"年柱：{bazi.year}")
    print(f"月柱：{bazi.month}")
    print(f"日柱：{bazi.day}")
    print(f"时柱：{bazi.hour}")
    if bazi.xun_kong_1:
        print(f"旬空：{bazi.xun_kong_1}{bazi.xun_kong_2}")
    print()
    
    # 显示十神
    print("【十神】")
    shi_shen_list = result.get_si_zhu_shi_shen()
    print(f"年干：{shi_shen_to_zh(shi_shen_list[0])}")
    print(f"月干：{shi_shen_to_zh(shi_shen_list[1])}")
    print(f"日干：{shi_shen_to_zh(shi_shen_list[2])}")
    print(f"时干：{shi_shen_to_zh(shi_shen_list[3])}")
    print()
    
    # 显示大运
    print("【大运】")
    da_yun_system = result.da_yun_system
    print(f"起运年龄：{da_yun_system.qi_yun_age}岁")
    print(f"排运方式：{'顺排' if da_yun_system.shun_pai else '逆排'}")
    print()
    print("前5个大运：")
    for i, da_yun in enumerate(da_yun_system.da_yun_list[:5], 1):
        print(f"  {i}. {da_yun.pillar} ({da_yun.start_age}-{da_yun.end_age}岁, "
              f"{da_yun.start_year}-{da_yun.end_year}年) "
              f"天干{shi_shen_to_zh(da_yun.gan_shi_shen)}/地支{shi_shen_to_zh(da_yun.zhi_shi_shen)}")
    print()
    
    # 显示最近流年
    import datetime
    current_year = datetime.datetime.now().year
    print(f"【流年】（{current_year-2}年-{current_year+2}年）")
    for year in range(current_year - 2, current_year + 3):
        liu_nian = result.get_liu_nian(year)
        marker = " ← 今年" if year == current_year else ""
        print(f"  {year}年：{liu_nian.pillar} ({liu_nian.age}岁) "
              f"天干{shi_shen_to_zh(liu_nian.gan_shi_shen)}/地支{shi_shen_to_zh(liu_nian.zhi_shi_shen)}{marker}")
    print()
    
    print("=" * 60)
    print("✅ 八字排盘完成！")
    print()


if __name__ == "__main__":
    main()

