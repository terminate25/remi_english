import csv
from datetime import datetime

from django.db.models import TextField
from django.http import HttpResponse
from default.logic.reportdatalogic import *
from default.models.models2 import BizProspect, User, MetaType, BaseDataMetaRel, MetaInfo
from default.logic.userlogic import LoginUser
from default.config.config_role import *


class DownloadFileLogic:
    @staticmethod
    def create_workbook_csv(start_date, end_date, fields, target_data):
        """
        Create csv file  
        @type start_date: datetime
        @param start_date: 
        @type end_date:datetime
        @param end_date: 
        @type fields: dict
        @param fields: 
        @type target_data: list
        @param target_data: Targets data which want to download 
        @return: 
        """
        file_name = datetime.today().date().strftime('%Y-%m-%d')
        file_name = file_name + ".csv"
        response = HttpResponse(content_type='text/csv; charset=Shift_JIS')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(file_name)
        result = DownloadFileLogic.create_budget_performance_data(start_date, end_date, fields, target_data)
        # result[1] is title dict
        # result[0] list of data dict
        data = DownloadFileLogic.sort_list(result[0], "start_date")
        data.insert(0, result[1])
        # Result[2] is fields list, for arrange the csv columns
        fields = result[2]
        c = csv.writer(response)
        for i in range(0, len(data), 1):
            row_data = []
            for field in fields:
                row_data.append(data[i][field])
            c.writerow(row_data)
        return response

    @staticmethod
    def sort_list(sort_list, sort_field):
        """
        Sort list of dict by key
        @param sort_list: 
        @param sort_field: 
        @rtype: list of dict
        @return: 
        """
        sorted_list = sorted(sort_list, key=lambda k: k[sort_field])
        return sorted_list

    @staticmethod
    def create_budget_performance_data(start_date, end_date, fields_dict, target_data):
        """
        Create list of budget performance data dict base on arguments  
        @type start_date: datetime
        @param start_date: 
        @type end_date: datetime
        @param end_date: 
        @type fields_dict: dict 
        @param fields_dict: 
        @type target_data: lists
        @param target_data: 
        @return: 
        """
        data_list = []
        field_keys = []
        # user field keys
        for key, value in fields_dict.items():
            field_keys.append(key)

        meta_types = MetaType.objects.values('id', 'meta_type', 'disp')
        meta_types_key = []
        for meta_type in meta_types:
            meta_dict = {meta_type['meta_type']: meta_type['disp']}
            field_keys.append(meta_type['meta_type'])
            meta_types_key.append(meta_type['meta_type'])
            fields_dict.update(meta_dict)

        # Filter data
        user = LoginUser.get_login_user()
        filters = user.get_filters(ModuleName.BudgetPerformance)
        # Biz Budget
        base_id_biz_budget = user.get_filtered_base_data_ids(filters, AuthBaseDataName.BizBudget.value)
        if BPDownloadTarget.BizBudget.code in target_data:
            biz_budget = DownloadFileLogic.create_biz_budget_data(start_date, end_date,
                                                                  field_keys, meta_types_key,
                                                                  base_id_biz_budget, user.id)
            data_list.extend(biz_budget)

        # Budget
        if BPDownloadTarget.Budget.code in target_data:
            budget = DownloadFileLogic.create_budget_data(start_date, end_date, field_keys,
                                                          meta_types_key)
            data_list.extend(budget)

        # Prospect
        past = False
        if BPDownloadTarget.PastProspect.code in target_data:
            past = True

        # Result
        if BPDownloadTarget.ResultAndProspect.code in target_data:
            base_id_prospect = user.get_filtered_base_data_ids(filters, AuthBaseDataName.BizProspect.value)

            # Get prospect data
            prospect = DownloadFileLogic.create_prospect_data(start_date, end_date, field_keys,
                                                              meta_types_key, base_id_prospect, user.id, past)
            data_list.extend(prospect)

            # Get schedule data
            schedule = DownloadFileLogic.create_schedule_data(start_date, end_date, field_keys, meta_types_key, past)
            data_list.extend(schedule)

            # Get result data (journal voucher )
            result = DownloadFileLogic.create_result_data(start_date, end_date, field_keys,
                                                          meta_types_key)
            data_list.extend(result)

        return data_list, fields_dict, field_keys

    @staticmethod
    def create_default_dict(fields):
        """
        Create default dict with all fields 
        @type fields: list
        @param fields: 
        @return: 
        """
        __default_dict = {}
        for field in fields:
            field_dict = {field: ""}
            __default_dict.update(field_dict)
        return __default_dict

    @staticmethod
    def create_biz_budget_data(start_date, end_date, fields, meta_types, base_id_filtered, logging_user_id):
        """
        @type start_date: datetime
        @param start_date: 
        @type end_date: datetime
        @param end_date: 
        @type fields: list
        @param fields: 
        @type: meta_types: Queryset
        @param meta_types
        @type base_id_filtered: list of int
        @param base_id_filtered 
        @type logging_user_id: int
        @param logging_user_id: 
        @return: 
        """
        data = []
        user_condition = DownloadFileLogic.create_user_condition('owner_id')
        results = BizBudget.objects.values('id', 'plan_type', 'account__account_code', 'owner_id',
                                           'account__account_name', 'amount', 'fiscal_period',
                                           'fiscal_period__term_number', 'fiscal_period__name',
                                           'fiscal_period__start_date',
                                           'fiscal_period__end_date').annotate(user_name=user_condition)

        if base_id_filtered is not None:
            results = results.filter(Q(id__in=base_id_filtered) | Q(owner_id=logging_user_id))
        ids = results.values_list('id', flat=True)
        base_data = DownloadFileLogic.create_meta_map(ids, TableName.BizBudget.value, meta_types)
        for r in results:
            if r['fiscal_period__start_date'] > end_date or r['fiscal_period__end_date'] < start_date:
                continue
            data_dict = DownloadFileLogic.create_default_dict(fields)
            if r['fiscal_period__start_date'] is None:
                data_dict['start_date'] = datetime(1900, 1, 1).date()
            else:
                data_dict["start_date"] = r['fiscal_period__start_date']
            data_dict["end_date"] = r['fiscal_period__end_date']
            data_dict["id"] = r['id']
            if BaseOptionDefine.Base.code == r['plan_type']:
                data_dict["plan_type"] = DataTypeBP.PlanBase.title
            else:
                data_dict["plan_type"] = DataTypeBP.PlanOption.title
            data_dict["data_type"] = DataTypeBP.BizBudget.title
            data_dict["account_id"] = r['account__account_code']
            data_dict["account_name"] = r['account__account_name']
            data_dict["term"] = r['fiscal_period__term_number']
            data_dict["amount"] = r['amount']
            data_dict["owner"] = r['user_name']
            data_dict["year"] = r['fiscal_period__start_date'].year
            data_dict["month"] = r['fiscal_period__name']
            # Disable
            for meta_type in meta_types:
                data_dict[meta_type] = base_data[r['id']][meta_type]
            data.append(data_dict)
        return data

    @staticmethod
    def create_budget_data(start_date, end_date, fields, meta_types):
        """
        @type start_date: datetime
        @param start_date: 
        @type end_date: datetime
        @param end_date: 
        @type fields: list
        @param fields: 
        @param meta_types
        @return: 
        """
        data = []
        user_condition = DownloadFileLogic.create_user_condition('owner_id')
        results = Budget.objects.values('id', 'plan_type', 'account__account_code', 'account__account_name',
                                        'amount', 'fiscal_period', 'fiscal_period__term_number',
                                        'fiscal_period__name', 'fiscal_period__start_date',
                                        'fiscal_period__end_date').annotate(user_name=user_condition)
        # if base_id_filtered is not None:
        #     results = results.filter(Q(id__in=base_id_filtered) | Q(owner_id=logging_user_id))
        ids = results.values_list('id', flat=True)
        base_data = DownloadFileLogic.create_meta_map(ids, TableName.Budget.value, meta_types)
        for r in results:
            if r['fiscal_period__start_date'] > end_date or r['fiscal_period__end_date'] < start_date:
                continue
            data_dict = DownloadFileLogic.create_default_dict(fields)
            if r['fiscal_period__start_date'] is None:
                data_dict['start_date'] = datetime(1900, 1, 1).date()
            else:
                data_dict['start_date'] = r['fiscal_period__start_date']

            data_dict['end_date'] = r['fiscal_period__end_date']
            data_dict["id"] = r['id']

            if BaseOptionDefine.Base.code == r['plan_type']:
                data_dict['plan_type'] = DataTypeBP.PlanBase.title
            else:
                data_dict['plan_type'] = DataTypeBP.PlanOption.title
            data_dict['data_type'] = DataTypeBP.Budget.title
            data_dict['account_id'] = r['account__account_code']
            data_dict['account_name'] = r['account__account_name']
            data_dict['term'] = r['fiscal_period__term_number']
            data_dict['amount'] = r['amount']
            data_dict['owner'] = r['user_name']
            data_dict['year'] = r['fiscal_period__start_date'].year
            data_dict['month'] = r['fiscal_period__name']

            for meta_type in meta_types:
                data_dict[meta_type] = base_data[r['id']][meta_type]
            data.append(data_dict)

        return data

    @staticmethod
    def create_prospect_data(start_date, end_date, fields, meta_types,
                             base_id_filtered, logging_user_id, past_prospect=False):
        """
        @type start_date: date
        @param start_date: 
        @type end_date: date
        @param end_date: 
        @type fields: list
        @param fields: 
        @type past_prospect: bool
        @param past_prospect:
        @type base_id_filtered: list of int
        @param base_id_filtered 
        @param meta_types
        @type logging_user_id: int
        @param logging_user_id
        @return: 
        """
        data = []
        last_import_date = ImportHistory.get_last_import_date()
        last_import_date = last_import_date.date()

        if not past_prospect:
            if (start_date < last_import_date) and (last_import_date < end_date):
                start_date = last_import_date
            elif end_date < last_import_date:
                return []
        user_condition = DownloadFileLogic.create_user_condition('owner_id')
        fiscal_periods = FiscalTermLogic.get_period_list_start_end_date(start_date, end_date)
        period_map = DownloadFileLogic.create_period_map(fiscal_periods)
        account_map = DownloadFileLogic.create_account_map()

        period_condition = DownloadFileLogic.create_period_condition('accrual_date', fiscal_periods)
        results = BizProspect.objects.values('id', 'type', 'amount', 'opportunity_stage',
                                             'owner_id', 'accrual_date') \
            .annotate(period=period_condition).annotate(user_name=user_condition) \
            .filter(Q(accrual_date__gte=start_date) & Q(accrual_date__lte=end_date))

        if base_id_filtered is not None:
            results = results.filter(Q(id__in=base_id_filtered) | Q(owner_id=logging_user_id))
        ids = results.values_list('id', flat=True)
        base_data = DownloadFileLogic.create_meta_map(ids, TableName.BizProspect.value, meta_types)
        for r in results:
            data_dict = DownloadFileLogic.create_default_dict(fields)
            data_dict['data_type'] = DataTypeBP.BizProspect.title
            type_result = r['type']
            account_id = Util.convert_prospect_type_to_account(type_result)
            data_dict['account_name'] = account_map[account_id]['name']
            data_dict['account_id'] = account_map[account_id]['code']
            data_dict['id'] = r['id']
            data_dict['amount'] = r['amount']
            data_dict['accuracy'] = OpportunityStage.get_title(r['opportunity_stage'])
            data_dict['owner'] = r['user_name']
            period_id = r['period']
            if period_id is not None:
                data_dict['term'] = period_map[period_id]['term']
                data_dict['month'] = period_map[period_id]['month']
                data_dict['start_date'] = period_map[period_id]['start_date']
                data_dict['end_date'] = period_map[period_id]['end_date']
                data_dict['year'] = period_map[period_id]['year']
            else:
                data_dict['term'] = 0
                data_dict['month'] = '01'
                data_dict['start_date'] = datetime(1900, 1, 1).date()
                data_dict['end_date'] = datetime(1900, 1, 1).date()
                data_dict['year'] = '1900'

            for meta_type in meta_types:
                data_dict[meta_type] = base_data[r['id']][meta_type]
            data.append(data_dict)
        return data

    @staticmethod
    def create_schedule_data(start_date, end_date, fields, meta_types, past_prospect=False):
        """
        @type start_date: date
        @param start_date: 
        @type end_date: date
        @param end_date: 
        @type fields: list
        @param fields: 
        @type past_prospect: bool
        @param past_prospect:
        @param meta_types
        @return: 
        """
        data = []
        last_import_date = ImportHistory.get_last_import_date()
        last_import_date = last_import_date.date()
        if not past_prospect:
            if (start_date < last_import_date) and (last_import_date < end_date):
                start_date = last_import_date
            elif end_date < last_import_date:
                return []
        user_condition = DownloadFileLogic.create_user_condition('owner_id')
        fiscal_periods = FiscalTermLogic.get_period_list_start_end_date(start_date, end_date)
        period_map = DownloadFileLogic.create_period_map(fiscal_periods)
        period_condition = DownloadFileLogic.create_period_condition('accrual_date', fiscal_periods)
        results = ScheduledJournal.objects.values('id', 'account__account_code', 'account__account_name',
                                                  'amount', 'owner_id',
                                                  'accrual_date') \
            .annotate(period=period_condition).annotate(user_name=user_condition) \
            .filter(Q(accrual_date__gte=start_date) & Q(accrual_date__lte=end_date))

        # if base_id_filtered is not None:
        #     results = results.filter(Q(id__in=base_id_filtered) | Q(owner_id=logging_user_id))
        ids = results.values_list('id', flat=True)
        base_data = DownloadFileLogic.create_meta_map(ids, TableName.BizProspect.value, meta_types)
        for r in results:
            data_dict = DownloadFileLogic.create_default_dict(fields)
            data_dict['data_type'] = DataTypeBP.Scheduled.title
            data_dict['account_name'] = r['account__account_name']
            data_dict['account_id'] = r['account__account_code']
            data_dict['id'] = r['id']
            data_dict['amount'] = r['amount']
            data_dict['owner'] = r['user_name']
            period_id = r['period']

            if period_id is not None:
                data_dict['term'] = period_map[period_id]['term']
                data_dict['month'] = period_map[period_id]['month']
                data_dict['start_date'] = period_map[period_id]['start_date']
                data_dict['end_date'] = period_map[period_id]['end_date']
                data_dict['year'] = period_map[period_id]['year']
            else:
                data_dict['term'] = 0
                data_dict['month'] = '01'
                data_dict['start_date'] = datetime(1900, 1, 1).date()
                data_dict['end_date'] = datetime(1900, 1, 1).date()
                data_dict['year'] = '1900'

            for meta_type in meta_types:
                data_dict[meta_type] = base_data[r['id']][meta_type]
            data.append(data_dict)
        return data

    @staticmethod
    def create_result_data(start_date, end_date, fields, meta_types):
        """
        @type start_date: date
        @param start_date: 
        @type end_date: date
        @param end_date: 
        @type fields: list
        @param fields: 
        @param meta_types
        @return: 
        """
        data = []
        last_import_date = ImportHistory.get_last_import_date()
        last_import_date = last_import_date.date()

        if (start_date < last_import_date) and (last_import_date < end_date):
            end_date = last_import_date
        fiscal_periods = FiscalTermLogic.get_period_list_start_end_date(start_date, end_date)
        period_map = DownloadFileLogic.create_period_map(fiscal_periods)
        period_condition = DownloadFileLogic.create_period_condition('date', fiscal_periods)
        owner_condition = DownloadFileLogic.create_user_condition('owner_id')
        results = JournalVoucher.objects.values('id', 'data_type', 'account__account_name', 'account__account_code',
                                                'amount', 'owner_id', 'opportunity_stage',
                                                'date').annotate(user_name=owner_condition) \
            .annotate(period=period_condition) \
            .filter(Q(date__gt=start_date) & Q(date__lt=end_date))
        # if base_id_filtered is not None:
        #     results = results.filter(Q(id__in=base_id_filtered) | Q(owner_id=logging_user_id))
        ids = results.values_list('id', flat=True)
        base_data = DownloadFileLogic.create_meta_map(ids, TableName.JournalVoucher.value, meta_types)

        for r in results:
            data_dict = DownloadFileLogic.create_default_dict(fields)
            data_dict['data_type'] = DataTypeBP.Result.title
            data_dict['account_name'] = r['account__account_name']
            data_dict['account_id'] = r['account__account_code']
            data_dict['owner'] = r['user_name']
            data_dict['amount'] = r['amount']
            data_dict['accuracy'] = OpportunityStage.get_title(r['opportunity_stage'])
            period_id = r['period']
            data_dict["id"] = r['id']

            if period_id is not None:
                data_dict['term'] = period_map[period_id]['term']
                data_dict['month'] = period_map[period_id]['month']
                data_dict['start_date'] = period_map[period_id]['start_date']
                data_dict['end_date'] = period_map[period_id]['end_date']
                data_dict['year'] = period_map[period_id]['year']
            else:
                data_dict['term'] = 0
                data_dict['month'] = '01'
                data_dict['start_date'] = datetime(1900, 1, 1).date()
                data_dict['end_date'] = datetime(1900, 1, 1).date()
                data_dict['year'] = '1900'

            for meta_type in meta_types:
                data_dict[meta_type] = base_data[r['id']][meta_type]
            data.append(data_dict)
        return data

    @staticmethod
    def create_meta_map(base_data_ids, table_name, meta_types):
        """
        
        @type base_data_ids: list
        @param base_data_ids: 
        @type table_name: basestring
        @param table_name: 
        @param meta_types: 
        @return: 
        """
        base_info_list = BaseDataMetaRel.objects.values('base_data_id', 'meta_id',
                                                        'meta_type__meta_type', 'meta_type__disp'). \
            filter(Q(base_data_id__in=base_data_ids) & Q(base_data_name=table_name))
        base_data = {}
        for base_id in base_data_ids:
            base_dict = DownloadFileLogic.create_default_dict(meta_types)
            base_data[base_id] = base_dict
        meta_info_map = DownloadFileLogic.create_meta_info_map()
        for base_info in base_info_list:
            try:
                base_data[base_info['base_data_id']][base_info['meta_type__meta_type']] = meta_info_map[
                    base_info['meta_id']]
            except KeyError as e:
                print("{0}: Meta info id {1} is not exist".format(e, base_info['meta_id']))
        return base_data

    @staticmethod
    def create_meta_info_map():
        """
        Create meta info dict {meta_info_id: meta_info_value}
        @rtype :dict
        @return:
        """
        meta_info_list = MetaInfo.objects.all()
        meta_info_map = {}
        for meta_info in meta_info_list:
            meta_map = dict()
            meta_map[meta_info.id] = meta_info.value
            meta_info_map.update(meta_map)
        return meta_info_map

    @staticmethod
    def create_period_condition(column_name, period_list):
        """
        @param column_name: 
        @param period_list: 
        @return: 
        """
        cases = []
        column_name_gte = column_name + '__gte'
        column_name_lte = column_name + '__lte'
        for i in range(0, period_list.count(), 1):
            period = period_list[i]
            start_date = period.start_date
            end_date = period.end_date
            cases.append(
                When((Q(**{column_name_gte: start_date}) & Q(**{column_name_lte: end_date})), then=period_list[i].id)
            )
        period_cases = Case(*cases, default=Value(None), output_field=IntegerField())
        return period_cases

    @staticmethod
    def create_period_map(period_list):
        """
        Dict of {period_id: {'term': term, 'month': month, 'start_date': start_date,...}}
        @param period_list: 
        @return: 
        """
        period_map = {}
        for period in period_list:
            period_map[period.id] = {}
            period_map[period.id]['term'] = period.term_number.term_number
            period_map[period.id]['month'] = period.name
            period_map[period.id]['start_date'] = period.start_date
            period_map[period.id]['end_date'] = period.end_date
            period_map[period.id]['year'] = period.start_date.year

        return period_map

    @staticmethod
    def create_user_condition(column):
        """
        Get owner name 
        @type column: str
        @param column: 
        @return: 
        """
        cases = []
        users = User.objects.values('id', 'user_name')
        for user in users:
            cases.append(
                When(Q(**{column: user['id']}), then=Value(user['user_name']))
            )
        user_case = Case(*cases, default=Value(''), output_field=TextField())
        return user_case

    @staticmethod
    def create_account_map():
        """
        Dict of  {account_id: {'name': account_name, 'code': account_code}}
        @rtype:dict
        @return: 
        """
        account_dict = {}
        accounts = Account.objects.all()
        for account in accounts:
            account_map = dict()
            account_map['name'] = account.account_name
            account_map['code'] = account.account_code
            account_dict[account.id] = account_map
        return account_dict
