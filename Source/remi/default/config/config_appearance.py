# -*- coding: utf-8 -*-
from enum import Enum


class AppearanceConfig(Enum):
    """
    System name and company name config
    """
    CompanyName = "Lag solutions"
    SystemName = "Remi English"


class LocalizeFormat(Enum):
    """
    Config the way show date, number

    """
    Language = "ja"  #
    DatePickerCalendarTitleFormat = "yyyy年mm月"  # "EE年mm月"
    DatePickerCalendarYearViewFormat = "yyyy"  # "EE"

    # 注意：DateFormatとPythonDateTimeFormatを合わせることが必要です。
    # 例えば片方和暦、片方西暦にすると、日付処理が正しくなくなります。
    DateFormat = "yyyy/mm/dd"  # "EE.mm.dd"
    PythonDateTimeFormat = "%Y/%m/%d %I:%M %p"  # "%o%E.%m.%d %I:%M %p"
    PythonDateFormat = "%Y/%m/%d"  # "%O%E.%m.%d"
    PythonTimeFormat = "%I:%M %p"

    NumberFormat = ""
    MinuteStep = 15
    ShowSecond = False
    ShowMeridian = True
    MeridianAM = "AM"  # "午前"
    MeridianPM = "PM"  # "午後"

