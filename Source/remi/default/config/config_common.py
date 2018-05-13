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


class DataTypeBP(Enum):
    Result = (1, "実績")  # journal_voucher
    Budget = (2, "全社予算")  # budget
    Scheduled = (3, "予定仕訳")  # scheduled_journal, repeatable_scheduled_journal, bill, loan
    BizBudget = (4, "営業目標")  # biz_budget
    BizProspect = (5, "見込み")  # biz_prospect
    PlanBase = (6, "基礎")
    PlanOption = (7, "努力")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class AccountDataType(Enum):
    Result = (1, "当年実績")  # journal_voucher
    ResultLastYear = (2, "昨年実績")
    Result3Year = (3, "過去3期平均")
    BudgetBase = (4, "予算・基礎")  # budget
    BudgetOption = (5, "予算・努力")  # budget
    Scheduled = (6, "予定仕訳")  # scheduled_journal, repeatable_scheduled_journal, bill, loan
    BizPlanBase = (7, "業務目標・基礎")  # biz_budget
    BizPlanOption = (8, "業務目標・努力")  # biz_budget
    BizProspect = (9, "見込み")  # biz_prospect

    def __init__(self, code, title):
        self.code = code
        self.title = title

    @staticmethod
    def get_value(code):
        for e in AccountDataType:
            if e.value[0] == code:
                return e.value
        return None


class Tax(Enum):
    Taxed = (0, "課税")
    TaxedFree = (1, "非課税")
    NotCovered = (3, "対象外")

    @staticmethod
    def get_value(code):
        for e in Tax:
            if e.value[0] == code:
                return e.value
        return None


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


class ImportDataType(Enum):
    JournalVoucher = 0  # 会計データ（実績）
    BizBudget = 1  # 営業目標
    BizProspect = 2  # 営業見込み


class TableName(Enum):
    BizBudget = 'biz_budget'
    BizProspect = 'biz_prospect'
    JournalVoucher = 'journal_voucher'
    Budget = 'budget'


class ReferenceDateType(Enum):

    Accrual = (0, "accrual_date")
    Settlement = (1, "settlement_date")

    def __init__(self, code, title):
        self.code = code
        self.title = title

    @staticmethod
    def get_name(code):
        for date_type in ReferenceDateType:
            if date_type.code == code:
                return date_type.title
        return None



class CalculationType(Enum):
    Summary = "sum"  # 指定した子供のアイテムの合計
    SummaryAccount = "sum_account"  # 指定した勘定科目の合計
    Different = "diff"  # 指定した勘定項目の引き算
    PreviousColumn = "precolumn"  # 指定した行番号の前月の値
    Nothing = "nothing"  # 指定した勘定項目の値


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


class AuthBaseDataName(Enum):
    BizBudget = "biz_budget"  # 営業目標
    BizProspect = "biz_prospect"  # 営業見込み
    ImportHistory = "import_history"  # 取込履歴
    Schedule = "scheduled_journal"
    JournalVoucher = "journal_voucher"
    Budget = "budget"
    User = "user"


class BaseDataName(Enum):
    BizBudget = "biz_budget"  # 営業目標
    BizProspect = "biz_prospect"  # 営業見込み
    JournalVoucher = "journal_voucher"  # 営業見込み


class MetaTypeDefine(Enum):
    Partner = (1, "partner")
    Staff = (2, "staff")
    Product = (3, "product")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class AuthMetaTypeDefine(Enum):
    Department = (1, "department")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class ProspectTypeDefine(Enum):
    Revenue = (0, "売上")
    Outsourcing = (1, "外注")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class CashFlowTableIdDefine(Enum):
    PreviousMonth = (50, "前月繰越")
    CurrentsAmount = (200, "収支")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class InternalAccountDefine(Enum):
    Revenue = (8100, "売上")  # 8100
    Outsourcing = (8223, "外注")  # 8300
    CostOfSales = (1000, "売上原価")  # 8200
    BusinessDevelopmentCost = (1001, "事業開発部売上原価")
    OverseasPurchase = (1002, "海外仕入")
    DomesticPurchase = (1003, "国内仕入")
    SpecialDomesticPurchase = (1004, "国内仕入（特殊）")

    def __init__(self, code, title):
        self.code = code
        self.title = title


prospect_type_account_id_map = {
    ProspectTypeDefine.Revenue.code: InternalAccountDefine.Revenue.code,
    ProspectTypeDefine.Outsourcing.code: InternalAccountDefine.Outsourcing.code,
}

account_id_prospect_type_map = {v: k for k, v in prospect_type_account_id_map.items()}


class InternalAccountList(Enum):
    IncomeAccounts = (InternalAccountDefine.Revenue.code, InternalAccountDefine.DomesticPurchase.code,
                      InternalAccountDefine.OverseasPurchase.code,
                      InternalAccountDefine.SpecialDomesticPurchase.code, ProspectTypeDefine.Revenue.code)
    OutcomeAccounts = (InternalAccountDefine.Outsourcing.code,
                       InternalAccountDefine.CostOfSales.code,
                       InternalAccountDefine.BusinessDevelopmentCost.code, ProspectTypeDefine.Outsourcing.code)


class InternalAccountParentMap(Enum):
    Outsourcing = [InternalAccountDefine.Outsourcing.code,
                   (InternalAccountDefine.CostOfSales.code, InternalAccountDefine.BusinessDevelopmentCost.code)]

    Revenue = [InternalAccountDefine.Revenue.code,
               (InternalAccountDefine.OverseasPurchase.code,
                InternalAccountDefine.DomesticPurchase.code,
                InternalAccountDefine.SpecialDomesticPurchase.code)]


class FiscalStatus(Enum):
    Possible = (0, '可能')
    Impossible = (1, '不可能')


LAST_IMPORT_DATE = datetime(2015, 12, 12)
