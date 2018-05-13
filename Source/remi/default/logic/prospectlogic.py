from helper.importadapter import ImportAdapter
from default.logic.loglogic import LogOperation
from default.config.config_log import LogModule, LogResult, LogType
from helper.util import DbAgent
from default.config.config_common import AuthMetaTypeDefine, ImportDataType, AuthBaseDataName, \
    BaseDataName, ProspectTypeDefine, MetaTypeDefine
from default.models.models2 import BizProspect, BaseDataAuthMetaRel, BaseDataMetaRel, ImportHistory, \
    FiscalPeriod, FiscalTerm, AuthMetaType, Target, AuthMetaInfo, MetaInfo, User, MetaType
from django.db import transaction
from middleware.router import DatabaseRouter
import operator
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from default.logic.userlogic import LoginUser
from default.config.config_role import ModuleName
from default.config.config import Config
from default.logic.fiscaltermlogic import FiscalTermLogic
from datetime import datetime


class ProspectLogic:
    @staticmethod
    def get_import_history_list(owner_id):

        query = "select ih.*, dp.meta_id as department_id, lt.meta_id as latest from import_history ih " \
                "left join (select import_history_id, meta_id from biz_prospect bp " \
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
                                            AuthBaseDataName.BizProspect.value, AuthMetaTypeDefine.Department.code,
                                            AuthBaseDataName.ImportHistory.value, owner_id,
                                            ImportDataType.BizProspect.value])
        rs = rs[:5]
        return rs

    @staticmethod
    @transaction.atomic(using=DatabaseRouter.data_database)
    def import_prospect(target_term, department_id, owner_id, imported_filename, memo, adapter):
        """

        @param target_term: Term id
        @param department_id: Department id
        @param owner_id: Owner id
        @param memo: Memo
        @param adapter: Import adapter
        @param imported_filename: Imported file name
        @type adapter: ImportAdapter
        @return:
        """
        target_term = int(target_term)
        department_id = int(department_id)
        term = FiscalTerm.objects.get(pk=target_term)

        # Get all of id which will be delete: the same term, department and owner_id
        query = "select id from biz_prospect where " \
                "import_history_id in (select id from import_history where data_type=%s " \
                "and target_term=%s and user_id=%s) and " \
                "id in (select base_data_id from base_data_auth_meta_rel " \
                "where base_data_name=%s and meta_type_id=%s and meta_id=%s)"
        biz_prospect_ids = DbAgent.get_data_list(query, [ImportDataType.BizProspect.value,
                                                         target_term, owner_id, AuthBaseDataName.BizProspect.value,
                                                         AuthMetaTypeDefine.Department.code, department_id])

        # Delete history data
        BizProspect.objects.filter(id__in=biz_prospect_ids).delete()

        # Delete auth base meta relation
        BaseDataAuthMetaRel.objects.filter(base_data_id__in=biz_prospect_ids,
                                           base_data_name=AuthBaseDataName.BizProspect.value).delete()
        # Delete base meta data relation
        BaseDataMetaRel.objects.filter(base_data_id__in=biz_prospect_ids,
                                       base_data_name=BaseDataName.BizProspect.value).delete()

        # New import history
        ih = ImportHistory()
        ih.target_term_id = target_term
        ih.data_type = ImportDataType.BizProspect.value
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
        biz_prospects = []
        for rec in data:
            # check accrual_date is datetime or date
            if isinstance(rec['accrual_date'], datetime):
                rec['accrual_date'] = rec['accrual_date'].date()
            if not rec['accrual_date']:
                continue
            # Check if data not in term
            if rec['accrual_date'] < term.start_date or rec['accrual_date'] > term.end_date:
                continue

            biz_prospect = BizProspect()
            biz_prospect.owner_id = owner_id
            biz_prospect.type = rec['type']
            biz_prospect.title = rec['title']
            biz_prospect.amount = rec['amount']
            biz_prospect.opportunity_stage = rec['opportunity_stage']
            biz_prospect.target_id = rec['target_id']
            biz_prospect.accrual_date = rec['accrual_date']
            biz_prospect.settlement_date = rec['settlement_date']
            biz_prospect.import_history_id = ih.id
            biz_prospects.append(biz_prospect)

        BizProspect.objects.bulk_create(biz_prospects)

        # Get list id of imported data
        query = "select id from biz_prospect where " \
                "import_history_id = %s order by id"
        biz_prospect_ids = DbAgent.get_data_list(query, [ih.id])

        # Auth base meta relation for prospect data
        auth_metas = []
        for base_data_id in biz_prospect_ids:

            # Update auth meta data
            auth_meta = BaseDataAuthMetaRel()
            auth_meta.base_data_name = AuthBaseDataName.BizProspect.value
            auth_meta.base_data_id = base_data_id
            auth_meta.meta_type_id = AuthMetaTypeDefine.Department.code
            auth_meta.meta_id = department_id
            auth_metas.append(auth_meta)

        BaseDataAuthMetaRel.objects.bulk_create(auth_metas)

        # Update meta data
        adapter.insert_meta_data_relation(biz_prospect_ids)

        # Write log
        LogOperation.log(LogModule.BizProspect, LogType.Insert, LogResult.Success, ih.id)

        return ih.id

    @staticmethod
    def get_biz_prospect_import(term_number, data):
        """
        Import data: BizProspect
        Display data from excel file.
        Using pandas library to filter data
        Return data group by ('target_id', 'type'(account_id), 'opportunity_stage') and sum('amount')
        @param term_number: 
        @param data: 
        @return: 
        """
        if term_number < 0:
            return []

        if not data:
            return []
        try:
            fiscal_term = FiscalTerm.objects.get(term_number=term_number)
        except ObjectDoesNotExist:
            return []

        periods = FiscalPeriod.objects.filter(term_number=term_number).order_by('start_date')

        results = []
        group_by_keys = []  # key: target_id, type, opportunity_stage

        target_map = OrderedDict({})
        month_amount = OrderedDict({})
        # create amount for 12 months is 0
        for period in periods:
            month = period.name
            month_amount[month] = 0
        for target in data:
            target_id = target['target_id']
            account_type = target['type']
            opportunity_stage = target['opportunity_stage']
            accrual_date = target['accrual_date']
            amount = target['amount']
            key = (target_id, account_type, opportunity_stage)
            # add amount
            if key in group_by_keys:
                if isinstance(accrual_date, datetime):
                    accrual_date = accrual_date.date()
                # check accrual_date of target term
                if fiscal_term.start_date <= accrual_date <= fiscal_term.end_date:
                    month = str(accrual_date.month) + '月'
                    target_map[month] += amount
                    target_map['sum'] += amount
                else:
                    continue
            else:
                target_map = OrderedDict({})
                target_map['target_id'] = target_id
                target_map['account_type'] = account_type
                target_map['opportunity_stage'] = opportunity_stage
                target_map.update(month_amount)
                target_map['sum'] = 0
                if isinstance(accrual_date, datetime):
                    accrual_date = accrual_date.date()
                # check accrual_date of target term
                if fiscal_term.start_date <= accrual_date <= fiscal_term.end_date:
                    month = str(accrual_date.month) + '月'
                    target_map[month] = amount
                    target_map['sum'] = amount
                    results.append(target_map)
                    group_by_keys.append(key)
                else:
                    continue
        if results:
            results.sort(key=operator.itemgetter('target_id'))
        return results

    @staticmethod
    def get_current_data(term_number):
        """
        Retrieve data from table by term_number.
        @param term_number: fiscal term
        @type term_number: int
        @return: 
        """
        user = LoginUser.get_login_user()

        fiscal = FiscalTerm.objects.get(term_number=int(term_number))
        periods = FiscalTermLogic.get_term_period_list(int(term_number))
        auth_meta_types = AuthMetaType.objects.all().order_by("meta_type")

        from helper.util import StringBuilder
        query = StringBuilder()
        query_from = StringBuilder()
        query_group_by = StringBuilder()
        query_order_by = StringBuilder()

        main_fields = "target_id, type, opportunity_stage"  # target_id

        query_from.append("\nfrom biz_prospect bz")
        query_group_by.append("\ngroup by {0}".format(main_fields))
        query.append("select {0}".format(main_fields))

        # Auth meta
        for meta_type in auth_meta_types:
            # Only department
            if meta_type.meta_type == AuthMetaTypeDefine.Department.title:
                in_query = user.get_filtered_query_string(ModuleName.BizProspect,
                                                          AuthMetaTypeDefine.Department.code)
                # len > 0
                if in_query is not None and len(in_query) > 0:
                    query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
                    query_from.append(" inner join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                                      "and bz.id={0}.base_data_id and {0}.meta_type_id={2} and {0}.meta_id in ({3})".
                                      format(meta_type.meta_type,
                                             AuthBaseDataName.BizProspect.value, meta_type.id, in_query))
                    query_group_by.append(", {0}.meta_id".format(meta_type.meta_type))
                    query_order_by.append(", {0}.meta_id".format(meta_type.meta_type))
                # config_role is None
                elif in_query is None:
                    query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
                    query_from.append(" inner join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                                      "and bz.id={0}.base_data_id and {0}.meta_type_id={2} ".
                                      format(meta_type.meta_type,
                                             AuthBaseDataName.BizProspect.value, meta_type.id))
                    query_group_by.append(", {0}.meta_id".format(meta_type.meta_type))
                    query_order_by.append(", {0}.meta_id".format(meta_type.meta_type))
                # len = 0
                else:
                    return []

        # Sum by 12 month
        for i in range(periods.count()):
            query.append(", sum(case when accrual_date >= '{0}' and accrual_date <= '{1}' "
                         "then amount else 0 end) as '{2}'".
                         format(periods[i].start_date, periods[i].end_date, periods[i].start_date.month))

        query.append(", sum(amount) as summary")

        query_order_by.append(", {0}".format(main_fields))
        query.append(query_from)
        query.append(" \nwhere accrual_date >= '{0}' and accrual_date <= '{1}' ".format(fiscal.start_date,
                                                                                        fiscal.end_date))
        query.append(query_group_by)
        query.append(" \norder by {0}".format(str(query_order_by)[1:]))

        results = DbAgent.get_record_set(str(query))

        return results

    @staticmethod
    def get_term_import_history_list(term_number):
        """
        Retrieve data from table by term_number:
            1. import_history: user_id, owner_id, memo, last_import_date
            2. user_filter: meta_type by user_id
            3. auth_meta_type: 
            4. base_data_auth_meta_rel: 
            5. biz_prospect: target_id, type, opportunity_stage by owner_id
        @param term_number: fiscal term
        @type term_number: int
        @return: 
        """
        user = LoginUser.get_login_user()
        in_query = user.get_filtered_query_string(ModuleName.BizProspect, AuthMetaTypeDefine.Department.code)
        results_map = dict()
        # len > 0
        if in_query is not None and len(in_query) > 0:
            query = "select ih.*, lt.meta_id as department_id from import_history ih " \
                    "inner join (select import_history_id, meta_id from biz_prospect bp " \
                    "inner join base_data_auth_meta_rel bd on bd.meta_type_id=%s " \
                    "and bd.base_data_name=%s and bp.id=bd.base_data_id and bd.meta_id in ({0})" \
                    "group by import_history_id, meta_id) lt " \
                    "on ih.id = lt.import_history_id " \
                    "where ih.target_term=%s and ih.data_type=%s " \
                    "order by lt.meta_id,imported_datetime desc".format(in_query)
        # config_role is None
        elif in_query is None:
            query = "select ih.*, lt.meta_id as department_id from import_history ih " \
                    "inner join (select import_history_id, meta_id from biz_prospect bp " \
                    "inner join base_data_auth_meta_rel bd on bd.meta_type_id=%s " \
                    "and bd.base_data_name=%s and bp.id=bd.base_data_id " \
                    "group by import_history_id, meta_id) lt " \
                    "on ih.id = lt.import_history_id " \
                    "where ih.target_term=%s and ih.data_type=%s " \
                    "order by lt.meta_id,imported_datetime desc"
        # len = 0
        else:
            return {}

        results = DbAgent.get_record_set(query, [AuthMetaTypeDefine.Department.code,
                                                 AuthBaseDataName.BizProspect.value, int(term_number),
                                                 ImportDataType.BizProspect.value])
        # map results to view in template
        for result in results:
            department_id = result['department_id']
            if department_id in results_map:
                results_map[department_id].append(result)
            else:
                department_value = []
                results_map[department_id] = department_value
                results_map[department_id].append(result)
        return results_map

    @staticmethod
    def get_month_data(term_number, department_id):
        """
        Retrieve data from table by term_number and department_id:
            1. import_history: user_id, owner_id, memo, last_import_date
            2. user_filter: meta_type by user_id
            3. auth_meta_type: 
            4. base_data_auth_meta_rel: 
            5. biz_prospect: target_id, type, opportunity_stage by owner_id
        @param term_number: fiscal term
        @param department_id: auth meta type id
        @type term_number: int
        @type department_id: int
        @return: 
        """

        periods = FiscalTermLogic.get_term_period_list(int(term_number))
        auth_meta_type = AuthMetaType.objects.get(id=AuthMetaTypeDefine.Department.code)

        from helper.util import StringBuilder
        query = StringBuilder()
        query_from = StringBuilder()
        query_group_by = StringBuilder()
        query_order_by = StringBuilder()

        main_fields = "target_id, type, opportunity_stage"  # target_id

        query_from.append("\nfrom biz_prospect bz")
        query_group_by.append("\ngroup by {0}".format(main_fields))
        query.append("select {0}".format(main_fields))

        # Auth meta
        if auth_meta_type.meta_type == AuthMetaTypeDefine.Department.title:
            query.append(", {0}.meta_id as {0}".format(auth_meta_type.meta_type))
            query_from.append(" inner join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                              "and bz.id={0}.base_data_id and {0}.meta_type_id={2} and {0}.meta_id={3}".
                              format(auth_meta_type.meta_type,
                                     AuthBaseDataName.BizProspect.value,
                                     auth_meta_type.id,
                                     int(department_id)))
            query_group_by.append(", {0}.meta_id".format(auth_meta_type.meta_type))
            query_order_by.append(", {0}.meta_id".format(auth_meta_type.meta_type))

        # Sum by 12 month
        for i in range(periods.count()):
            query.append(", sum(case when accrual_date >= '{0}' and accrual_date <= '{1}' "
                         "then amount else 0 end) as '{2}'".
                         format(periods[i].start_date, periods[i].end_date, periods[i].start_date.month))

        query_order_by.append(", {0}".format(main_fields))
        query.append(query_from)

        query.append(query_group_by)
        query.append(" \norder by {0}".format(str(query_order_by)[1:]))

        results = DbAgent.get_record_set(str(query))
        depart_month_final = []
        depart_month_sum_map = dict()
        # map results to view in template
        for target in results:
            depart_month_map = OrderedDict({})
            target_id = target['target_id']
            prospect_type = target['type']
            opportunity_stage = target['opportunity_stage']

            try:
                target_name = Target.objects.get(id=target_id).name
            except ObjectDoesNotExist:
                target_name = ''
            depart_month_map['target_name'] = target_name
            # map prospect type
            if prospect_type == ProspectTypeDefine.Revenue.code:
                depart_month_map['prospect_type'] = ProspectTypeDefine.Revenue.value[1]
            elif prospect_type == ProspectTypeDefine.Outsourcing.code:
                depart_month_map['prospect_type'] = ProspectTypeDefine.Outsourcing.value[1]
            else:
                depart_month_map['prospect_type'] = ''

            # map opportunity stage
            depart_month_map['opportunity_stage'] = \
                Config.get_code_to_name_map('opportunity_stage')[opportunity_stage]

            target_month_map = OrderedDict({})
            # add mount to 12 months
            for period in periods:
                target_month_map[period.start_date.month] = round(target[str(period.start_date.month)] / 1000)
                if period.start_date.month in depart_month_sum_map:
                    depart_month_sum_map[period.start_date.month] += int(target[str(period.start_date.month)])
                else:
                    depart_month_sum_map[period.start_date.month] = int(target[str(period.start_date.month)])
            depart_month_map['month'] = target_month_map
            depart_month_map['sum'] = sum(depart_month_map['month'].values())
            if depart_month_map['sum'] != 0:
                depart_month_final.append(depart_month_map)

        return depart_month_final

    @staticmethod
    def get_detail_data(term_number, department_id, month_id):
        """
        Retrieve data from table by term_number, department_id, month_id:
            1. import_history: user_id, owner_id, memo, last_import_date
            2. user_filter: meta_type by user_id
            3. auth_meta_type: 
            4. base_data_auth_meta_rel: 
            5. biz_prospect: target_id, type, opportunity_stage by owner_id
        @param term_number: fiscal term
        @param department_id: auth meta type id
        @param month_id: month
        @type term_number: int
        @type department_id: int
        @type month_id: int
        @return: 
        """

        periods = FiscalTermLogic.get_term_period_list(int(term_number))
        period = periods.get(name=str(month_id) + '月')
        auth_meta_type = AuthMetaType.objects.get(id=AuthMetaTypeDefine.Department.code)
        meta_types = MetaType.objects.all().order_by("meta_type")

        from helper.util import StringBuilder
        query = StringBuilder()
        query_from = StringBuilder()
        query_order_by = StringBuilder()

        main_fields = "*"

        query_from.append("\nfrom biz_prospect bz")
        query.append("select {0}".format(main_fields))

        if auth_meta_type.meta_type == AuthMetaTypeDefine.Department.title:
            query.append(", {0}.meta_id as {0}".format(auth_meta_type.meta_type))
            query_from.append(" inner join base_data_auth_meta_rel {0} on {0}.base_data_name='{1}' "
                              "and bz.id={0}.base_data_id and {0}.meta_type_id={2} and {0}.meta_id={3}".
                              format(auth_meta_type.meta_type,
                                     AuthBaseDataName.BizProspect.value,
                                     auth_meta_type.id,
                                     int(department_id)))
            query_order_by.append(", {0}.meta_id".format(auth_meta_type.meta_type))

        # Meta
        for meta_type in meta_types:
            # Only staff
            if meta_type.id in [MetaTypeDefine.Staff.code,
                                MetaTypeDefine.Product.code,
                                MetaTypeDefine.Partner.code]:
                query.append(", {0}.meta_id as {0}".format(meta_type.meta_type))
                query_from.append(" left join base_data_meta_rel {0} on {0}.base_data_name='{1}' "
                                  "and bz.id={0}.base_data_id and {0}.meta_type_id={2}".
                                  format(meta_type.meta_type, AuthBaseDataName.BizProspect.value, meta_type.id))

        query.append(", import_history.user_id as user_id")
        query_from.append(" inner join import_history on bz.import_history_id=import_history.id")

        query_order_by.append(", {0}".format('target_id'))
        query.append(query_from)
        query.append(" \nwhere accrual_date >= '{0}' and accrual_date <= '{1}'".
                     format(period.start_date, period.end_date))

        results = DbAgent.get_record_set(str(query))
        month_detail_final = []
        # map results to view in template
        for target in results:
            target_id = target['target_id']  # target name and product name
            prospect_type = target['type']  # account type
            opportunity_stage = target['opportunity_stage']
            try:
                product_name = MetaInfo.objects.get(id=target['product']).value
            except ObjectDoesNotExist:
                product_name = ''
            try:
                partner_name = MetaInfo.objects.get(id=target['partner']).value
            except ObjectDoesNotExist:
                partner_name = ''
            try:
                staff_name = MetaInfo.objects.get(id=target['staff']).value
            except ObjectDoesNotExist:
                staff_name = ''
            # retrieve target name
            try:
                target_name = Target.objects.get(id=target_id).name
            except ObjectDoesNotExist:
                target_name = ''

            try:
                username = User.objects.get(id=target['user_id']).user_name
            except ObjectDoesNotExist:
                username = ''
            target_map = dict()
            target_map['title'] = target['title']
            target_map['target_name'] = target_name
            # map prospect_type
            if prospect_type == ProspectTypeDefine.Revenue.code:
                target_map['prospect_type'] = ProspectTypeDefine.Revenue.value[1]
            elif prospect_type == ProspectTypeDefine.Outsourcing.code:
                target_map['prospect_type'] = ProspectTypeDefine.Outsourcing.value[1]
            else:
                target_map['prospect_type'] = ''

            # map opportunity_stage to A, B, C
            target_map['opportunity_stage'] = \
                Config.get_code_to_name_map('opportunity_stage')[opportunity_stage]

            target_map['amount'] = round(target['amount'] / 1000)
            target_map['accrual_date'] = target['accrual_date']
            target_map['settlement_date'] = target['settlement_date']
            target_map['staff_name'] = staff_name
            target_map['product_name'] = product_name
            target_map['partner_name'] = partner_name
            target_map['username'] = username
            month_detail_final.append(target_map)

        return month_detail_final
