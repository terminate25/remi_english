from enum import Enum
"""
All of message are defined here
"""

class MetaTypeMessage(Enum):
    UpdateError = "An error occurred. The MetaType could not be updated."
    DeleteError = "An error occurred. The MetaType could not be deleted."
    InsertError = "An error occurred. The MetaType could not be inserted."
    MergeError = "An error occurred. The MetaType could not be merged."
    AllowDeleteError = "Not allowed to delete this MetaType."


class MetaInfoMessage(Enum):
    UpdateError = "An error occurred. The MetaInfo could not be updated."
    DeleteError = "An error occurred. The MetaInfo could not be deleted."
    InsertError = "An error occurred. The MetaInfo could not be inserted."


class AuthMetaTypeMessage(Enum):
    UpdateError = "The AuthMetaType could not be updated."
    DeleteError = "The AuthMetaType could not be deleted."
    InsertError = "The AuthMetaType could not be inserted."
    MergeError = "The AuthMetaType could not be merged."
    AllowDeleteError = "Not allowed to delete this AuthMetaType."


class BudgetTypeMessage(Enum):
    UpdateError = "Some wrong when saving budget data, please try again!"


class CashflowTypeMessage(Enum):
    UpdateError = "Some wrong when saving cash flow data, please try again!"


class AuthMetaInfoMessage(Enum):
    UpdateError = "The AuthMetaInfo could not be updated."
    DeleteError = "The AuthMetaInfo could not be deleted."
    InsertError = "The AuthMetaInfo could not be inserted."


class FiscalTermMessage(Enum):
    UpdateError = "The FiscalTerm could not be updated."
    DeleteError = "The FiscalTerm could not be deleted."
    InsertError = "The FiscalTerm could not be inserted."
    AllowUpdateError = "Not allowed to update this FiscalTerm."
    AllowDeleteError = "Not allowed to delete this FiscalTerm."


class FiscalPeriodMessage(Enum):
    InsertError = "The FiscalPeriod could not be inserted."



