# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import JSONEncoder
from collections import OrderedDict


def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)
_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default  # Replacement


class AccountTotal(object):
    """
    Define account info which account id, data type and 12 months amount.
    Data type is define as AccountDataType

    """
    account_id = None
    data_type = None
    amount_list = []

    def __init__(self, account_id=None, data_type=None):
        self.amount_list = []
        self.account_id = account_id
        self.data_type = data_type

    def to_json(self):
        ret = self.__dict__.copy()
        ret['amount_list'] = []
        for amount in self.amount_list:
            ret['amount_list'].append(amount.to_json())
        return ret

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{0}: {1}".format(self.account_id, self.data_type)


class Amount(object):
    """
    Define amount of an entry of account total.
    It have value of each stage of opportunity
    """
    each_stage = []
    no_stage = 0

    def __init__(self, no_stage=0):
        self.each_stage = []
        self.no_stage = no_stage

    def to_json(self):
        ret = self.__dict__.copy()
        ret['each_stage'] = []
        for stage in self.each_stage:
            ret['each_stage'].append(stage)
        return ret


class TableMonthEntry(object):
    """
    Define an entry of table at o month.
    I have data type (AccountDataType) and amount
    """
    data_type = 0
    amount = 0

    def __init__(self, data_type=0, amount=0):
        """

        @rtype: TableMonthEntry
        """
        self.data_type = data_type
        self.amount = amount

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class TableAccountEntry(object):
    """
    One row of cash flow, budget performance table
    """

    table_define_id = 0
    account_calculation_type = ''
    account_calculation_args = []
    account_id = 0
    depth = 0
    parent_id = 0
    title = None
    children = []
    data = OrderedDict()
    style = ''
    level1 = ''
    level2 = ''

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{0} {1} {2}".format(self.title, self.parent_id, self.depth)

    def __init__(self):
        self.table_define_id = 0
        self.account_calculation_type = ''
        self.account_calculation_args = []
        self.account_id = 0
        self.depth = 0
        self.parent_id = 0
        self.hidden = False
        self.title = None
        self.children = []
        self.data = OrderedDict()

    def to_json(self):
        ret = self.__dict__.copy()
        ret['children'] = self.children.copy()
        ret['data'] = self.data.copy()

        return ret


class JournalVoucherResponse(object):

    date = None
    account_id = None
    data_type = None
    side = None
    amount = None
    tax = None
    reference = None
    accuracy = None
    opportunity_stage = None
    is_prospect = False

    def __init__(self):
        self.date = None
        self.account_id = None
        self.data_type = None
        self.side = None
        self.amount = None
        self.tax = None
        self.reference = None
        self.accuracy = None
        self.opportunity_stage = None
        self.is_prospect = False

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class CashFlowTableResponse:

    period_list = []
    account_totals = []
    table_definitions = []
    cash_balance = None
    last_import_date = None

    def __init__(self):
        self.period_list = []
        self.account_totals = []
        self.table_definitions = []
        self.cash_balance = None
        self.last_import_date = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class TableDefinitionResponse(object):

    id = None
    depth = None
    parent = None
    title = None
    type = None
    color = None
    account = None
    calculation = None
    type = None

    def __init__(self):
        self.id = None
        self.depth = None
        self.parent = None
        self.title = None
        self.type = None
        self.color = None
        self.account = None
        self.calculation = None
        self.type = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class Calculation(object):
    type = None
    args = []

    def __init__(self):
        self.type = None
        self.args = []

    def to_json(self):
        ret = self.__dict__.copy()
        ret['args'] = []
        for arg in self.args:
            ret['args'].append(arg)
        return ret


class FiscalPeriodResponse(object):

    id = None
    term_number = None
    name = None
    start_date = None
    end_date = None

    def __init__(self):
        self.id = None
        self.term_number = None
        self.name = None
        self.start_date = None
        self.end_date = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class BizBudgetTotalResponse(object):

    target_id = None
    target_period = None
    title = None
    biz_budget_base = None
    biz_budget_option = None
    result = None
    # List Integer
    each_stage = []
    # List of BizJournalResponse
    biz_journal_list = []

    def __init__(self):
        self.target_id = None
        self.target_period = None
        self.title = None
        self.biz_budget_base = None
        self.biz_budget_option = None
        self.result = None
        # List Integer
        self.each_stage = []
        # List of BizJournalResponse
        self.biz_journal_list = []

    def to_json(self):
        ret = self.__dict__.copy()
        ret['each_stage'] = []
        ret['biz_journal_list'] = []
        for arg in self.each_stage:
            ret['each_stage'].append(arg)
        for arg in self.biz_journal_list:
            ret['biz_journal_list'].append(arg)
        return ret


class BizBudgetJournalResponse(object):

    data_type = None
    amount = None
    reference = None
    accuracy = None
    opportunity_stage = None
    # Date
    accrual_date = None
    # Date
    settlement_date = None
    # List of MetaDataResponse
    meta_list = []

    def __init__(self):
        self.data_type = None
        self.amount = None
        self.reference = None
        self.accuracy = None
        self.opportunity_stage = None
        # Date
        self.accrual_date = None
        # Date
        self.settlement_date = None
        # List of MetaDataResponse
        self.meta_list = []

    def to_json(self):
        from helper.util import Format
        ret = self.__dict__.copy()
        ret['accrual_date'] = Format.format_date(ret['accrual_date'])
        ret['settlement_date'] = Format.format_date(ret['settlement_date'])
        ret['meta_list'] = []
        for arg in self.meta_list:
            ret['meta_list'].append(arg)
        return ret


class MetaDataResponse(object):
    key = None
    value = None

    def __init__(self):
        self.key = None
        self.value = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret

    @staticmethod
    def create_meta_data_list(meta_dict):
        """
        @type meta_dict: dict
        @param meta_dict: 
        @return: 
        """
        meta_data_list = []
        if meta_dict is None or len(meta_dict) == 0:
            return meta_data_list

        for key, rel_list in meta_dict.items():
            for rel in rel_list:
                meta = MetaDataResponse()
                meta.key = rel.info.type
                meta.value = rel.info.value
                meta_data_list.append(meta)

        return meta_data_list


class BaseDataMetaRelResponse(object):
    id = None
    base_data_name = None
    base_id = None
    # MetaInfoResponse
    info = None

    def __init__(self):
        self.id = None
        self.base_data_name = None
        self.base_id = None
        self.info = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret


class MetaInfoResponse:

    id = -1  # はマスタへの存在の有無が不明を表す
    # MetaTypeResponse
    type = None
    value = None

    def __init__(self):
        self.id = -1
        self.type = None
        self.value = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret

class CourseInfo:

    title = None
    id = None
    image_link = None

    def __init__(self):
        self.title = ""
        self.id = -1
        self.image_link = ""

    def to_json(self):
        ret = self.__dict__.copy()
        return ret

class MetaTypeResponse:

    id = None
    type = None
    disp = None
    grouping_target = None
    restriction = None

    def __init__(self):
        self.id = None
        self.type = None
        self.disp = None
        self.grouping_target = None
        self.restriction = None

    def to_json(self):
        ret = self.__dict__.copy()
        return ret

