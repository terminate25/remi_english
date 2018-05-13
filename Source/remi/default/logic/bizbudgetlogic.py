from datetime import datetime, timedelta

from django.db.models import F, Sum, Q
from default.config.config_role import *
from default.config.config_common import *
from default.logic.fiscaltermlogic import *
from default.logic.loglogic import *
from default.models.models2 import ImportHistory, FiscalPeriod, JournalVoucher, \
    BizProspect, BizBudget, BaseDataMetaRel, MetaInfo
from default.response.responses import *
from helper.util import DbAgent
from middleware.router import DatabaseRouter
from default.config.config_common import AuthMetaTypeDefine, ImportDataType, AuthBaseDataName, BaseDataName
from default.models.models2 import BizBudget, BaseDataAuthMetaRel, BaseDataMetaRel, ImportHistory
from django.db import transaction
from helper.util import Util


class BizBudgetLogic:

    @staticmethod
    def get_biz_budgets(account_id, start_date, end_date):
        """
        @type account_id : int
        @param account_id: Account id
        @type start_date: datetime
        @param start_date: 
        @type end_date: datetime
        @param end_date: 
        @return:  
        """

        # 対象の月度を取得。
        # XXXX endDate は使われていない。 startDate を含む月度の情報だけを返している。これでいいのか？
        # 詳細画面で使うので、取得は月度単位が前提、。
        # クライアントからは startDate に表示対象月度の初日が指定されるはずなのでこれで今のところの用途は足りてる模様だが。
        periods = FiscalTermLogic.get_period_list(start_date, 1)
        period = periods[0]
        total_map = {}
        # 指定月度の明細をターゲットID単位で束ねて取得
        biz_journal_dict = BizJournalLogic.get_biz_journal_map(period, account_id, total_map)
        # 指定月度の総額をターゲットID単位で集計した情報を取得
        target_total_dict = BizJournalLogic.get_total_map_by_target_id(period, account_id)
        # List BizTotal
        targets = []

        for target_id, biz_total in target_total_dict.items():
            targets.append(biz_total)
            if target_id in biz_journal_dict:
                biz_total.biz_journal_list = biz_journal_dict[target_id]
            if target_id in total_map:
                total = total_map[target_id]
            else:
                total = None
            if total is not None:
                biz_total.result = total.result
                biz_total.each_stage = total.each_stage
            else:
                empty_stage = []
                for stage in OpportunityStage:
                    empty_stage.append(0)
                biz_total.result = 0
                biz_total.each_stage = empty_stage

        return targets

    @staticmethod
    def get_import_history_list(owner_id):
        """
        Retrieve import history of user
        @param owner_id: account login
        @type owner_id: int
        @return: 
        """
        query = "select ih.*, dp.meta_id as department_id, lt.meta_id as latest from import_history ih " \
                "left join (select import_history_id, meta_id from biz_budget bp " \
                "inner join base_data_auth_meta_rel bd on bd.meta_type_id=%s " \
                "and bd.base_data_name=%s and bp.id=bd.base_data_id " \
                "group by import_history_id, meta_id) lt " \
                "on ih.id = lt.import_history_id " \
                "left join (select base_data_id, meta_id from base_data_auth_meta_rel " \
                "where meta_type_id=%s and base_data_name=%s) dp " \
                "on dp.base_data_id=ih.id " \
                "where ih.user_id=%s and ih.data_type=%s " \
                "order by imported_datetime desc"

        rs = DbAgent.get_record_set(query, [AuthMetaTypeDefine.Department.code,
                                            AuthBaseDataName.BizBudget.value, AuthMetaTypeDefine.Department.code,
                                            AuthBaseDataName.ImportHistory.value, owner_id,
                                            ImportDataType.BizBudget.value])
        rs = rs[:5]
        return rs

    @staticmethod
    def get_term_import_history_list(target_term):
        """
        Retrieve data from table by target term and filter by user
        @param target_term: fiscal term
        @type target_term: int
        @return: 
        """
        # Filter
        user = LoginUser.get_login_user()
        in_query = user.get_filtered_query_string(ModuleName.BizBudget, AuthMetaTypeDefine.Department.code,
                                                  none_if_no_filter=False)

        if in_query is not None and len(in_query) > 0:
            query = "select ih.*, lt.meta_id as department_id from import_history ih " \
                    "inner join (select import_history_id, meta_id from biz_budget bp " \
                    "inner join base_data_auth_meta_rel bd on bd.meta_type_id=%s " \
                    "and bd.base_data_name=%s and bp.id=bd.base_data_id and bd.meta_id in ({0})" \
                    "group by import_history_id, meta_id) lt " \
                    "on ih.id = lt.import_history_id " \
                    "where ih.target_term=%s and ih.data_type=%s " \
                    "order by lt.meta_id,imported_datetime desc".format(in_query)
        elif in_query is None:
            query = "select ih.*, lt.meta_id as department_id from import_history ih " \
                    "inner join (select import_history_id, meta_id from biz_budget bp " \
                    "inner join base_data_auth_meta_rel bd on bd.meta_type_id=%s " \
                    "and bd.base_data_name=%s and bp.id=bd.base_data_id " \
                    "group by import_history_id, meta_id) lt " \
                    "on ih.id = lt.import_history_id " \
                    "where ih.target_term=%s and ih.data_type=%s " \
                    "order by lt.meta_id,imported_datetime desc"
        else:
            return []

        rs = DbAgent.get_record_set(query, [AuthMetaTypeDefine.Department.code,
                                            AuthBaseDataName.BizBudget.value, target_term,
                                            ImportDataType.BizBudget.value])
        # rs = rs[:5]
        return rs

    @staticmethod
    @transaction.atomic(using=DatabaseRouter.data_database)
    def import_biz_budget(target_term, department_id, owner_id, imported_filename, memo, adapter):
        """
        Process data from file excel
        @param target_term: Term id
        @param department_id: Department id
        @param owner_id: Owner id
        @param memo: Memo
        @param adapter: Import adapter
        @param imported_filename: Imported file name
        @type target_term: int
        @type department_id: int
        @type owner_id: int
        @type imported_filename: str
        @type memo: str
        @type adapter: ImportAdapter
        @return:
        """
        target_term = int(target_term)
        department_id = int(department_id)

        # Get all of id which will be delete: the same term, department and owner_id
        query = "select id from biz_budget where " \
                "import_history_id in (select id from import_history where data_type=%s " \
                "and target_term=%s and user_id=%s) and " \
                "id in (select base_data_id from base_data_auth_meta_rel " \
                "where base_data_name=%s and meta_type_id=%s and meta_id=%s)"
        biz_budget_ids = DbAgent.get_data_list(query, [ImportDataType.BizBudget.value,
                                                       target_term, owner_id, AuthBaseDataName.BizBudget.value,
                                                       AuthMetaTypeDefine.Department.code, department_id])

        # Delete history data
        BizBudget.objects.filter(id__in=biz_budget_ids).delete()

        # Delete auth base meta relation
        BaseDataAuthMetaRel.objects.filter(base_data_id__in=biz_budget_ids,
                                           base_data_name=AuthBaseDataName.BizBudget.value).delete()
        # Delete base meta data relation
        BaseDataMetaRel.objects.filter(base_data_id__in=biz_budget_ids,
                                       base_data_name=BaseDataName.BizBudget.value).delete()

        # New import history
        ih = ImportHistory()
        ih.target_term_id = target_term
        ih.data_type = ImportDataType.BizBudget.value
        ih.user_id = owner_id
        if memo and memo != "":
            ih.memo = memo
        ih.imported_filename = imported_filename
        ih.save()

        # Auth base meta relation for import history
        auth_meta = BaseDataAuthMetaRel()
        auth_meta.base_data_name = AuthBaseDataName.ImportHistory.value
        auth_meta.base_data_id = ih.id
        auth_meta.meta_type_id = AuthMetaTypeDefine.Department.code
        auth_meta.meta_id = department_id
        auth_meta.save()

        # Import data
        data = adapter.get_data()
        biz_budgets = []
        periods = FiscalTermLogic.get_term_period_list(target_term)
        periods = list(periods)
        for rec in data:
            for i in range(12):
                if i < len(periods):
                    biz_budget = BizBudget()
                    biz_budget.owner_id = owner_id
                    biz_budget.import_history_id = ih.id
                    biz_budget.target_id = rec['target_id']
                    biz_budget.plan_type = rec['plan_type']
                    biz_budget.account_id = rec['account']
                    biz_budget.fiscal_period_id = periods[i].id
                    biz_budget.amount = rec['amount{0}'.format(i+1)]
                    biz_budgets.append(biz_budget)

        BizBudget.objects.bulk_create(biz_budgets)

        # Get list id of imported data
        query = "select id from biz_budget where " \
                "import_history_id = %s order by id"
        biz_budget_ids = DbAgent.get_data_list(query, [ih.id])

        # Auth base meta relation for prospect data
        auth_metas = []
        for base_data_id in biz_budget_ids:

            # Update auth meta data
            auth_meta = BaseDataAuthMetaRel()
            auth_meta.base_data_name = AuthBaseDataName.BizBudget.value
            auth_meta.base_data_id = base_data_id
            auth_meta.meta_type_id = AuthMetaTypeDefine.Department.code
            auth_meta.meta_id = department_id
            auth_metas.append(auth_meta)

        BaseDataAuthMetaRel.objects.bulk_create(auth_metas)

        # Update meta data
        adapter.insert_meta_data_relation(biz_budget_ids, 12)

        # Write log
        LogOperation.log(LogModule.BizBudget, LogType.Insert, LogResult.Success, ih.id)

        return ih.id

    @staticmethod
    def get_term_data(term_number, import_history_id=None):
        """
        Retrieve data of current fiscal and filter by user
        @param term_number: fiscal term
        @param import_history_id: import history of user
        @type term_number: int
        @type import_history_id: int
        @return: 
        """
        user = LoginUser.get_login_user()

        periods = FiscalTermLogic.get_term_period_list(int(term_number))
        fiscal_period_ids = FiscalTermLogic.create_period_id_in_cond(periods)
        auth_meta_types = AuthMetaType.objects.all().order_by("meta_type")
        # meta_types = MetaType.objects.all().order_by("meta_type")

        from helper.util import StringBuilder
        query = StringBuilder()
        query_from = StringBuilder()
        query_group_by = StringBuilder()
        query_order_by = StringBuilder()

        main_fields = "account_id, plan_type"  # target_id

        query_from.append("\nfrom biz_budget bz")
        query_group_by.append("\ngroup by {0}".format(main_fields))
        query.append("select {0}".format(main_fields))

        # Auth meta
        for meta_type in auth_meta_types:
            # Only department
            if meta_type.meta_type == AuthMetaTypeDefine.Department.title:
                in_query = user.get_filtered_query_string(ModuleName.BizBudget, AuthMetaTypeDefine.Department.code,
                                                          none_if_no_filter=False)
                if in_query is not None and len(in_query) > 0:
                    query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
                    query_from.append(" left join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                                      "and bz.id={0}.base_data_id and {0}.meta_type_id={2} and {0}.meta_id in ({3})".
                                      format(meta_type.meta_type, AuthBaseDataName.BizBudget.value, meta_type.id, in_query))
                    query_group_by.append(", {0}.meta_id".format(meta_type.meta_type))
                    query_order_by.append(", {0}.meta_id".format(meta_type.meta_type))
                elif in_query is None:
                    query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
                    query_from.append(" left join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                                      "and bz.id={0}.base_data_id and {0}.meta_type_id={2} ".
                                      format(meta_type.meta_type, AuthBaseDataName.BizBudget.value, meta_type.id))
                    query_group_by.append(", {0}.meta_id".format(meta_type.meta_type))
                    query_order_by.append(", {0}.meta_id".format(meta_type.meta_type))
                else:
                    return []

        # # Meta
        # for meta_type in meta_types:
        #     # Only staff
        #     if meta_type.id == MetaTypeDefine.Staff.code:
        #         query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
        #         query_from.append(" left join base_data_meta_rel {0} on {0}.base_data_name='{1}' "
        #                           "and bz.id={0}.base_data_id and {0}.meta_type_id={2}".
        #                           format(meta_type.meta_type, AuthBaseDataName.BizBudget.value, meta_type.id))
        #         query_group_by.append(", {0}.meta_id".format(meta_type.meta_type))

        # Sum by 12 month
        for i in range(periods.count()):
            query.append(", sum(case when fiscal_period_id = {0} then amount else 0 end) as amount{1}".
                         format(periods[i].id, i+1))

        # summary
        query.append(", sum(amount) as summary")

        query_order_by.append(", {0}".format(main_fields))
        query.append(query_from)
        query.append(" \nwhere fiscal_period_id in ({0})".format(", ".join(map(str, fiscal_period_ids))))

        if import_history_id is not None:
            query.append(" and import_history_id={0} ".format(import_history_id))

        query.append(query_group_by)
        query.append(" \norder by {0}".format(str(query_order_by)[1:]))

        results = DbAgent.get_record_set(str(query))

        return results


class BizJournalLogic:
    class Total:
        result = 0
        each_stage = []

        def __init__(self):
            self.result = 0
            self.each_stage = []

    @staticmethod
    def get_biz_journal_map(period, account_id, total_dict):
        """
        @type period: FiscalPeriod
        @param period: 
        @type account_id: int
        @param account_id: 
        @type total_dict: dict
        @param total_dict: 
        @return: 
        """
        last_import_date = ImportHistory.get_last_import_date()

        journal_query_date = period.end_date
        prospect_query_date = period.start_date
        last_imported_next_date = last_import_date + timedelta(1)

        if (period.start_date <= last_import_date.date()) and (period.end_date >= last_import_date.date()):
            journal_query_date = last_import_date
            prospect_query_date = last_imported_next_date

        # case 1: 実績取得（過去～最終取込日まで）
        results = JournalVoucher.objects.filter(Q(date__gte=period.start_date) & Q(date__lte=journal_query_date) &
                                                Q(account=account_id)).values('id', 'amount', 'reference',
                                                                              'date', 'target_id')
        target_ids = []
        for r in results:
            target_ids.append(r['id'])
        meta_dict = BaseDataMetaRelLogic.get_meta_map(TableName.JournalVoucher.value, target_ids)

        # BizBudgetJournal
        biz_journal_dict = {}
        for r in results:
            target_id = r['target_id']
            biz_journal_list = []
            if target_id in biz_journal_dict:
                biz_journal_list = biz_journal_dict[target_id]
            else:
                biz_journal_dict[target_id] = biz_journal_list

            journal = BizBudgetJournalResponse()
            journal.data_type = AccountDataType.Result.code
            journal.amount = r['amount']
            journal.reference = r['reference']
            journal.accrual_date = r['date']

            if r['id'] in meta_dict:
                journal.meta_list = MetaDataResponse.create_meta_data_list(meta_dict[r['id']])
            biz_journal_list.append(journal)
            if target_id in total_dict:
                total = total_dict[target_id]
            else:
                total = BizJournalLogic.Total()
                for stage in OpportunityStage:
                    total.each_stage.append(0)
                total_dict[target_id] = total
            total.result += journal.amount

        # Case 2: 見込み取得（最終取込日～未来） : 対象とする期間の末尾が最終取込み日の後なら取得。そうでなければ空
        if period.end_date > last_import_date.date():
            prospects = BizProspect.objects.annotate(account_id=Case(
                    When(type=0, then=1),
                    When(type=1, then=2),
                    default=F('type'),
                    output_field=IntegerField(),)).filter(Q(accrual_date__gte=prospect_query_date) &
                                                          Q(accrual_date__lte=period.end_date)).\
                values('id', 'amount', 'title', 'accuracy', 'opportunity_stage', 'accrual_date',
                       'settlement_date', 'target_id', 'account_id')
        else:
            prospects = []

        # BIZ_PROSPECT のメタ情報を取得する
        target_ids = []
        for prospect in prospects:
            target_ids.append(prospect['id'])

        meta_dict = BaseDataMetaRelLogic.get_meta_map(TableName.BizProspect.value, target_ids)

        for prospect in prospects:
            target_id = prospect['target_id']
            biz_journal_list = []

            if target_id in biz_journal_dict:
                biz_journal_list = biz_journal_dict[target_id]
            else:
                biz_journal_dict[target_id] = biz_journal_list
            journal = BizBudgetJournalResponse()
            journal.data_type = AccountDataType.BizProspect.code
            journal.amount = prospect['amount']
            journal.accuracy = prospect['accuracy']
            journal.opportunity_stage = prospect['opportunity_stage']
            journal.reference = prospect['title']
            journal.accrual_date = prospect['accrual_date']
            journal.settlement_date = prospect.get("settlement_date")
            # メタデータの格納
            if prospect['id'] in meta_dict:
                meta_list = MetaDataResponse.create_meta_data_list(meta_dict[prospect['id']])
                journal.meta_list = meta_list
            biz_journal_list.append(journal)

            if target_id in total_dict:
                total = total_dict[target_id]
            else:
                total = BizJournalLogic.Total()
                for stage in OpportunityStage:
                    total.each_stage.append(0)
                total_dict[target_id] = total

            each_stage_amount = total.each_stage[journal.opportunity_stage]
            total.each_stage[journal.opportunity_stage] = each_stage_amount + journal.amount
        return biz_journal_dict

    @staticmethod
    def get_total_map_by_target_id(period, account_id):
        """
        @type period : FiscalPeriod
        @param period: 
        @type account_id: int
        @param account_id: 
        @rtype: dict
        @return: 
        """
        target_period_name = period.term_number.name + period.name
        #  XXX: 暫定仕様
        #  補助科目に相当する科目が指定された場合、予算は親科目の方を参照するが、実際の明細は子科目を参照する。
        # （本来なら仕入目標が存在する？）
        #  例）
        #  売上(海外仕入) ⇒ 1002
        #  売上(国内仕入) ⇒ 1003
        #  売上(国内仕入(特殊)) ⇒ 1004
        #  となっていた場合、予算は売上を参照し、各明細はそれぞれ海外仕入、国内仕入、国内仕入（特殊）を参照する

        account_id = Util.get_parent_account_id(account_id)
        biz_budgets = BizBudget.objects.filter(Q(fiscal_period=period.id) & Q(account=account_id)).\
            values('target', 'plan_type').annotate(amount=Sum('amount')).\
            values('target__name', 'target', 'plan_type', 'amount')

        biz_total_dict = {}
        for biz_budget in biz_budgets:
            target_id = biz_budget['target']
            biz_total = BizBudgetTotalResponse()
            if target_id in biz_total_dict:
                biz_total = biz_total_dict[target_id]
            else:
                biz_total.target_id = target_id
                biz_total_dict[target_id] = biz_total
            biz_total.title = biz_budget['target__name']
            biz_total.target_period = target_period_name
            plan_type = biz_budget['plan_type']
            if plan_type == BaseOptionDefine.Base.code:
                biz_total.biz_budget_base = biz_budget['amount']
            else:
                biz_total.biz_budget_option = biz_budget['amount']

        return biz_total_dict


class BaseDataMetaRelLogic:

    # baseDataName, id 指定で紐づくメタデータの Map を返す
    # 指定した baseDataName、ID に紐づくメタ情報の Map を返す
    # 戻り値は  Map<baseId, Map<MetaType, List<BaseDataMetaRel>>
    @staticmethod
    def get_meta_map(table, target_ids):
        """
        @type table : basestring
        @param table: 
        @type target_ids: list
        @param target_ids: 
        @return: 
        """
        meta_dict = {}
        if target_ids is None or len(target_ids) == 0:
            return meta_dict
        results = BaseDataMetaRel.objects.filter(Q(base_data_name=table) &
                                                 Q(base_data_id__in=target_ids)).\
            values('id', 'base_data_id', 'meta_type_id', 'meta_id')

        for result in results:
            rel = BaseDataMetaRelResponse()
            rel.id = result['id']
            rel.base_data_name = table
            rel.base_id = result['base_data_id']
            type_id = result['meta_type_id']
            meta_id = result['meta_id']

            try:
                info = MetaInfo.objects.get(Q(id=meta_id) & Q(meta_type=type_id))
            except ObjectDoesNotExist:
                info = None
                print(type_id)
                print("===================")
                print(meta_id)
            if info is None:
                continue

            info_response = MetaInfoResponse()
            info_response.id = info.id
            info_response.value = info.value

            meta_type_response = MetaTypeResponse()
            meta_type_response.id = info.meta_type.id
            meta_type_response.type = info.meta_type.meta_type
            meta_type_response.disp = info.meta_type.disp
            meta_type_response.grouping_target = info.meta_type.grouping_target
            meta_type_response.restriction = info.meta_type.restriction

            info_response.type = meta_type_response
            rel.info = info_response
            result_map = {}
            if rel.base_id in meta_dict:
                result_map = meta_dict[rel.base_id]

            meta_list = []
            if rel.info in result_map:
                meta_list = result_map[rel.info.type]
            meta_list.append(rel)
            result_map[rel.info.type] = meta_list
            meta_dict[rel.base_id] = result_map

        return meta_dict
