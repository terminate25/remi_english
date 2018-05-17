# -*- coding: utf-8 -*-
from enum import Enum
from datetime import datetime

"""
All of constant is define here
"""


class BaseOptionDefine(Enum):
    Base = (0, "基礎")
    Option = (1, "努力")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class TestResult(Enum):
    Failed = (0, "Failed")
    Done = (1, "Passed")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class AccountType(Enum):
    Strategy = (0, "戦略科目")
    InterLocking = (1, "連動科目")
    Expenses = (2, "経費系科目")
    Other = (3, "その他")

    def __init__(self, code, title):
        self.code = code
        self.title = title

    @staticmethod
    def get_value(code):
        """
        Enum format: name = value(code,title)
        Return value
        """
        for e in AccountType:
            if e.value[0] == code:
                return e.value
        return None


class SideDefine(Enum):
    Debit = (0, "借方")  # 借方
    Credit = (1, "貸方")  # 貸方

    def __init__(self, code, title):
        self.code = code
        self.title = title

    @staticmethod
    def get(code):
        """
        Return enum: SideDefine.Debit or SideDefine.Credit
        @param code:
        @return:
        """
        for e in SideDefine:
            if e.code == code:
                return e
        return None


class AccountClass(Enum):
    Assets = (0, "資産", SideDefine.Debit)
    Liabilities = (1, "負債", SideDefine.Credit)
    Equity = (2, "資本", SideDefine.Credit)
    Revenues = (3, "収益", SideDefine.Credit)
    Expenses = (4, "費用", SideDefine.Debit)

    def __init__(self, code, title, side):
        self.code = code
        self.title = title
        self.side = side

    @staticmethod
    def get_value(code):
        for e in AccountClass:
            if e.value[0] == code:
                return e.value
        return None


class TableAccountDataType(Enum):
    Percentage = (-1, "達成率")
    Hidden = (-99, "表示しない")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class OpportunityStage(Enum):
    NotAttempt = (0, 'C')
    Attempting = (1, 'B')
    Proposal = (2, 'A')
    Close = (3, '')
    ClosedLast = (4, '')

    def __init__(self, code, title):
        self.code = code
        self.title = title

    @staticmethod
    def get_value(code):
        for e in OpportunityStage:
            if e.value == code:
                return e.value
        return None

    @staticmethod
    def get_title(code):
        for acc in OpportunityStage:
            if acc.code == code:
                return acc.title
        return None


class CashFlow(Enum):
    DefaultPeriodLimit = 12


class ColumnDefine(Enum):
    Id = 1
    Account = 2
    Parent = 3
    Depth = 4
    CalculationType = 5
    Argument = 6
    Title = 7
    Color = 8
    Hidden = 99

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


LAST_IMPORT_DATE = datetime(2015, 12, 12)
