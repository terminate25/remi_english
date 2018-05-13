# -*- coding: utf-8 -*-
import datetime
import numbers
import os

from django.conf import settings

from default.models.models2 import BaseDataMetaRel
from helper.util import Format
from .util import GacoiFormFieldType, DbAgent


class ImportAdapter:
    """
    This class support importing data.
    It's format data to expected value (date, int, name map to code) and validate data.
    1) First use ExcelReader read_block to get data
    2) Call ImportAdapter format_data to check and prepare data
    3) Call ImportAdapter get_data to get formatted data
    4) Process data. Call ImportAdapter insert_meta_data_relation to update meta data

    """
    def __init__(self, start_col, end_col, start_row, base_data_name):
        """
        Col and row start by 1
        @param start_col:
        @param end_col:
        @param start_row:
        @param base_data_name: Base data name use to register meta
        """
        self.end_col = end_col
        self.start_col = start_col
        self.start_row = start_row
        self.base_data_name = base_data_name

        self.fields = {}
        self.data = []
        self.error_message = None

        self.date_format = None

    def get_field(self, field_name):
        """
        Get field
        @param field_name:
        @return:
        """
        if field_name not in self.fields:
            self.fields[field_name] = {}
            self.fields[field_name]['name'] = field_name
        return self.fields[field_name]

    def get_field_attribute(self, field_name, attribute, default=None):
        """
        Get attribute of a field
        @param field_name:
        @param attribute:
        @param default:
        @return:
        """
        field = self.get_field(field_name)
        if attribute in field:
            return field[attribute]
        return default

    def set_column(self, field_name, value):
        """
        Set column index of a field. column index start by 1.
        Note: column index count in formatted block data, not in excel file.
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['col'] = value

    def get_column(self, field_name):
        """
        Get column index of a field. column index start by 1.
        Note: column index count in formatted block data, not in excel file.
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'col')

    def set_max_length(self, field_name, value):
        """
        Set max length of a field. If field is number: max value of field. If field is string: max count of char
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['max_length'] = value

    def get_max_length(self, field_name):
        """
        Get max length of a field. If field is number: max value of field. If field is string: max count of char
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'max_length')

    def set_meta_type_name(self, field_name, value):
        """
        Set meta type name
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['meta_type_name'] = value

    def get_meta_type_name(self, field_name):
        """
        Get meta type name
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'meta_type_name')

    def set_meta_type_id(self, field_name, value):
        """
        Set meta type id
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['meta_type_id'] = value

    def get_meta_type_id(self, field_name):
        """
        Get meta type id
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'meta_type_id')

    def set_type(self, field_name, value):
        """
        Set data type of field
        @param field_name:
        @type value: GacoiFormFieldType
        @param value:
        @return:
        """
        self.get_field(field_name)['type'] = value

    def get_type(self, field_name):
        """
        Get type of field
        @param field_name:
        @return:
        @rtype: GacoiFormFieldType
        """
        return self.get_field_attribute(field_name, 'type')

    def set_title(self, field_name, value):
        """
        Set title of field
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['title'] = value

    def get_title(self, field_name):
        """
        Get title of field
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'title')

    def set_filters(self, field_name, value):
        """
        Set the values that not import (excluding value).
        If field's value match this filters, value converted to None
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['filters'] = value

    def get_filters(self, field_name):
        """
        Get list of excluding value
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'filters')

    def set_required(self, field_name, value=True):
        """
        Set field is required of not
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['required'] = value

    def is_required(self, field_name):
        """
        Check if field is required
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'required', False)

    def set_account_convert(self, field_name, value=True):
        """
        Set if field must convert customer account to internal account or not
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['account_convert'] = value

    def is_account_convert(self, field_name):
        """
        Check if field must convert customer account to internal account or not
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'account_convert', False)

    def set_value(self, field_name, value):
        """
        Set field's value
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['value'] = value

    def get_value(self, field_name):
        """
        Get values
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'value')

    def set_map(self, field_name, value):
        """
        Set map of name and code
        @param field_name:
        @param value:
        @return:
        """
        self.get_field(field_name)['map'] = value

    def get_map(self, field_name):
        """
        Get map of name and code
        @param field_name:
        @return:
        """
        return self.get_field_attribute(field_name, 'map')

    def set_insert_query(self, field_name, value):
        """
        Ex: insert into table_a (value) values ({0})
        @param field_name: 
        @param value: 
        @return: 
        """
        self.get_field(field_name)['query'] = value

    def get_insert_query(self, field_name):
        return self.get_field_attribute(field_name, 'query')

    def get_data(self):
        return self.data

    def set_data(self, value):
        self.data = value

    def format_data(self, raw_data, check=True):
        """
        Prepare data: convert name to code, check required, data type
        @param raw_data:
        @param check: if True, just check data, do not insert meta data
        @return: formatted data
        """
        account_map = ImportAdapter.get_account_code_map()

        self.data = []
        row = 0
        for arr in raw_data:
            rec = {}
            for field_name in self.fields:
                col = self.get_column(field_name)
                data_filter = self.get_filters(field_name)
                value = self.get_value(field_name)

                if value is not None:
                    rec[field_name] = value
                    continue

                # Check col
                if col >= len(arr):
                    self._create_error_message("{0}の項目は列番号{1}が存在しません。",
                                               row, col, self.get_title(field_name), col + 1)
                    return None

                if isinstance(arr[col], str):
                    value = arr[col].strip()
                else:
                    value = arr[col]

                if value == '':
                    value = None

                origin_value = value

                if data_filter is not None and value is not None:
                    if value in data_filter:
                        value = None

                # Check required
                if self.is_required(field_name) and value is None:
                    self._create_error_message("{0}の項目は必須です",
                                               row, col, self.get_title(field_name))
                    return None

                # Check type
                field_type = self.get_type(field_name)
                if field_type == GacoiFormFieldType.Number:
                    if value is not None:
                        if not isinstance(value, numbers.Number):
                            if isinstance(value, str):
                                if value.isdigit():
                                    value = int(value)

                        if not isinstance(value, numbers.Number):
                            self._create_error_message("{0}の項目は数字が必要です。{1}は数字ではありません。",
                                                       row, col, self.get_title(field_name), origin_value)

                            return None
                elif field_type == GacoiFormFieldType.DateTime or field_type == GacoiFormFieldType.Date:
                    if value is not None:

                        if not isinstance(value, datetime.date):
                            # covert
                            value = Format.to_date(value, self.date_format)

                        if value is None or not isinstance(value, datetime.date):
                            self._create_error_message("{0}の項目は日付型です。{1}は日付ではありません。",
                                                       row, col, self.get_title(field_name), origin_value)
                            return None

                # Check max_length
                max_length = self.get_max_length(field_name)
                if max_length:
                    if isinstance(value, int) and value > max_length:
                        self._create_error_message("{0}の項目の値「{1}」は設定した最大値「{2}」を超えました。",
                                                   row, col, self.get_title(field_name), origin_value, max_length)
                        return None
                    elif isinstance(value, str) and len(value) > max_length:
                        self._create_error_message("{0}の項目の値「{1}」は設定した文字長さ「{2}」を超えました。",
                                                   row, col, self.get_title(field_name), origin_value, max_length)
                        return None

                # Check account map
                if self.is_account_convert(field_name):
                    if value not in account_map:
                        self._create_error_message("{0}の項目の{1}は内部の内部のアカウントコードに変換できません。",
                                                   row, col, self.get_title(field_name), origin_value)
                        return None
                    else:
                        value = account_map[value]

                # Check map
                field_map = self.get_map(field_name)
                if field_map is not None:
                    if value in field_map:
                        if not check:
                            value = field_map[value]
                    else:
                        if value is not None and isinstance(value, str):
                            if self.get_insert_query(field_name):
                                if not check:
                                    new_id = DbAgent.execute_query(self.get_insert_query(field_name), [value])
                                    # Update map to avoid insert again
                                    field_map[value] = new_id
                                    value = new_id
                            else:
                                self._create_error_message("{0}の項目の「{1}」値はコードに変換できません。",
                                                           row, col, self.get_title(field_name), origin_value)
                                return None
                        else:
                            if isinstance(value, int):
                                pass
                            elif value is not None:
                                self._create_error_message("{0}の項目の「{1}」値はコードに変換できません。",
                                                           row, col, self.get_title(field_name), origin_value)
                                return None

                # OK
                rec[field_name] = value

            self.data.append(rec)

            row = row + 1
        return self.data

    def _create_error_message(self, message, row, col, *args):
        column_string = ImportAdapter.excel_column_string(self. start_col + col)

        self.error_message = "【{1}{0}】 {2}".format(self.start_row + row, column_string, message).\
            format(*args)

    def _get_have_meta_field(self):
        ret = list()
        for field_name in self.fields:
            meta_type_id = self.get_meta_type_id(field_name)
            if meta_type_id:
                ret.append(field_name)
        return ret

    def insert_meta_data_relation(self, base_data_ids, step=1):
        """
        Insert meta data relation to base_data_meta_rel
        @param base_data_ids: List of base data id
        @return:
        """
        meta_fields = self._get_have_meta_field()
        if not meta_fields:
            return

        # current_datetime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        meta_rel_list = []
        for idx in range(len(self.data)):
            for step_idx in range(step):
                rec = self.data[idx]
                base_data_idx = idx*step + step_idx
                if base_data_idx >= len(base_data_ids):
                    break
                base_data_id = base_data_ids[base_data_idx]

                for field_name in meta_fields:
                    meta_type_id = self.get_meta_type_id(field_name)
                    if not meta_type_id:
                        continue
                    if field_name not in rec or not isinstance(rec[field_name], numbers.Number):
                        continue
                    meta_rel = BaseDataMetaRel()
                    meta_rel.base_data_name = self.base_data_name
                    meta_rel.base_data_id = base_data_id
                    meta_rel.meta_type_id = meta_type_id
                    meta_rel.meta_id = rec[field_name]
                    meta_rel_list.append(meta_rel)

        if meta_rel_list:
            BaseDataMetaRel.objects.bulk_create(meta_rel_list)

    @staticmethod
    def move_uploaded_file(import_history_id, uploaded_file):
        """
        Move file to uploaded folder so can download later
        @param import_history_id:
        @param uploaded_file:
        @return:
        """
        archive_file = ImportAdapter.get_uploaded_file_path(import_history_id)
        os.rename(uploaded_file, archive_file)

    @staticmethod
    def get_uploaded_file_path(import_history_id, check_exists=False):
        """
        Get uploaded file path
        @param import_history_id:
        @param check_exists:
        @return:
        """
        ret = os.path.join(settings.BASE_DIR, 'uploaded', str(import_history_id))
        if check_exists and not os.path.isfile(ret):
            return None
        return ret

    @staticmethod
    def get_uploaded_file_name(import_history_id):
        """
        Get uploaded file name.
        @param import_history_id:
        @return:
        """
        from default.models.models2 import ImportHistory
        ih = ImportHistory.objects.get(pk=import_history_id)
        return ih.imported_filename

    @staticmethod
    def get_account_code_map():
        """
        Get map of customer account to internal account code
        @return:
        """
        from default.models.models2 import Account
        ret = dict()
        accounts = Account.objects.all()
        for account in accounts:
            ret[account.account_code] = account.id
        return ret

    @staticmethod
    def excel_column_string(n):
        div = n
        string = ""
        while div > 0:
            m = (div - 1) % 26
            string = chr(65 + m) + string
            div = int((div - m) / 26)
        return string
