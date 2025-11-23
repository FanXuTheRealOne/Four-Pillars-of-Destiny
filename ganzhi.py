"""
天干地支系统
提供天干地支的枚举和相关运算
"""
from enum import IntEnum
from typing import List, Optional, Tuple


# ==================== 枚举定义 ====================

class TianGan(IntEnum):
    """天干枚举"""
    JIA = 0   # 甲
    YI = 1    # 乙
    BING = 2  # 丙
    DING = 3  # 丁
    WU = 4    # 戊
    JI = 5    # 己
    GENG = 6  # 庚
    XIN = 7   # 辛
    REN = 8   # 壬
    GUI = 9   # 癸


class DiZhi(IntEnum):
    """地支枚举"""
    ZI = 0    # 子
    CHOU = 1  # 丑
    YIN = 2   # 寅
    MAO = 3   # 卯
    CHEN = 4  # 辰
    SI = 5    # 巳
    WU = 6    # 午
    WEI = 7   # 未
    SHEN = 8  # 申
    YOU = 9   # 酉
    XU = 10   # 戌
    HAI = 11  # 亥


class WuXing(IntEnum):
    """五行枚举"""
    MU = 1    # 木
    HUO = 2   # 火
    TU = 3    # 土
    JIN = 4   # 金
    SHUI = 5  # 水


class YinYang(IntEnum):
    """阴阳枚举"""
    YIN = 0   # 阴
    YANG = 1  # 阳


class ShiShen(IntEnum):
    """十神枚举"""
    BI_JIAN = 0     # 比肩
    JIE_CAI = 1     # 劫财
    SHI_SHEN = 2    # 食神
    SHANG_GUAN = 3  # 伤官
    PIAN_CAI = 4    # 偏财
    ZHENG_CAI = 5   # 正财
    QI_SHA = 6      # 七杀
    ZHENG_GUAN = 7  # 正官
    PIAN_YIN = 8    # 偏印
    ZHENG_YIN = 9   # 正印


# ==================== 中文名称映射 ====================

TIAN_GAN_ZH = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI_ZH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
WU_XING_ZH = ["", "木", "火", "土", "金", "水"]
YIN_YANG_ZH = ["阴", "阳"]
SHENG_XIAO_ZH = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
SHI_SHEN_ZH = ["比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"]


def gan_to_zh(gan: TianGan) -> str:
    """天干转中文"""
    return TIAN_GAN_ZH[gan]


def zhi_to_zh(zhi: DiZhi) -> str:
    """地支转中文"""
    return DI_ZHI_ZH[zhi]


def wu_xing_to_zh(wx: WuXing) -> str:
    """五行转中文"""
    return WU_XING_ZH[wx]


def yin_yang_to_zh(yy: YinYang) -> str:
    """阴阳转中文"""
    return YIN_YANG_ZH[yy]


def shi_shen_to_zh(ss: ShiShen) -> str:
    """十神转中文"""
    return SHI_SHEN_ZH[ss]


def zh_to_gan(zh: str) -> Optional[TianGan]:
    """中文转天干"""
    try:
        return TianGan(TIAN_GAN_ZH.index(zh))
    except ValueError:
        return None


def zh_to_zhi(zh: str) -> Optional[DiZhi]:
    """中文转地支"""
    try:
        return DiZhi(DI_ZHI_ZH.index(zh))
    except ValueError:
        return None


# ==================== 五行属性 ====================

def get_gan_wu_xing(gan: TianGan) -> WuXing:
    """获取天干五行"""
    wu_xing_map = [
        WuXing.MU, WuXing.MU,      # 甲乙木
        WuXing.HUO, WuXing.HUO,    # 丙丁火
        WuXing.TU, WuXing.TU,      # 戊己土
        WuXing.JIN, WuXing.JIN,    # 庚辛金
        WuXing.SHUI, WuXing.SHUI   # 壬癸水
    ]
    return wu_xing_map[gan]


def get_zhi_wu_xing(zhi: DiZhi) -> WuXing:
    """获取地支五行"""
    wu_xing_map = [
        WuXing.SHUI,                # 子水
        WuXing.TU,                  # 丑土
        WuXing.MU, WuXing.MU,       # 寅卯木
        WuXing.TU,                  # 辰土
        WuXing.HUO, WuXing.HUO,     # 巳午火
        WuXing.TU,                  # 未土
        WuXing.JIN, WuXing.JIN,     # 申酉金
        WuXing.TU,                  # 戌土
        WuXing.SHUI                 # 亥水
    ]
    return wu_xing_map[zhi]


# ==================== 阴阳属性 ====================

def get_gan_yin_yang(gan: TianGan) -> YinYang:
    """获取天干阴阳"""
    return YinYang.YANG if gan % 2 == 0 else YinYang.YIN


def get_zhi_yin_yang(zhi: DiZhi) -> YinYang:
    """获取地支阴阳"""
    return YinYang.YANG if zhi % 2 == 0 else YinYang.YIN


# ==================== 五行生克关系 ====================

def wu_xing_sheng(x: WuXing, y: WuXing) -> bool:
    """判断五行相生（x生y）"""
    sheng_map = {
        (WuXing.MU, WuXing.HUO): True,   # 木生火
        (WuXing.HUO, WuXing.TU): True,   # 火生土
        (WuXing.TU, WuXing.JIN): True,   # 土生金
        (WuXing.JIN, WuXing.SHUI): True, # 金生水
        (WuXing.SHUI, WuXing.MU): True   # 水生木
    }
    return sheng_map.get((x, y), False)


def wu_xing_ke(x: WuXing, y: WuXing) -> bool:
    """判断五行相克（x克y）"""
    ke_map = {
        (WuXing.MU, WuXing.TU): True,    # 木克土
        (WuXing.TU, WuXing.SHUI): True,  # 土克水
        (WuXing.SHUI, WuXing.HUO): True, # 水克火
        (WuXing.HUO, WuXing.JIN): True,  # 火克金
        (WuXing.JIN, WuXing.MU): True    # 金克木
    }
    return ke_map.get((x, y), False)


# ==================== 地支藏干 ====================

def get_cang_gan(zhi: DiZhi) -> List[TianGan]:
    """获取地支藏干（主气、中气、余气）"""
    cang_gan_table = {
        DiZhi.ZI: [TianGan.GUI],
        DiZhi.CHOU: [TianGan.JI, TianGan.GUI, TianGan.XIN],
        DiZhi.YIN: [TianGan.JIA, TianGan.BING, TianGan.WU],
        DiZhi.MAO: [TianGan.YI],
        DiZhi.CHEN: [TianGan.WU, TianGan.YI, TianGan.GUI],
        DiZhi.SI: [TianGan.BING, TianGan.WU, TianGan.GENG],
        DiZhi.WU: [TianGan.DING, TianGan.JI],
        DiZhi.WEI: [TianGan.JI, TianGan.DING, TianGan.YI],
        DiZhi.SHEN: [TianGan.GENG, TianGan.REN, TianGan.WU],
        DiZhi.YOU: [TianGan.XIN],
        DiZhi.XU: [TianGan.WU, TianGan.XIN, TianGan.DING],
        DiZhi.HAI: [TianGan.REN, TianGan.JIA]
    }
    return cang_gan_table[zhi]


# ==================== 十神计算 ====================

def get_shi_shen(day_gan: TianGan, other_gan: TianGan) -> ShiShen:
    """获取十神关系（以日干为我）"""
    day_wx = get_gan_wu_xing(day_gan)
    other_wx = get_gan_wu_xing(other_gan)
    day_yy = get_gan_yin_yang(day_gan)
    other_yy = get_gan_yin_yang(other_gan)
    same_yy = (day_yy == other_yy)
    
    if day_wx == other_wx:
        # 比和
        return ShiShen.BI_JIAN if same_yy else ShiShen.JIE_CAI
    elif wu_xing_sheng(day_wx, other_wx):
        # 我生者
        return ShiShen.SHI_SHEN if same_yy else ShiShen.SHANG_GUAN
    elif wu_xing_ke(day_wx, other_wx):
        # 我克者
        return ShiShen.PIAN_CAI if same_yy else ShiShen.ZHENG_CAI
    elif wu_xing_ke(other_wx, day_wx):
        # 克我者
        return ShiShen.QI_SHA if same_yy else ShiShen.ZHENG_GUAN
    else:
        # 生我者
        return ShiShen.PIAN_YIN if same_yy else ShiShen.ZHENG_YIN


# ==================== 旬空计算 ====================

def get_xun_kong(day_gan: TianGan, day_zhi: DiZhi) -> Tuple[DiZhi, DiZhi]:
    """获取旬空（空亡）的两个地支"""
    # 计算旬首地支
    xun_shou_idx = (day_zhi - day_gan + 12) % 12
    # 旬空为旬首前两位
    kong1 = DiZhi((xun_shou_idx - 2 + 12) % 12)
    kong2 = DiZhi((xun_shou_idx - 1 + 12) % 12)
    return (kong1, kong2)

