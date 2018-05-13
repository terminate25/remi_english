from .config import Config
from collections import OrderedDict


"""
Budget performance table's define.
If change database, must restart web server to take effect
"""
budget_performance_table = OrderedDict()
# Config.load_table_config(budget_performance_table, "budget_performance_table")
Config.load_database_table_config(budget_performance_table, "bp_table")

"""
Cashflow performance table's define
If change database, must restart web server to take effect
"""
cash_flow_table = OrderedDict()
# Config.load_table_config(cash_flow_table, "cash_flow_table")
Config.load_database_table_config(cash_flow_table, "cashflow_table")


