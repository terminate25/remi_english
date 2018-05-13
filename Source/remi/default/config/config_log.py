# -*- coding: utf-8 -*-
from enum import Enum


class LogModule(Enum):
    """
    Log module name, which save in log database
    """
    User = "user"
    MetaType = "meta_type"
    MetaData = "meta_data"
    AuthMetaType = "auth_meta_type"
    AuthMetaData = "auth_meta_data"
    Budget = "budget"
    BizBudget = "biz_budget"
    BizProspect = "biz_prospect"
    Account = "account"
    Fiscal = "fiscal"
    JournalVoucher = "journal_voucher"


class LogResult(Enum):
    Success = 0
    Fail = 1


class LogType(Enum):
    """
    Log type
    """
    view = "view"
    Insert = "insert"
    Update = "update"
    Delete = "delete"
    Download = "download"
    Merge = "merge"
