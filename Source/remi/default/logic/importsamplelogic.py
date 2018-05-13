# -*- coding: utf-8 -*-
from default.config.config import Config
from helper.excelreader import ExcelReader
from default.models.models2 import Account
from django.core.exceptions import ObjectDoesNotExist
from helper.util import DbAgent
from django.db.models import Q
import os
from django.conf import settings


class ImportSample:
    @staticmethod
    def load_data(adapter_name, import_file):
        ia = Config.get_data_import_adapter(adapter_name)
        er = ExcelReader()
        er.open(import_file)
        block = er.read_block(0, ia.start_col, ia.end_col, ia.start_row)
        data = ia.format_data(block, False)
        if not data:
            print(ia.error_message)
            return None
        return data

    @staticmethod
    def import_account(import_file=None):
        if import_file is None:
            import_file = os.path.join(settings.BASE_DIR, 'sampledata', 'account code.xlsx')

        data = ImportSample.load_data("account_import_adapter", import_file)
        if not data:
            return

        accounts = list()
        for rec in data:
            # Update table define to jis code

            DbAgent.execute_query("update account set id=%s, deleted_flag = true where id=%s", [rec['jis_id'],
                                                                                                rec['id']])
            DbAgent.execute_query("update table_definition set account_id=%s where account_id=%s", [rec['jis_id'],
                                                                                                    rec['id']])
            try:
                Account.objects.get(Q(pk=rec['id']) | Q(pk=rec['jis_id']))
            except ObjectDoesNotExist:
                o = Account()
                o.id = rec['jis_id']
                o.title = rec['title']
                if rec['tax_class'] is not None:
                    o.tax_class = rec['tax_class']
                else:
                    o.tax_class = 1
                o.settlement_date_type = rec['settlement_date_type']
                if rec['account_class'] is not None:
                    o.account_class = rec['account_class']
                else:
                    o.account_class = 3

                if rec['type'] is not None:
                    o.type = rec['type']

                o.is_cash = rec['is_cash']

                if rec['account_name']:
                    o.account_name = rec['account_name']
                else:
                    o.account_name = rec['title']
                if rec['account_code']:
                    o.account_code = rec['account_code']
                else:
                    o.account_code = rec['id']

                accounts.append(o)

        Account.objects.bulk_create(accounts)

    @staticmethod
    def import_scheduled(import_file=None):
        from default.logic.userlogic import LoginUser
        user = LoginUser.get_login_user()

        if import_file is None:
            import_file = os.path.join(settings.BASE_DIR, 'sampledata', 'scheduled.xlsx')

        data = ImportSample.load_data("scheduled_import_adapter", import_file)
        if not data:
            return

        from default.models.models2 import ScheduledJournal
        l = list()
        start_date = None
        end_date = None
        for rec in data:
            o = ScheduledJournal()
            o.owner_id = user.id
            o.type = rec['type']
            o.accrual_date = rec['accrual_date']
            o.settlement_date = rec['settlement_date']
            if end_date is None or end_date < o.settlement_date:
                end_date = o.settlement_date
            if start_date is None or start_date > o.settlement_date:
                start_date = o.settlement_date

            o.account_id = rec['account_id']
            o.opposite_account_id = rec['opposite_account_id']
            o.amount = rec['amount']
            o.tax = rec['tax']
            o.reference = rec['reference']
            o.definition_type = rec['definition_type']
            o.definition_id = rec['definition_id']
            o.tax_class = rec['tax_class']
            o.tax_rate_id = rec['tax_rate_id']
            l.append(o)

        # Delete old data first
        if start_date is not None and end_date is not None:
            DbAgent.execute_query("delete from scheduled_journal where "
                                  "owner_id=%s and settlement_date >= %s and settlement_date <=%s",
                                  [user.id, start_date, end_date])

        ScheduledJournal.objects.bulk_create(l)

    @staticmethod
    def import_budget(term_number, import_file=None):
        if import_file is None:
            import_file = os.path.join(settings.BASE_DIR, 'sampledata', 'budget.xlsx')

        data = ImportSample.load_data("budget_import_adapter", import_file)
        if not data:
            return

        from default.logic.fiscaltermlogic import FiscalTermLogic
        from default.models.models2 import Budget
        from default.logic.userlogic import LoginUser
        from helper.util import Util
        user = LoginUser.get_login_user()

        budgets = []
        periods = FiscalTermLogic.get_term_period_list(term_number)
        periods = list(periods)
        for rec in data:
            for i in range(12):
                if i < len(periods):
                    budget = Budget()
                    budget.owner_id = user.id
                    budget.plan_type = rec['plan_type']
                    budget.account_id = rec['account_id']
                    budget.fiscal_period_id = periods[i].id
                    budget.comment = rec['comment']
                    budget.amount = rec['amount{0}'.format(i+1)]
                    budgets.append(budget)

        DbAgent.execute_query("delete from budget where owner_id=%s and fiscal_period_id in ({0})".
                              format(", ".join(map(str, Util.model_list_to_list(periods, "id")))), [user.id])

        Budget.objects.bulk_create(budgets)

    @staticmethod
    def import_account_jis():
        from default.config.config import Config
        from helper.excelreader import ExcelReader
        from default.models.models2 import Account
        from django.core.exceptions import ObjectDoesNotExist

        ia = Config.get_data_import_adapter("account_jis_import_adapter")
        er = ExcelReader()
        er.open("C:\\Workspace\\Project\\2017\\201701 ASCADE\\delivery\\account code.xlsx")
        block = er.read_block(0, ia.start_col, ia.end_col, ia.start_row)
        data = ia.format_data(block, False)
        if not data:
            print(ia.error_message)
        else:
            accounts = list()
            for rec in data:
                try:
                    o = Account.objects.get(pk=rec['id'])
                    o.title = rec['title']
                    if rec['tax_class'] is not None:
                        o.tax_class = rec['tax_class']
                    else:
                        o.tax_class = 1

                    if rec['account_class'] is not None:
                        o.account_class = rec['account_class']
                    else:
                        o.account_class = 3

                    if rec['type'] is not None:
                        o.type = rec['type']
                    if rec['is_cash'] is not None and rec['is_cash']:
                        o.is_cash = True
                    else:
                        o.is_cash = False
                    if rec['account_name']:
                        o.account_name = rec['account_name']
                    else:
                        o.account_name = rec['title']
                    if rec['account_code']:
                        o.account_code = rec['account_code']
                    else:
                        o.account_code = rec['id']
                    o.save()
                except ObjectDoesNotExist:
                    o = Account()
                    o.id = rec['id']
                    o.title = rec['title']
                    if rec['tax_class'] is not None:
                        o.tax_class = rec['tax_class']
                    else:
                        o.tax_class = 1

                    if rec['account_class'] is not None:
                        o.account_class = rec['account_class']
                    else:
                        o.account_class = 3

                    if rec['type'] is not None:
                        o.type = rec['type']
                    if rec['is_cash'] is not None and rec['is_cash']:
                        o.is_cash = True
                    else:
                        o.is_cash = False
                    if rec['account_name']:
                        o.account_name = rec['account_name']
                    else:
                        o.account_name = rec['title']
                    if rec['account_code']:
                        o.account_code = rec['account_code']
                    else:
                        o.account_code = rec['id']

                    accounts.append(o)

            Account.objects.bulk_create(accounts)
