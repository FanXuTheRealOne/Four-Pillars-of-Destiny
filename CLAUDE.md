# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for Chinese BaZi (八字, Four Pillars of Destiny) calculation based on the `cnlunar` library. It provides accurate calculation of:
- Year Pillar (年柱) - based on Lichun solar term
- Month Pillar (月柱) - based on solar terms
- Day Pillar (日柱) - based on Julian day
- Hour Pillar (时柱) - based on Wu Shu Dun (五鼠遁) method with early/late Zi hour handling

## Development Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install cnlunar
```

## Running the Code

```bash
# Run the main calculator with comprehensive test cases (50 tests)
python3 bazi_calculator_complete.py

# Run usage examples (demonstrates API usage)
python3 example_usage.py
```

## Architecture

The codebase consists of two main files:

### Core Module: `bazi_calculator_complete.py`

**Key Classes:**
- `Pillar`: Represents a single pillar (干支对) with `gan` (天干) and `zhi` (地支)
- `BaZi`: Represents the complete Four Pillars with year, month, day, and hour pillars
- `BaZiCalculator`: Main calculator that wraps the `cnlunar.Lunar` object and extracts pillar data

**Calculation Flow:**
1. Initialize `Lunar` object from `cnlunar` library with datetime
2. Extract pre-calculated values from `cnlunar`:
   - `lunar.year8Char` → year pillar
   - `lunar.month8Char` → month pillar
   - `lunar.day8Char` → day pillar
   - `lunar.twohour8Char` → hour pillar
3. Wrap values in `Pillar` objects and return as `BaZi` instance

**Important:** This library is a wrapper around `cnlunar` - the actual calendar calculations (solar terms, Julian day conversion, Wu Shu Dun) are handled by `cnlunar`. Our code provides a cleaner API and type-safe object model.

### Example Module: `example_usage.py`

Demonstrates five usage patterns:
1. Basic usage with convenience function
2. Using datetime objects directly
3. Accessing detailed information and converting to dict
4. Handling early vs late Zi hour (子时) edge cases
5. Solar term boundary handling (e.g., Lichun for year calculation)

## Dependency: cnlunar Library

- **License:** MIT License (commercial use allowed)
- **Repository:** https://github.com/OPN48/cnlunar
- **Key Requirement:** Include copyright notice and MIT license text when distributing
- The library handles complex Chinese calendar calculations including 24 solar terms, which are critical for accurate BaZi calculation

## Testing

The main module includes 50 comprehensive test cases covering:
- Different time periods (1900-2026)
- All 12 months
- All 12 time periods (时辰)
- Special cases: leap years (闰年), month boundaries, solar term boundaries
- Edge cases: early/late Zi hour (早晚子时), Lichun boundary

Run tests via: `python3 bazi_calculator_complete.py`

## API Usage Patterns

```python
# Quick calculation
from bazi_calculator_complete import calculate_bazi
bazi = calculate_bazi(1990, 1, 1, 0, 0)

# With datetime object
from bazi_calculator_complete import BaZiCalculator
import datetime
calculator = BaZiCalculator(datetime.datetime(1990, 1, 1, 0, 0))
bazi = calculator.calculate()

# Access individual pillars
print(bazi.year_pillar.gan)   # 天干
print(bazi.year_pillar.zhi)   # 地支
print(bazi.year_pillar.ganzhi) # 干支

# Get all eight characters
year_gan, year_zhi, month_gan, month_zhi, day_gan, day_zhi, hour_gan, hour_zhi = bazi.get_eight_chars()

# Convert to dict for JSON serialization
bazi_dict = bazi.to_dict()
```

## Critical Edge Cases

1. **Zi Hour (子时) Handling:** 23:00-00:59 is Zi hour, but day changes at 00:00
   - 23:00-23:59 (late Zi/晚子时): belongs to current day
   - 00:00-00:59 (early Zi/早子时): belongs to current day but is start of new calendar day

2. **Solar Term Boundaries:** Year pillar changes at Lichun (立春), not January 1st
   - Before Lichun: use previous year's pillar
   - After Lichun: use current year's pillar

3. **Month Boundaries:** Month pillar changes at solar terms, not calendar month boundaries

## Commercial Use

This code can be deployed in commercial applications. Requirements:
- Include acknowledgment of `cnlunar` library usage
- Include MIT License text for `cnlunar`
- Attribute original author (OPN48)
