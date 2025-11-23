"""
八字系统主模块
实现八字排盘、大运、流年等功能
"""
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
from ganzhi import (
    TianGan, DiZhi, ShiShen,
    gan_to_zh, zhi_to_zh, shi_shen_to_zh,
    get_shi_shen, get_cang_gan, get_xun_kong,
    get_gan_yin_yang, YinYang
)
from lunarcal import calculate_bazi, jiazi_from_index, get_sixty_jiazi_index


# ==================== 数据结构 ====================

@dataclass
class Pillar:
    """干支柱"""
    gan: TianGan
    zhi: DiZhi
    
    def __str__(self) -> str:
        return f"{gan_to_zh(self.gan)}{zhi_to_zh(self.zhi)}"
    
    @classmethod
    def from_tuple(cls, t: Tuple[TianGan, DiZhi]):
        return cls(gan=t[0], zhi=t[1])


@dataclass
class BaZi:
    """四柱八字"""
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    xun_kong_1: str
    xun_kong_2: str
    
    @classmethod
    def from_solar(cls, year: int, month: int, day: int, hour: int):
        """从公历创建八字"""
        bazi_data = calculate_bazi(year, month, day, hour)
        
        year_pillar = Pillar.from_tuple(bazi_data['year'])
        month_pillar = Pillar.from_tuple(bazi_data['month'])
        day_pillar = Pillar.from_tuple(bazi_data['day'])
        hour_pillar = Pillar.from_tuple(bazi_data['hour'])
        
        # 计算旬空
        kong1, kong2 = get_xun_kong(day_pillar.gan, day_pillar.zhi)
        
        return cls(
            year=year_pillar,
            month=month_pillar,
            day=day_pillar,
            hour=hour_pillar,
            xun_kong_1=zhi_to_zh(kong1),
            xun_kong_2=zhi_to_zh(kong2)
        )


@dataclass
class DaYun:
    """大运信息"""
    pillar: Pillar
    start_age: int
    end_age: int
    start_year: int
    end_year: int
    gan_shi_shen: ShiShen
    zhi_shi_shen: ShiShen
    
    def __str__(self) -> str:
        return f"{self.pillar}({self.start_age}-{self.end_age}岁 {self.start_year}-{self.end_year}年)"
    
    def contains_age(self, age: int) -> bool:
        """判断年龄是否在此大运范围内"""
        return self.start_age <= age <= self.end_age


@dataclass
class LiuNian:
    """流年信息"""
    year: int
    pillar: Pillar
    age: int
    gan_shi_shen: ShiShen
    zhi_shi_shen: ShiShen
    
    def __str__(self) -> str:
        return f"{self.year}年 {self.pillar} ({self.age}岁)"


# ==================== 大运系统 ====================

class DaYunSystem:
    """大运系统"""
    
    def __init__(self, bazi: BaZi, is_male: bool, birth_year: int):
        self.bazi = bazi
        self.is_male = is_male
        self.birth_year = birth_year
        
        # 判断年柱天干阴阳
        yang_year = (get_gan_yin_yang(bazi.year.gan) == YinYang.YANG)
        
        # 阳男阴女顺排，阴男阳女逆排
        self.shun_pai = (is_male == yang_year)
        
        # 起运年龄（简化：固定为3岁，实际应根据节气计算）
        self.qi_yun_age = 3
        
        # 生成大运列表
        self.da_yun_list = self._generate_da_yun_list(10)
    
    def _generate_da_yun_list(self, count: int) -> List[DaYun]:
        """生成大运列表"""
        result = []
        
        # 从月柱开始推算
        current_gan = self.bazi.month.gan
        current_zhi = self.bazi.month.zhi
        
        current_age = self.qi_yun_age
        current_year = self.birth_year + self.qi_yun_age
        
        for i in range(count):
            # 前进或后退一柱
            if self.shun_pai:
                # 顺排：干支都加1
                current_gan = TianGan((current_gan + 1) % 10)
                current_zhi = DiZhi((current_zhi + 1) % 12)
            else:
                # 逆排：干支都减1
                current_gan = TianGan((current_gan + 9) % 10)
                current_zhi = DiZhi((current_zhi + 11) % 12)
            
            pillar = Pillar(current_gan, current_zhi)
            
            # 计算十神
            gan_shi_shen = get_shi_shen(self.bazi.day.gan, current_gan)
            cang_gan = get_cang_gan(current_zhi)
            zhi_shi_shen = get_shi_shen(self.bazi.day.gan, cang_gan[0])
            
            da_yun = DaYun(
                pillar=pillar,
                start_age=current_age,
                end_age=current_age + 9,
                start_year=current_year,
                end_year=current_year + 9,
                gan_shi_shen=gan_shi_shen,
                zhi_shi_shen=zhi_shi_shen
            )
            
            result.append(da_yun)
            
            current_age += 10
            current_year += 10
        
        return result
    
    def get_da_yun_by_age(self, age: int) -> Optional[DaYun]:
        """根据年龄获取当前大运"""
        for da_yun in self.da_yun_list:
            if da_yun.contains_age(age):
                return da_yun
        return None


# ==================== 流年系统 ====================

def create_liu_nian(year: int, birth_year: int, day_gan: TianGan) -> LiuNian:
    """创建流年"""
    # 从年份获取干支（简化：使用年中7月1日）
    bazi_data = calculate_bazi(year, 7, 1, 12)
    year_pillar = Pillar.from_tuple(bazi_data['year'])
    
    # 计算虚岁
    age = year - birth_year + 1
    
    # 计算十神
    gan_shi_shen = get_shi_shen(day_gan, year_pillar.gan)
    cang_gan = get_cang_gan(year_pillar.zhi)
    zhi_shi_shen = get_shi_shen(day_gan, cang_gan[0])
    
    return LiuNian(
        year=year,
        pillar=year_pillar,
        age=age,
        gan_shi_shen=gan_shi_shen,
        zhi_shi_shen=zhi_shi_shen
    )


# ==================== 八字排盘结果 ====================

@dataclass
class BaZiResult:
    """完整八字排盘结果"""
    ba_zi: BaZi
    is_male: bool
    birth_year: int
    birth_month: int
    birth_day: int
    birth_hour: int
    da_yun_system: DaYunSystem
    
    @classmethod
    def from_solar(cls, year: int, month: int, day: int, hour: int, is_male: bool):
        """从公历创建八字结果"""
        ba_zi = BaZi.from_solar(year, month, day, hour)
        da_yun_system = DaYunSystem(ba_zi, is_male, year)
        
        return cls(
            ba_zi=ba_zi,
            is_male=is_male,
            birth_year=year,
            birth_month=month,
            birth_day=day,
            birth_hour=hour,
            da_yun_system=da_yun_system
        )
    
    def get_liu_nian(self, year: int) -> LiuNian:
        """获取指定年份的流年"""
        return create_liu_nian(year, self.birth_year, self.ba_zi.day.gan)
    
    def get_current_da_yun(self, age: int) -> Optional[DaYun]:
        """获取当前年龄的大运"""
        return self.da_yun_system.get_da_yun_by_age(age)
    
    def get_si_zhu_shi_shen(self) -> List[ShiShen]:
        """获取四柱十神"""
        day_gan = self.ba_zi.day.gan
        return [
            get_shi_shen(day_gan, self.ba_zi.year.gan),
            get_shi_shen(day_gan, self.ba_zi.month.gan),
            get_shi_shen(day_gan, self.ba_zi.day.gan),
            get_shi_shen(day_gan, self.ba_zi.hour.gan)
        ]

