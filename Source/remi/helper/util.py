# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import html
import locale
import numbers
import os
import re
from collections import OrderedDict
from enum import Enum
import math
from sqlalchemy.sql.expression import literal_column


from six import PY2, text_type

from default.config.config_appearance import *
from middleware.router import DatabaseRouter

# if os.name == 'nt':
#     locale.setlocale(locale.LC_CTYPE, 'Japanese')
# else:
#     locale.setlocale(locale.LC_CTYPE, 'ja_JP.UTF-8')


class UserButton:
    """
    Button to add GacoiForm form. This button is added below the form.
    """
    def __init__(self, display, action, validate=False, link=None):
        """
        Button
        @param display: button value
        @param action: javascript function name
        @param validate: If true, validate form when click button
        @param link: url
        """
        self.display = display
        self.validate = validate
        self.action = action
        self.link = link


class InlineUserButton:
    def __init__(self, display, return_value, validate=False, action=None):
        """
        Button to add GacoiForm form. This button is added at the right of each row in grid form.
        @param display: button value
        @param return_value: javascript function name
        @param validate: If true, validate form when click button
        """
        self.display = display
        self.validate = validate
        self.return_value = return_value
        self.action = action


class StringBuilder:
    """
    String concat supporting class
    """
    _file_str = None

    def __init__(self):
        self._file_str = []

    def append(self, value):
        if isinstance(value, numbers.Number):
            self._file_str.append(str(value))
        elif isinstance(value, StringBuilder):
            self._file_str.extend(value._file_str)
        else:
            self._file_str.append(value)

    def __str__(self):
        return ''.join(self._file_str)


class GacoiFormAction(Enum):
    """
    Define action of a Gacoi form
    """
    InsertStart = 1
    InsertDone = 2
    UpdateStart = 3
    UpdateDone = 4
    DeleteDone = 5
    SearchDone = 6


class GacoiFormFieldType(Enum):
    """
    Field data type of a field in GacoiForm
    """
    Number = 1
    Date = 2
    Text = 3
    File = 4
    Boolean = 11
    TextArea = 5
    DateTime = 6
    Time = 7
    Password = 8
    Checkbox = 9
    Radio = 10


class GacoiFormViewType(Enum):
    """
    Form type. 2 kind of form. Single form (tabular from) and grid form.
    """
    GridView = 1
    FormView = 2


class GacoiField:
    """
    A field in GacoiForm. Its have some attribute
    """
    name = None
    attribute = {}

    def __init__(self, name):
        self.name = name
        self.attribute = {}

    def get(self, key, default=None):
        """
        Get attribute of field by key
        @param key:
        @param default:
        @return:
        """
        if key in self.attribute:
            return self.attribute[key]
        else:
            return default

    def set(self, key, value):
        """
        Set attribute of field by value
        @param key:
        @param value:
        @return:
        """
        self.attribute[key] = value

    def get_type(self, default=None):
        """
        Type
        @param default:
        @return:
        """
        return self.get("type", default)

    def set_type(self, value):
        """
        Type
        @param value:
        @return:
        """
        self.set("type", value)

    def get_column_width(self, default=None):
        """
        Column width
        @param default:
        @return:
        """
        return self.get("column_width", default)

    def get_column_width_css(self, default=''):
        """
        Column width as style='width:10px'
        @param default:
        @return: '' if have not set
        """
        column_width = self.get_column_width()

        if column_width:
            return ' style="width: {0}" '.format(column_width)
        return default

    def set_column_width(self, value):
        """
        Column width
        @param value:
        @return:
        """
        self.set("column_width", value)

    def get_decimal_point(self, default=None):
        """
        Decimal point
        @param default:
        @return:
        """
        return self.get("decimal", default)

    def set_decimal_point(self, value):
        """
        Decimal point
        @param value:
        @return:
        """
        self.set("decimal", value)

    def get_number_unit(self, default=None):
        """
        Number unit. Ex: When it set to 1000, field value divided 1000 before showed
        @param default:
        @return:
        """
        return self.get("number_unit", default)

    def set_number_unit(self, value):
        """
        Number unit. Ex: When it set to 1000, field value divided 1000 before showed
        @param value:
        @return:
        """
        self.set("number_unit", value)

    def get_value_blank2none(self, default=None):
        """
        Get field value. If blank (empty string), return None
        @param default:
        @return:
        """
        value = self.get("value", default)
        if value == '':
            return None
        return value

    def get_value_none2blank(self, default=''):
        """
        Get field value. Inf None, return blank
        @param default:
        @return:
        """
        value = self.get("value", default)
        if value is None:
            return ''
        return value

    def get_search_value(self, default=None):
        """
        Get search inputed value of field
        @param default:
        @return:
        """
        return self.get("search_value", default)

    def set_search_value(self, value):
        """
        Set search input value. This function is called in init method
        @param value:
        @return:
        """
        self.set("search_value", value)

    def get_value(self, default=None):
        """
        Get field value
        @param default:
        @return:
        """
        ret = self.get("value", default)
        if ret is None:
            return self.get_default(default)
        return ret

    def set_value(self, value):
        """
        Set field value. This function is called in init method
        @param value:
        @return:
        """
        self.set("value", value)

    def get_caption(self):
        """
        Get caption of field.
        @return:
        """
        caption = self.get("caption", None)
        if caption is None:
            return self.name
        else:
            return caption

    def set_caption(self, value):
        """
        Caption of field
        @param value:
        @return:
        """
        self.set("caption", value)

    def get_link(self, default=None):
        """
        Field's url
        @param default:
        @return:
        """
        return self.get("link", default)

    def set_link(self, value):
        """
        Field url
        @param value:
        @return:
        """
        self.set("link", value)

    def get_header_link(self, default=None):
        """
        Grid form header's url
        @param default:
        @return:
        """
        return self.get("header_link", default)

    def set_header_link(self, value):
        """
        Grid from header's url
        @param value:
        @return:
        """
        self.set("header_link", value)

    def get_drop_down_list_values(self, default=None):
        """
        Content of drop down list attach with field
        @param default:
        @return:
        """
        return self.get("dropdown", default)

    def is_drop_down_list_all_value(self):
        return self.get("dropdown_all_value")

    def set_keep_value_in_insert(self,keep=False):
        return self.set("keep_value_in_insert",keep)

    def is_keep_value_in_insert(self):
        return self.get("keep_value_in_insert")

    def set_drop_down_list_values(self, value, all_value=True):
        """
        Content of drop down list attach with field.
        It's a dict
        @param value: dict
        @return:
        """
        self.set("dropdown", value)
        self.set("dropdown_all_value",all_value)

    def get_default(self, default=""):
        """
        Field default value
        @param default:
        @return:
        """
        return self.get("default", default)

    def set_default(self, value):
        """
        Field default value
        @param value:
        @return:
        """
        self.set("default", value)

    def is_required(self, default=None):
        """
        Required
        @param default:
        @return:
        """
        return self.get("required", default)

    def set_required(self, value=True):
        """
        Required
        @param value:
        @return:
        """
        self.set("required", value)

    def is_search(self, default=None):
        """
        Field can be search or not
        @param default:
        @return:
        """
        return self.get("search", default)

    def set_search(self, value=True):
        """
        Field can be search or not
        @param value:
        @return:
        """
        self.set("search", value)

    def get_order(self, default=None):
        """
        Field can be sort or not
        @param default:
        @return:
        """
        return self.get("order", default)

    def set_order(self, value=True):
        """
        Field can be sort or not
        @param value:
        @return:
        """
        self.set("order", value)

    def is_key(self, default=None):
        """
        Key field
        @param default:
        @return:
        """
        return self.get("key", default)

    def set_key(self, value=True):
        """
        Key field
        @param value:
        @return:
        """
        self.set("key", value)

    def is_nowrap(self, default=None):
        """
        Field nowrap
        @param default:
        @return:
        """
        return self.get("nowrap", default)

    def set_nowrap(self, value=True):
        """
        Field nowrap
        @param value:
        @return:
        """
        self.set("nowrap", value)

    def is_view(self, default=None):
        """
        Field will be showed or not
        @param default:
        @return:
        """
        return self.get("view", default)

    def set_view(self, value=True):
        """
        Field will be showed or not
        @param value:
        @return:
        """
        self.set("view", value)

    def is_update(self, default=None):
        """
        Field will be updated or not
        @param default:
        @return:
        """
        return self.get("update", default)

    def set_update(self, value=True):
        """
        Field will be updated or not
        @param value:
        @return:
        """
        self.set("update", value)

    def is_insert(self, default=None):
        """
        Field will be added or not
        @param default:
        @return:
        """
        return self.get("insert", default)

    def set_insert(self, value=True):
        """
        Field will be added or not
        @param value:
        @return:
        """
        self.set("insert", value)

    def is_summary(self, default=None):
        """
        Summary in grid
        @param default:
        @return:
        """
        return self.get("summary", default)

    def set_summary(self, value=True):
        """
        Summary in grid
        @param value:
        @return:
        """
        self.set("summary", value)

    def set_bitwise_value(self, state=False):
        self.set("bitwise_state", state)

    def is_bitwise(self):
        return self.get("bitwise_state")

    def set_multi_choices(self, master_data_query, selected_data_query, cols=3):
        """
        Multi choices fields. This field will be shown as list of check box (table).
        @param master_data_query: Master of multi choices value. Query or Enum class
        @param selected_data_query: Selected data. It's a list
        @param cols: number of cols of check box table
        @return:
        """
        self.set("multi_choices_selected_query", selected_data_query)
        self.set("multi_choices_master_query", master_data_query)
        self.set("multi_choices_cols", cols)

    def is_multi_choices(self):
        """
        Check if field is  multi choices field.
        @return:
        """
        return self.get("multi_choices_master_query") is not None

    def get_multi_choices_selected_query(self):
        """

        @return:
        """
        return self.get("multi_choices_selected_query")

    def get_multi_choices_master_query(self):
        """

        @return:
        """
        return self.get("multi_choices_master_query")

    def get_multi_choices_cols(self):
        """

        @return:
        """
        return self.get("multi_choices_cols", 3)

    def get_multi_choices_selected_values(self):
        """

        @return:
        """
        return self.get("multi_choices_selected_values")

    def set_multi_choices_selected_values(self, values):
        """

        @param values:
        @return:
        """
        self.set("multi_choices_selected_values", values)

    def get_multi_choices_master_values(self):
        """

        @return:
        """
        return self.get("multi_choices_master_values")

    def set_multi_choices_master_values(self, values):
        """

        @param values:
        @return:
        """
        self.set("multi_choices_master_values", values)

    def set_checked_value(self, value=None):
        """
        It call in init method to set value of radio field.
        @param value:
        @return:
        """
        self.set("checked_value", value)

    def set_checked_values(self, values=None):
        """
        It call in init method to set value of check box field.
        @param values:
        @return:
        """
        self.set("checked_values", values)

    def get_value_expression(self, default=None):
        """
        Value expression for check box and radio field. When field is checked, field will return this value.
        Value expression is evaluated before set to field.
        Ex: [a] + '_' + [b] : field return value of field a and b as a_b
        @param default:
        @return:
        """
        return self.get("value_expression", default)

    def get_checked_values(self, default=None):
        """
        Get checked values of check box field.
        @param default:
        @return:
        """
        return self.get("checked_values", default)

    def get_checked_value(self, default=None):
        """
        Get checked value of radio box field
        @param default:
        @return:
        """
        return self.get("checked_value", default)

    def set_check_box(self, value_expression, values=None):
        """
        Set the field is the check box field.
        It work in Grid from. It show check box at each row to select data
        @param value_expression: Ex. [id]
        @param values: list of selected value
        @return:
        """
        self.set_type(GacoiFormFieldType.Checkbox)
        self.set("value_expression", value_expression)
        self.set_checked_values(values)

    def set_radio_box(self, value_expression, value=None):
        """
        Set the field is the radio box field.
        It work in Grid from. It show radio box at each row to select data
        @param value_expression: Ex. [id]
        @param value: selected value
        @return:
        """
        self.set_type(GacoiFormFieldType.Radio)
        self.set("value_expression", value_expression)
        self.set_checked_values(value)


class GacoiForm:
    """
    This is wrapping of a form, maybe Grid form or Tabular form.

    """
    name = None
    formAction = None
    hiddenFields = None
    fields = None
    action = None
    method = None
    selectedRow = None
    keyValues = None
    info_message = None
    error_message = None
    popup_message = None
    relate_fields = None

    form_data = None
    form_data_model = None
    userButtons = None
    inlineUserButtons = None
    inline_user_button_return_value = None
    header_link_return_value = None
    option_update_in_form_view = False
    option_deletable = False
    option_form_label_col = 2
    max_record_per_page = None
    next_page_index = 1
    page_tab_number = 5


    def set_error_message(self, message=None):
        self.error_message = message

    def set_info_message(self, message=None):
        self.info_message = message

    def set_popup_message(self, message=None):
        self.popup_message = message

    languages = {"insert new": "Insert New",
                 "back": "Back", "save": "Save",
                 "Are you sure to delete?": "Are you sure to delete?",
                 "This is required item.": "This is required item."
                 }

    def __init__(self, name, form_action="", method="POST"):
        self.name = name
        self.formAction = form_action
        self.hiddenFields = {}
        self.fields = OrderedDict()
        self.viewType = GacoiFormViewType.GridView
        self.method = method
        self.keyValues = {}
        self.is_search = False
        self.order_field = None
        self.order_type = None
        self.current_menu_state = 1

    @staticmethod
    def lang(name, default=None):
        if name in GacoiForm.languages:
            return GacoiForm.languages[name]
        if default is None:
            return name
        return default

    def get_current_menu_state(self):
        return self.current_menu_state

    def set_current_menu_state(self, menu_state):
        self.current_menu_state = menu_state

    def set_paging_value(self, max_record):
        self.max_record_per_page = max_record

    def get_paging_value(self):
        return self.max_record_per_page

    def add_field_relate(self, father_field, children_field, parent_child_dict):
        if self.relate_fields is None:
            self.relate_fields = []
        relate_dict = {
            "father_field": father_field,
            "children_field": children_field,
            "parent_child_dict": parent_child_dict
        }
        self.relate_fields.append(relate_dict)

    def set_hidden(self, field, value):
        """
        Hidden field
        @param field:
        @param value:
        @return:
        """
        self.hiddenFields[field] = value

    def render_form_begin(self):
        """
        Show form start tag. Form's hidden field is rendered here.
        @return:
        """
        sb = StringBuilder()

        if self.viewType == GacoiFormViewType.FormView or self.is_action(GacoiFormAction.InsertStart) or \
                (self.is_action(GacoiFormAction.UpdateStart) and self.get_option_update_in_form_view()):
            form_class = "class='form-horizontal'"
        else:
            form_class = ""
        # Form start
        sb.append("<form enctype='multipart/form-data' name='{0}' action='{1}' method='{2}' id='{0}-id' {3}>\n"
                  .format(self.name, self.formAction, self.method, form_class))

        # Echo hidden field
        sb.append("<input type='hidden' name='{0}_action'>\n".format(self.name))
        sb.append("<input type='hidden' name='current_menu_state' value='{0}'>\n".format(self.current_menu_state))
        for name, field in self.fields.items():
            if field.is_drop_down_list_all_value() is not None and not field.is_drop_down_list_all_value():
                sb.append("<input type='hidden' name='search_{0}_keep' value='{1}'>\n".format(name, field.get_search_value()))

        if self.order_field is not None:
            sb.append("<input type='hidden' name='{0}_order_field' value='{1}'>\n".format(self.name, self.order_field))
        else:
            sb.append("<input type='hidden' name='{0}_order_field' value=''>\n".format(self.name))

        sb.append("<input type='hidden' name='{0}_order_type' value='{1}'>\n".format(self.name, self.order_type))
        sb.append("<input type='hidden' name='{0}_inline_user_button_return_value'>\n".format(self.name))
        sb.append("<input type='hidden' name='{0}_header_link_return_value'>\n".format(self.name))
        sb.append("<input type='hidden' name='{0}_next_page_index' value='{1}'>\n".format(self.name, self.next_page_index))
        if self.is_action(GacoiFormAction.UpdateStart):
            sb.append("<input type='hidden' name='{0}_selected_row' value={1}>\n".format(self.name, self.selectedRow))
        else:
            sb.append("<input type='hidden' name='{0}_selected_row'>\n".format(self.name))

        for key, value in self.hiddenFields.items():
            sb.append("<input type='hidden' name='{0}' value='{1}'>\n".format(key, value))

        return sb.__str__()

    @staticmethod
    def render_form_end():
        """
        Render form end tag
        @return:
        """
        return "</form>"

    def render_content(self):
        """
        Render form content.

        @return:
        """
        print("Start render content {0}".format(datetime.datetime.today()))
        sb = StringBuilder()
        if self.popup_message is not None:
            sb.append('<script>'
                      '$( document ).ready(function() {{ bootbox.alert("{0}") }});</script>'.
                      format(self.popup_message.replace('"', '\\"')))

        if self.viewType == GacoiFormViewType.GridView:
            if self.is_action(GacoiFormAction.InsertStart):
                sb.append(self.render_form_view_content())
            elif self.is_action(GacoiFormAction.UpdateStart) and self.get_option_update_in_form_view():
                sb.append(self.render_form_view_content())
            else:
                sb.append(self.render_grid_view_content())
        else:
            sb.append(self.render_form_view_content())
        print("End render content {0}".format(datetime.datetime.today()))
        return str(sb)

    def set_values(self, data):
        """
        Set all value of fields from data.
        @param data: dict or Django model
        @return:
        """
        try:
            if data is None:
                # Set data for search fields
                for name, field in self.fields.items():
                    field.set_value(field.get_search_value())
            else:
                if isinstance(data, dict):
                    dicts = data
                else:
                    dicts = data.__dict__
                for name, field in self.fields.items():
                    # Not fair, but django convert ForeignKey to ..._id
                    if name not in dicts:
                        name = "{0}_id".format(name)

                    if name in dicts:
                        field.set_value(dicts[name])

        except ValueError:
            pass

    @staticmethod
    def _prepare_multi_choices_master(field):
        """
        Prepare the dict of master of multi choices field
        @param field:
        @return:
        """
        master = field.get_multi_choices_master_values()
        if master:
            return
        query = field.get_multi_choices_master_query()

        if isinstance(query, str):
            master = DbAgent.get_data_map(query)
        elif isinstance(query, dict):
            master = query
        else:
            # if issubclass(query, Enum):
            master = Util.enum_to_dict(query)

        field.set_multi_choices_master_values(master)

    def render_field_edit_mode(self, field, search_mode=False):
        """
        Render a field in editable status
        @type field: GacoiField
        @param field:
        @param search_mode:
        @return:
        """
        if isinstance(field, str):
            field = self.get_field(field)

        if search_mode:
            field_name = "search_{0}".format(field.name)
        else:
            field_name = "{0}".format(field.name)

        sb = StringBuilder()

        if field.get_type() == GacoiFormFieldType.File:
            sb.append('<input type="file" name="{0}">'.format(field_name))
            return sb.__str__()

        dropdown = field.get_drop_down_list_values()
        if dropdown is not None:
            sb.append('<select  class="form-control form-control-sm" name="{0}" class="chosen-select">'.format(field_name))
            if search_mode:
                if field.is_drop_down_list_all_value():
                    sb.append("<option value=''></option>")

            for key, value in dropdown.items():
                selected = ''
                field_value = str(field.get_value())
                if field.is_keep_value_in_insert():
                    field_value = str(field.get_search_value())
                if field_value == str(key):
                    selected = 'selected'
                sb.append("<option value='{0}' {1}>{2}</option>".format(key, selected, value))
            sb.append('</select>')
        elif field.is_multi_choices():
            GacoiForm._prepare_multi_choices_master(field)
            master = field.get_multi_choices_master_values()
            cols = field.get_multi_choices_cols()

            if self.is_action(GacoiFormAction.InsertStart):
                checked_values = []
            else:
                if search_mode:
                    checked_values = field.get_search_value()
                else:
                    query = field.get_multi_choices_selected_query()
                    if query is None:
                        checked_values = field.get_multi_choices_selected_values()
                    else:
                        query = self.apply_parameter(query)
                        checked_values = DbAgent.get_data_list(query)
            sb.append('<table>')
            count = 0
            sb.append('<tr style="line-height: 20px;">')
            for key, value in master.items():
                sb.append('<td style="border:0px;">')
                checked = ''
                if checked_values is not None and (key in checked_values or str(key) in checked_values):
                    checked = 'checked'
                sb.append('<input type="checkbox" class="ace" value="{2}" name="{0}" {1}/> '
                          '<span class="lbl">{3}&nbsp;&nbsp;</span>'
                          .format(field_name, checked, key, value))
                sb.append('</td>')
                count += 1
                if count % cols == 0:
                    sb.append('</tr><tr style="line-height: 20px;">')
            sb.append('<tr>')

            sb.append('</table>')

        else:
            field_type = field.get_type()
            if field_type == GacoiFormFieldType.Date:
                sb.append('<input type="text" class="form-control date-picker" '
                          'value="{0}" name="{1}">'
                          .format(Format.format_date(field.get_value_none2blank()), field_name))
            elif field_type == GacoiFormFieldType.Time:
                sb.append('<input type="text" class="form-control time-picker" '
                          'value="{0}" name="{1}">'
                          .format(Format.format_time(field.get_value_none2blank()), field_name))
            elif field_type == GacoiFormFieldType.DateTime:
                sb.append('<input type="text" class="form-control datetime-picker" '
                          'value="{0}" name="{1}">'
                          .format(Format.format_datetime(field.get_value_none2blank()), field_name))
            elif field_type == GacoiFormFieldType.Password:
                sb.append('<input type="password" class="form-control" value="{0}" name="{1}">'
                          .format(field.get_value_none2blank(), field_name))
            elif field_type == GacoiFormFieldType.Number:
                sb.append('<input type="number" class="form-control" value="{0}" name="{1}">'
                          .format(field.get_value_none2blank(), field_name))
            elif field_type == GacoiFormFieldType.Boolean:
                sb.append('<input type="checkbox" class="form-control ace" value="1" name="{0}" {1}/>'
                          '<span class="lbl"></span>'
                          .format(field_name, "checked" if field.get_value(False) else ""))
            elif field_type == GacoiFormFieldType.Checkbox:
                checked = ''
                checked_values = field.get_checked_values()
                value = self.apply_parameter(field.get_value_expression())
                if checked_values is not None and (value in checked_values or str(value) in checked_values):
                    checked = 'checked'
                sb.append('<input type="checkbox" class="ace" value="{2}" name="{0}" {1}/><span class="lbl"></span>'
                          .format(field_name, checked, value))
            elif field_type == GacoiFormFieldType.Radio:
                checked = ''
                checked_value = field.get_checked_value()
                value = self.apply_parameter(field.get_value_expression())
                if checked_value == value:
                    checked = 'checked'
                sb.append('<input type="radio" class="ace" value="{2}" name="{0}" {1}/><span class="lbl"></span>'
                          .format(field_name, checked, value))
            else:
                sb.append('<input type="text" class="form-control" value="{0}" name="{1}">'.format(field.get_value_none2blank(), field_name))

        return sb.__str__()

    def render_field_view_mode(self, field):
        """
        Render a field in readonly status
        @type field: GacoiField
        @param field:
        @return:
        """
        if isinstance(field, str):
            field = self.get_field(field)

        value = field.get_value_none2blank()
        dropdown = field.get_drop_down_list_values()
        if dropdown is not None and value in dropdown:
            value = dropdown[value]

        link = field.get_link()
        field_type = field.get_type()

        if link is not None:
            return '<a href="{0}">{1}</a>'.format(self.apply_parameter(link), html.escape(str(value)))
        elif field_type == GacoiFormFieldType.Boolean:
            sb = StringBuilder()
            sb.append('<input type="checkbox" disabled="" class="ace" {0}/><span class="lbl"></span>'
                      .format("checked" if field.get_value(False) else ""))
            return sb.__str__()
        elif field.is_multi_choices():
            sb = StringBuilder()
            GacoiForm._prepare_multi_choices_master(field)
            master = field.get_multi_choices_master_values()
            cols = field.get_multi_choices_cols()
            query = field.get_multi_choices_selected_query()

            if query is None:
                checked_values = field.get_multi_choices_selected_values()
            else:
                query = self.apply_parameter(query)
                checked_values = DbAgent.get_data_list(query)
                # checked_values = Util.get_list_from_record_set(get_db_instance().get_record_set(query))
                if field.is_bitwise():
                    if len(checked_values)>0:
                        multi_checked = []
                        for value in master:
                            if value & checked_values[0]:
                                multi_checked.append(value)
                        checked_values = multi_checked

            sb.append('<table>')
            count = 0
            sb.append('<tr style="line-height: 20px;">')
            for key, value in master.items():
                if checked_values is not None and (key in checked_values or str(key) in checked_values):
                    sb.append('<td style="border:0px;">')
                    # sb.append('<input type="checkbox" disabled="" class="ace" checked/> '
                    #          '<span class="lbl">{0}&nbsp;&nbsp;</span>'.format(value))
                    sb.append('<span style="white-space: pre;"><span style="font-weight: bold;color: gray;">◎</span>'
                              '{0}&nbsp;</span> '.format(value))
                    sb.append('</td>')
                    count += 1
                    if count % cols == 0:
                        sb.append('</tr><tr style="line-height: 20px;">')
            sb.append('<tr>')
            sb.append('<tr>')

            sb.append('</table>')

            return sb.__str__()
        else:
            field_type = field.get_type()
            if field_type == GacoiFormFieldType.Date:
                return "<span style='white-space: pre;'>{0}</span>".format(Format.format_date(value))
            elif field_type == GacoiFormFieldType.DateTime:
                return "<span style='white-space: pre;'>{0}</span>".format(Format.format_datetime(value))
            elif field_type == GacoiFormFieldType.Time:
                return "<span style='white-space: pre;'>{0}</span>".format(Format.format_time(value))
            elif field_type == GacoiFormFieldType.Number:
                if field.get_number_unit() and isinstance(value, numbers.Number):
                    value = round(value / field.get_number_unit())

                if field.get_decimal_point() is not None:
                    return "<span style='white-space: pre;float:right;'>{0}</span>".format(Format.format_number(value))
                else:
                    return html.escape(str(value))
            else:
                if field.is_nowrap():
                    return "<span style='white-space: pre'>{0}</span>".format(html.escape(str(value)))
                else:
                    return html.escape(str(value))

    def render_form_view_content(self):
        """
        Render form content as tabular form
        @return:
        """
        sb = StringBuilder()
        col = self.option_form_label_col
        # sb.append("<p></p>")
        if self.error_message is not None:
            sb.append('<div class="form-group">'
                      '<div class="col-sm-offset-{0} col-sm-8" style="color:red;">{1}</div></div>'.
                      format(col, self.error_message))

        if self.info_message is not None:
            sb.append('<div class="form-group">'
                      '<div class="col-sm-offset-{0} col-sm-8" style="color:blue;">{1}</div></div>'.
                      format(col, self.info_message))

        # Get data
        if self.form_data is not None:
            # Grid view
            if self.viewType == GacoiFormViewType.GridView:
                # Only when update
                if self.is_action(GacoiFormAction.UpdateStart):
                    # if self.get_paging_value() is not None:
                    #     start_index = (self.next_page_index - 1) * self.get_paging_value()
                    #     end_index = start_index + self.get_paging_value()
                    self.form_data = self.get_current_page_form_data()

                    for index, rec in enumerate(self.form_data):
                        self.set_values(rec)
                        for name, field in self.fields.items():
                            # Save key
                            if field.is_key():
                                sb.append(
                                    "<input type='hidden' name='key_{0}' value='{1}'>\n".format(field.name,
                                                                                                field.get_value()))
                    if self.is_action(GacoiFormAction.UpdateStart) and self.selectedRow is not None:
                        self.set_values(self.form_data[self.selectedRow])
            else:
                for rec in self.form_data:
                    self.set_values(rec)
                    break

        for name, field in self.fields.items():
            if (field.is_insert() and self.is_action(GacoiFormAction.InsertStart)) \
                    or (field.is_update() and self.is_action(GacoiFormAction.UpdateStart)):

                sb.append('<div class="form-group" >\n')
                sb.append('<label class="col-sm-{1} control-label no-padding-right" '
                          'style="white-space:nowrap;">{0}</label>\n'
                          .format(field.get_caption(), col))
                sb.append('                <div class="col-sm-8">\n')
                sb.append(self.render_field_edit_mode(field))
                sb.append('                </div>\n')
                sb.append('</div>\n')

        # Chi khi nao la form cua grid view
        sb.append('<div class="form-group"><div class="col-sm-offset-{0} col-sm-8">'.format(col))
        if self.viewType == GacoiFormViewType.GridView:

            sb.append('<button class="btn btn-sm btn-success" formnovalidate >\n')
            sb.append(self.lang("back"))
            sb.append('</button>\n')
            if self.is_action(GacoiFormAction.UpdateStart):
                sb.append('<button class="btn btn-sm btn-success" onclick="gacoiform_endUpdate(\'{0}\',{1})">\n'
                          .format(self.name, self.selectedRow))
                sb.append(self.lang("save"))
                sb.append('</button>\n')
            else:
                sb.append('<button class="btn btn-sm btn-success" onclick="gacoiform_endInsert(\'{0}\')">\n'.format(self.name))
                sb.append(self.lang("save"))
                sb.append('</button>\n')

        if self.viewType == GacoiFormViewType.FormView or (not self.is_action(GacoiFormAction.UpdateStart)
                                                           and not self.is_action(GacoiFormAction.InsertStart)):

            sb.append(self.render_user_button())

        sb.append("</div></div>")
        return str(sb)

    def render_search(self):
        """
        Render search row of Grid form
        @return:
        """
        if not self.is_search:
            return ''

        sb = StringBuilder()
        if self.is_action(GacoiFormAction.SearchDone):
            sb.append('<tr id="{0}_search_panel" style="background-color:lightblue" >\n'.format(self.name))
        else:
            sb.append('<tr id="{0}_search_panel" style="display:none;background-color:lightblue" >\n'.format(self.name))

        # Get data from search fields
        self.set_values(None)
        for name, field in self.fields.items():
            if field.is_view():
                if field.is_search():
                    sb.append('<td>\n')
                    sb.append(self.render_field_edit_mode(field, search_mode=True))
                    sb.append('</td>\n')
                    # Save key
                else:
                    sb.append('<td></td>\n')

        sb.append('<td nowrap>\n')
        sb.append('<div class="hidden-sm hidden-xs btn-group-minier">\n')
        sb.append('<button class="btn btn-sm btn-success" onclick="gacoiform_search(\'{0}\')">\n'
                  .format(self.name))
        sb.append('<i class="ace-icon fa fa-search "></i>\n')
        sb.append('</button>\n')
        sb.append('</div>\n')
        sb.append('</td>\n')

        if self.inlineUserButtons is not None:
            sb.append('<td></td>\n')

        sb.append('</tr>\n')
        return sb

    def render_grid_view_content(self):
        """
        Render form content as Grid form
        @return:
        """
        sb = StringBuilder()

        # Check right
        can_insert = False
        can_update = False
        can_delete = False
        for name, field in self.fields.items():
            if field.is_update():
                can_update = True
            if field.is_insert():
                can_insert = True
            if field.is_key() and self.option_deletable:
                can_delete = True
        sb.append('<div class="container-fluid">')
        if self.error_message is not None:
            sb.append("<div style='color:red;'>{0}</div>".format(self.error_message))
        if self.info_message is not None:
            sb.append("<div style='color:blue;'>{0}</div>".format(self.info_message))

        # Render insert button
        if can_insert:
            sb.append(
                '<button class="btn btn-sm btn-success" style="margin-bottom:15px;"'
                'formnovalidate onclick="gacoiform_startInsert(\'{0}\')">\n'.format(
                    self.name))
            sb.append(self.lang("insert new"))
            sb.append('</button>')
            sb.append('</br>')


        sb.append('<div class ="row">')
        sb.append('<div class ="col-sm-12">')
        # sb.append('<table id="dynamic-table" class="table table-striped table-bordered table-hover dataTable">\n')
        sb.append('<table class="table table-bordered">')
        sb.append('<thead><tr>\n')

        # Header field
        for name, field in self.fields.items():
            if field.is_view():
                order_by = field.get_order()
                order_icon = ''
                if order_by:
                    if order_by == 'asc':
                        sb.append('<th class="sorting_asc" onclick="gacoiform_startOrder(\'{0}\',\'{1}\')">\n'.format(
                            self.name, field.name
                        ))
                        order_icon = '<i class="fa fa-caret-down" style="color:#00BFFF;float: right;" aria-hidden="true"></i>'
                    elif order_by == 'desc':
                        sb.append('<th class="sorting_desc" onclick="gacoiform_startOrder(\'{0}\',\'{1}\')">\n'.format(
                            self.name, field.name
                        ))
                        order_icon = '<i class="fa fa-caret-up" style="color:#00BFFF;float: right;" aria-hidden="true"></i>'
                    else:
                        sb.append('<th class="sorting" onclick="gacoiform_startOrder(\'{0}\',\'{1}\')">\n'.format(
                            self.name, field.name
                        ))
                        order_icon = '<i class="fa fa-sort" style="float: right;" aria-hidden="true"></i>'
                else:
                    sb.append('<th>\n')

                header_link = field.get_header_link()
                if header_link is not None:
                    sb.append('<a style="cursor:pointer;" onclick="gacoiform_clickHeader(\'{0}\',\'{1}\');">{2}</a>\n'.
                              format(self.name, header_link, field.get_caption()))
                else:
                    sb.append('<div style="display: inline;">{0}'.format(field.get_caption()))
                    sb.append(order_icon)
                    sb.append('</div>')
                sb.append('</th>\n')
        # Action column
        if can_delete or can_update or self.is_search:
            sb.append('<th>\n')
            if self.is_search:
                sb.append('<div class="hidden-sm hidden-xs btn-group-minier">\n')
                sb.append('<button class="btn btn-sm btn-default" onclick="return gacoiform_toggleSearch(\'{0}\')">\n'
                          .format(self.name))
                sb.append('<i class="ace-icon fa fa-search bigger-120"></i>\n')
                sb.append('</button>\n')
                sb.append('</div>\n')

            sb.append('</th>\n')

        if self.inlineUserButtons is not None:
            sb.append('<th></th>\n')

        sb.append('</tr></thead>\n')
        sb.append(self.render_search())

        # Prepare for summary field
        summaries = dict()
        for name, field in self.fields.items():
            if field.is_summary():
                summaries[name] = 0
        # Data
        if self.form_data is not None:
            r = 0
            data_count = self.form_data.count()
            if self.get_paging_value() is None:
                number_paging = 1
            else:
                if data_count%self.get_paging_value() == 0:
                    number_paging = int(data_count/self.get_paging_value())
                else:
                    number_paging = math.floor(data_count/self.get_paging_value()) + 1

            self.form_data = self.get_current_page_form_data()
            for index, rec in enumerate(self.form_data):

                sb.append('<tr>\n')
                self.set_values(rec)
                for name, field in self.fields.items():
                    # Calculate summary
                    if field.is_summary():
                        summaries[name] += field.get_value()

                    field_type = field.get_type()
                    if field.is_view():
                        sb.append('<td{0}>\n'.format(field.get_column_width_css()))
                        if self.is_action(GacoiFormAction.UpdateStart) and self.selectedRow == r and field.is_update():
                            sb.append(self.render_field_edit_mode(field))
                        elif field_type == GacoiFormFieldType.Checkbox or field_type == GacoiFormFieldType.Radio:
                            sb.append(self.render_field_edit_mode(field))
                        else:
                            sb.append(self.render_field_view_mode(field))
                        sb.append('</td>\n')
                        # Save key
                    if field.is_key():
                        sb.append(
                            "<input type='hidden' name='key_{0}' value='{1}'>\n".format(field.name, field.get_value()))

                if can_delete or can_update or self.is_search:
                    sb.append('<td nowrap>\n')
                if can_delete or can_update:
                    if self.is_action(GacoiFormAction.UpdateStart) and self.selectedRow == r:
                        sb.append('<div class="hidden-sm hidden-xs  btn-group-minier">\n')
                        sb.append('<button class="btn btn-sm btn-success" onclick="gacoiform_endUpdate(\'{0}\',{1})">\n'
                                  .format(self.name, r))
                        sb.append('<i class="ace-icon fa fa-check"></i>\n')
                        sb.append('</button>\n')
                        sb.append('</div>\n')

                    else:
                        sb.append('<div class="hidden-sm hidden-xs btn-group-minier">\n')
                        if can_update:
                            sb.append('<button class="btn btn-sm  btn-info" formnovalidate '
                                      'onclick="gacoiform_startUpdate(\'{0}\',{1})">\n'.format(self.name, r))
                            sb.append('<i class="ace-icon fa fa-pencil"></i>\n')
                            sb.append('</button>\n')
                        if can_delete:
                            sb.append('<button class="btn btn-sm  btn-danger" formnovalidate '
                                      'onclick="gacoiform_deleteConfirm(event,\'{0}\',{1})">\n'.format(self.name, r))
                            sb.append('<i class="ace-icon fa fa-trash-o"></i>\n')
                            sb.append('</button>\n')
                        sb.append('</div>\n')
                if can_delete or can_update or self.is_search:
                    sb.append('</td>\n')

                if self.inlineUserButtons is not None:
                    sb.append('<td nowrap>\n')
                    sb.append(self.render_inline_user_button(r))
                    sb.append('</td>\n')

                sb.append('</tr>\n')

                r = r + 1

            # Summary row
            if len(summaries) > 0:
                sb.append('<tr style="background-color:cyan;">\n')
                for name, field in self.fields.items():
                    if field.is_view():
                        if field.is_summary():
                            sb.append("<td><span style='white-space: pre;float:right;'>{0}</span></td>\n".
                                      format(Format.format_number(summaries[name], field.get_decimal_point(0))))
                        else:
                            sb.append('<td></td>\n')
                    if can_delete or can_update or self.is_search:
                        sb.append('<td></td>\n')
                    if self.inlineUserButtons is not None:
                        sb.append('<td></td>\n')

                sb.append('</tr>\n')
        sb.append('<tr>')
        sb.append('</table>')
        sb.append('<tr>')
        if self.form_data is not None:
            sb.append(self.render_page_tab(number_paging))

        sb.append('</div></div><br>\n')

        # Render insert button
        # if can_insert:
        #     sb.append(
        #         '<button class="btn btn-sm btn-success" '
        #         'formnovalidate onclick="gacoiform_startInsert(\'{0}\')">\n'.format(
        #             self.name))
        #     sb.append(self.lang("insert new"))
        #     sb.append('</button>&nbsp;')

        sb.append(self.render_user_button())
        sb.append('</div></br>')
        return str(sb)

    def render_user_button(self):
        """
        Render user button below form
        @return:
        """
        sb = StringBuilder()
        if self.userButtons:
            for button in self.userButtons:
                formnovalidate = 'formnovalidate'
                if button.validate:
                    formnovalidate = ''
                sb.append('<button class="btn btn-sm btn-success" {0} onclick="return {1}">\n'
                          .format(formnovalidate, button.action.replace('"', "'")))
                sb.append(button.display)
                sb.append('</button>&nbsp;\n')
        return str(sb)

    def render_inline_user_button(self, r):
        """
        Render user button at each row
        @param r:
        @return:
        """
        sb = StringBuilder()
        sb.append('<div class="hidden-sm hidden-xs btn-group-minier">\n')
        if self.inlineUserButtons:
            for button in self.inlineUserButtons:
                formnovalidate = 'formnovalidate'
                if button.validate:
                    formnovalidate = ''
                if button.action:
                    action = self.apply_parameter(button.action)
                    sb.append('<button class="btn btn-sm btn-success" '
                              'onclick="return {0}" {1}>{2}\n'.
                              format(action, formnovalidate, button.display))
                else:
                    sb.append('<button class="btn btn-sm btn-success" '
                              'onclick="gacoiform_clickUserInlineButton(\'{0}\',{1},\'{2}\');" {3}>{4}\n'.
                              format(self.name, r, button.return_value, formnovalidate, button.display))
                sb.append('</button>\n')
        sb.append('</div>\n')
        return str(sb)

    def render_page_tab(self, number_paging):
        if number_paging == 1:
            return ""
        sb = StringBuilder()
        if self.next_page_index%5 != 0:
            min_current_tab_page_index = self.next_page_index-(self.next_page_index%5)+1
        else:
            min_current_tab_page_index = self.next_page_index - self.page_tab_number + 1
        max_current_tab_page_index = min_current_tab_page_index + self.page_tab_number
        if max_current_tab_page_index > number_paging:
            max_current_tab_page_index = number_paging + 1
        number_paging_numbers = list(range(min_current_tab_page_index, max_current_tab_page_index))

        sb.append('<ul class="pagination">')
        if self.next_page_index > self.page_tab_number:
            sb.append(
            '<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>First</a></li>'
                .format(self.name, 1))
        if self.next_page_index == 1:
            sb.append('<li class="page-item"><a class="page-link" onclick="">Prev</a></li>')
        else:
            sb.append(
                '<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>Prev</a></li>'
                    .format(self.name, self.next_page_index - 1))
        if self.next_page_index > self.page_tab_number:
            sb.append(
                '<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>...</a></li>'
                    .format(self.name, min_current_tab_page_index-1))

        for i in number_paging_numbers:
            if i == self.next_page_index:
                active = "active"
            else:
                active = ""
            sb.append(
                '<li class="page-item {0}"><a class="page-link" onclick=gacoiform_paging_index("{1}",{2})>{2}</a></li>'
                .format(active, self.name, i))

        if max_current_tab_page_index <= number_paging:
            sb.append('<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>...</a></li>'
                      .format(self.name, max_current_tab_page_index))

        if self.next_page_index < number_paging:
            sb.append(
                '<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>Next</a></li>'
                .format(self.name, self.next_page_index + 1))
        else:
            sb.append(
                '<li class="page-item"><a class="page-link" onclick="">Next</a></li>')
        if max_current_tab_page_index <= number_paging:
            sb.append('<li class="page-item"><a class="page-link" onclick=gacoiform_paging_index("{0}",{1})>Last</a></li>'
                      .format(self.name, number_paging))

        sb.append('</ul>')
        return sb.__str__()

    @staticmethod
    def render_common_script():
        """
        Render common java script that used in GacoiForm
        @return:
        """
        sb = StringBuilder()
        sb.append('<script type="text/javascript">\n')

        # Insert start function
        sb.append('    function gacoiform_startInsert(formname){\n')
        sb.append('        document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.InsertStart.value))
        sb.append('    }\n')

        sb.append('function gacoiform_startOrder(formname,field_name){  ')
        sb.append('	var current_field_name = document.forms[formname][formname +  "_order_field"].value;')
        sb.append('	if (current_field_name != field_name) {')
        sb.append('		order_type = "asc";')
        sb.append('	}else{')
        sb.append('		order_type = document.forms[formname][formname +  "_order_type"].value;')
        sb.append('		if (order_type == "asc") {')
        sb.append('			order_type = "desc";')
        sb.append('		} else { ')
        sb.append('			order_type = "asc";')
        sb.append('		}')
        sb.append('	}')
        sb.append('	document.forms[formname][formname +  "_order_field"].value = field_name;')
        sb.append('	document.forms[formname][formname +  "_order_type"].value = order_type;')
        sb.append('	document.all[formname].submit();')
        sb.append('}')

        # Search function
        sb.append('    function gacoiform_search(formname){\n')
        sb.append('        document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.SearchDone.value))
        sb.append('    }\n')

        # Search function
        sb.append('    function gacoiform_paging_index(formname,page_index){\n')
        sb.append('        document.forms[formname][formname + "_next_page_index"].value = page_index;')
        sb.append('	       document.all[formname].submit();')
        sb.append('    }\n')


        # Search function
        sb.append('    function gacoiform_toggleSearch(formname){ \n')
        sb.append('        try { if (document.all[formname +  "_search_panel"].style.display == "none"){\n')
        sb.append('        document.all[formname + "_search_panel"].style.display = "";\n')
        sb.append('        } else {\n')
        sb.append('        document.all[formname + "_search_panel"].style.display = "none";\n')
        sb.append('        } } catch (e) { alert(e)} \n')
        sb.append('        return false;\n')
        sb.append('    }\n')

        # Insert done function
        sb.append('    function gacoiform_endInsert(formname){\n')
        sb.append('        if(!$("#" + formname + "-id").valid()) {\n')
        sb.append('        }else{\n')
        sb.append('             document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.InsertDone.value))
        sb.append('        }\n')
        sb.append('     return false;   \n')
        sb.append('    }\n')

        # Update start function
        sb.append('    function gacoiform_startUpdate(formname,row){\n')
        sb.append('        document.forms[formname][formname + "_selected_row"].value = row;\n')
        sb.append('        document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.UpdateStart.value))
        sb.append('    }\n')

        # User inline button
        sb.append('    function gacoiform_clickUserInlineButton(formname, row, value){\n')
        sb.append('        document.forms[formname][formname + "_selected_row"].value = row;\n')
        sb.append('        document.forms[formname][formname + "_inline_user_button_return_value"].value = value;\n')
        sb.append('    }\n')

        # User inline button
        sb.append('    function gacoiform_clickHeader(formname, value){\n')
        sb.append('        document.forms[formname][formname + "_header_link_return_value"].value = value;\n')
        sb.append('        document.forms[formname].submit();\n')
        sb.append('    }\n')

        # Update end function
        sb.append('    function gacoiform_endUpdate(formname,row){\n')
        sb.append('        document.forms[formname][formname + "_selected_row"].value = row;\n')
        sb.append('        document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.UpdateDone.value))
        sb.append('    }\n')

        # Delete confirm function
        sb.append('    function gacoiform_deleteConfirm(e,formname,row){\n')

        sb.append('bootbox.confirm("{0}",\n'.format(GacoiForm.lang("Are you sure to delete?")))
        sb.append('	function(result){\n')
        sb.append('		if (result){\n')
        sb.append('			document.forms[formname][formname + "_selected_row"].value = row;\n')
        sb.append('			document.forms[formname][formname + "_action"].value = {0};\n'.format(
            GacoiFormAction.DeleteDone.value))
        sb.append('			document.forms[formname].submit();\n')
        sb.append('		}\n')
        sb.append('	});\n')
        sb.append('\n')
        sb.append('e.preventDefault();\n')
        sb.append('return false;\n')

        # sb.append('        if (!confirm("{0}"))\n'.format(GacoiForm.lang("Are you sure to delete?")))
        # sb.append('        {\n')
        # sb.append('            e.preventDefault();\n')
        # sb.append('            return false;\n')
        # sb.append('        }\n')
        # sb.append('        document.forms[formname][formname + "_selected_row"].value = row;\n')
        # sb.append('        document.forms[formname][formname + "_action"].value = {0};\n'.format(
        #     GacoiFormAction.DeleteDone.value))
        # sb.append('        return true;\n')

        sb.append('    }\n')

        # sb.append("jQuery(function($) {\n")
        #
        # # sb.append("$.fn.datepicker.dates['{0}']['titleFormat']='{1}';\n".format(
        # #     LocalizeFormat.Language.value, LocalizeFormat.DatePickerCalendarTitleFormat.value))
        # sb.append("$.fn.datepicker.dates['{0}']['yearViewFormat']='{1}';\n".format(
        #     LocalizeFormat.Language.value, LocalizeFormat.DatePickerCalendarYearViewFormat.value))
        #
        # sb.append("	$('.date-picker').datepicker({\n")
        # sb.append("		autoclose: true,\n")
        # sb.append("		todayHighlight: true,\n")
        # sb.append("		language: '{0}',\n".format(LocalizeFormat.Language.value))
        # sb.append("		format: '{0}',\n".format(LocalizeFormat.DateFormat.value))
        # sb.append("	})\n")
        # sb.append("	.next().on(ace.click_event, function(){\n")
        # sb.append("		$(this).prev().focus();\n")
        # sb.append("	});\n")
        #
        # sb.append("	//or change it into a date range picker\n")
        # sb.append("	//$('.input-daterange').datepicker({autoclose:true});\n")
        #
        # sb.append("	$('.time-picker').timepicker({\n")
        # sb.append("		minuteStep: {0},\n".format(LocalizeFormat.MinuteStep.value))
        # sb.append("		showSeconds: {0},\n".format("true" if LocalizeFormat.ShowSecond.value else "false"))
        # sb.append("		showMeridian: {0},\n".format("true" if LocalizeFormat.ShowMeridian.value else "false"))
        # sb.append("		disableFocus: false,\n")
        # sb.append("		meridianAM: '{0}',\n".format(LocalizeFormat.MeridianAM.value))
        # sb.append("		meridianPM: '{0}',\n".format(LocalizeFormat.MeridianPM.value))
        # sb.append("		icons: {\n")
        # sb.append("			up: 'fa fa-chevron-up',\n")
        # sb.append("			down: 'fa fa-chevron-down'\n")
        # sb.append("		}\n")
        # sb.append("	}).on('focus', function() {\n")
        # sb.append("		$(this).timepicker('showWidget');\n")
        # sb.append("	}).next().on(ace.click_event, function(){\n")
        # sb.append("		$(this).prev().focus();\n")
        # sb.append("	});\n")
        # sb.append("});\n")
        #
        sb.append('</script>\n')

        return sb


    # Render spinner script
    @staticmethod
    def render_spinner_script():
        sb = StringBuilder()
        sb.append('<script type="text/javascript">\n')
        sb.append('function start_spinner() {\n')
        sb.append('	 var opts = {\n')
        sb.append('		lines: 11 // The number of lines to draw\n')
        sb.append('		, length: 5 // The length of each line\n')
        sb.append('		, width: 5 // The line thickness\n')
        sb.append('		, radius: 11 // The radius of the inner circle\n')
        sb.append('		, scale: 2 // Scales overall size of the spinner\n')
        sb.append('		, corners: 0.2 // Corner roundness (0..1)\n')
        sb.append('		, color: "#000" \n')

        sb.append('		, opacity: 0.15 // Opacity of the lines\n')
        sb.append('		, rotate: 0 // The rotation offset\n')
        sb.append('		, direction: 1 // 1: clockwise, -1: counterclockwise\n')
        sb.append('		, speed: 1 // Rounds per second\n')
        sb.append('		, trail: 56 // Afterglow percentage\n')
        sb.append('		, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS\n')
        sb.append('		, zIndex: 2e9 // The z-index (defaults to 2000000000)\n')
        sb.append('		, className: "spinner" // The CSS class to assign to the spinner\n')
        sb.append('		, top: "50%" // Top position relative to parent\n')
        sb.append('		, left: "50%" // Left position relative to parent\n')
        sb.append('		, shadow: false // Whether to render a shadow')
        sb.append('		, hwaccel: false // Whether to use hardware acceleration\n')
        sb.append('		, position: "absolute" // Element positioning\n')
        sb.append('	  }\n')
        sb.append('	  $("#page-content").append(\'<div id="spinner-preview"> </div>\');\n')
        sb.append('	  $("#spinner-preview").css({\n')
        sb.append('		"position": "absolute",\n')
        sb.append('		"left": "50%",\n')
        sb.append('		"margin-top": "-50px",\n')
        sb.append('		"margin-left": "-50px",\n')
        sb.append('		"width": "100px",\n')
        sb.append('		"height": "100px" });\n')
        sb.append('		var top = String(screen.height/2) + "px";\n')
        sb.append('	  $("#spinner-preview").css({"top":top});\n')
        sb.append('	  var target = document.getElementById("spinner-preview")\n')
        sb.append('	  var spinner = new Spinner(opts).spin(target);\n')
        sb.append('	}\n')
        sb.append('	function stop_spinner()\n')
        sb.append('	{\n')
        sb.append('		var target = document.getElementById("spinner - preview")\n')
        sb.append('		$("#spinner-preview").empty();\n')
        sb.append('	}\n')
        sb.append('</script>\n')


        return sb

    # Render java script
    def render_script(self):
        """
        Render java script for each form. This script do the validate action
        @return:
        """
        sb = StringBuilder()
        sb.append('<script type="text/javascript">\n')

        # JQuery for validation
        sb.append("    jQuery(function($) {\n")
        sb.append("        try{\n")

        sb.append("            $('#{0}-id').validate({{\n".format(self.name))
        sb.append("                errorElement: 'div',\n")
        sb.append("                errorClass: 'help-block',\n")
        sb.append("                focusInvalid: false,\n")
        sb.append("                ignore: '',\n")
        sb.append("                rules: {\n")

        for name, field in self.fields.items():
            if field.is_required():
                sb.append("                    {0}: {{\n".format(field.name))
                sb.append("                        required: true,\n")
                sb.append("                    },\n")

        sb.append("                },\n")
        sb.append("                messages: {\n")

        for name, field in self.fields.items():
            if field.is_required():
                sb.append("                    {0}: {{\n".format(field.name))
                sb.append("                        required: '{0}',\n".format(GacoiForm.lang("This is required item.")))
                sb.append("                    },\n")

        sb.append("                },\n")
        sb.append("                highlight: function (e) {\n")
        sb.append("                    $(e).closest('.form-group').removeClass('has-info').addClass('has-error');\n")
        sb.append("                },\n")
        sb.append("                success: function (e) {\n")
        sb.append("                    $(e).closest('.form-group').removeClass('has-error');\n")
        sb.append("                    $(e).remove();\n")
        sb.append("                },\n")

        sb.append("                errorPlacement: function (error, element) {\n")
        sb.append("                    if(element.is('input[type=checkbox]') || element.is('input[type=radio]')) {\n")
        sb.append("                        var controls = element.closest('div[class*=\"col-\"]');\n")
        sb.append("                        if(controls.find(':checkbox,:radio').length > 1) controls.append(error);\n")
        sb.append("                        else error.insertAfter(element.nextAll('.lbl:eq(0)').eq(0));\n")
        sb.append("                    }\n")
        sb.append("                    else if(element.is('.select2')) {\n")
        sb.append(
            "                        error.insertAfter(element.siblings('[class*=\"select2-container\"]:eq(0)'));\n")
        sb.append("                    }\n")
        sb.append("                    else if(element.is('.chosen-select')) {\n")
        sb.append(
            "                        error.insertAfter(element.siblings('[class*=\"chosen-container\"]:eq(0)'));\n")
        sb.append("                    }\n")
        sb.append("                    else if(element.parent().prop('tagName')=='TD') {\n")
        sb.append("                        error.insertAfter(element);\n")
        sb.append("                    }\n")
        sb.append("                    else { error.insertAfter(element);}\n")
        sb.append("                },\n")

        sb.append("                submitHandler: function (form) {\n")
        sb.append("                    form.submit();\n")
        sb.append("                },\n")

        sb.append("                invalidHandler: function (form) {\n")
        sb.append("                }\n")

        sb.append("            });\n")
        sb.append("        }catch (e){\n")
        sb.append("            alert(e);\n")
        sb.append("            \n")
        sb.append("        }\n")
        sb.append("    })\n")
        sb.append('</script>\n')
        sb.append(self.render_relate_fields_script())
        return sb.__str__()

    def render_relate_fields_script(self):
        sb = StringBuilder()
        if self.relate_fields is None:
            return ""
        for relate in self.relate_fields:
            parent_field = relate['father_field']
            child_field = relate['children_field']
            parent_child_dict = relate['parent_child_dict']
            parent_field = self.get_field(parent_field)
            if parent_field.is_search():
                search_parent_field = 'search_{0}'.format(parent_field)
                search_childrent_field = 'search_{0}'.format(child_field)
                sb.append('<script type="text/javascript">\n')
                sb.append('var {0}_{1} = {2}'.format(parent_field,child_field,parent_child_dict))
                sb.append('function handleRelate(childrenName, parentName)')
                sb.append('{var dict = window[parentName + "_" + childrenName];')
                sb.append('var x = document.getElementsByName("mySelect").value; ')
                sb.append('document.getElementById("demo").innerHTML = "You selected: " + String(children_dict[1]);')
                sb.append(' }')
                sb.append('</script>')



        return sb.__str__()

    def get_key_value(self, field_name, index=None):
        """
        Get value of key field
        @param field_name:
        @param index:
        @return:
        """
        if index is None:
            index = self.selectedRow
        if index is None:
            return None
        if field_name in self.keyValues:
            return self.keyValues[field_name][index] if len(self.keyValues[field_name]) > index else None

    def get_field_value(self, field_name, indicator=''):
        """
        Get value of field
        @param field_name:
        @param indicator:
        @return:
        """
        field = self.get_field(field_name)
        if field is None:
            return ''
        if indicator == '@':
            pass
        if indicator == '#':
            pass
        if indicator == '!':
            pass
        else:
            return str(field.get_value())

    def apply_parameter(self, string):
        """
        Replace [field] to field's value
        @param string:
        @return:
        """
        return re.sub(r"\[([\#\@\!]?)([a-zA-Z0-9_-]*)\]",
                      lambda x: self.get_field_value(x.group(2), x.group(1)), string)

    # Get data from request
    def init(self, request):
        """
        Init form. Get submitted data from request apply to form.
        Here will check the action of form
        @param request:
        @return:
        """
        if request.method == 'POST':
            params = request.POST
        else:
            params = request.GET

        # Get value of fields
        for name, field in self.fields.items():
            # Value
            field.set_value(params.get(name, None))

            # Get Keys value
            if field.is_key():
                keys = (params.getlist("key_{0}".format(field.name), None))
                if keys is not None:
                    if field.name not in self.keyValues:
                        self.keyValues[field.name] = []
                    for key in keys:
                        self.keyValues[field.name].append(key)
            field_type = field.get_type()
            # Checkbox value
            if field_type == GacoiFormFieldType.Checkbox:
                values = params.getlist(name, None)
                if values is not None and field.get_checked_values() is None:
                    field.set_checked_values(values)
            elif field_type == GacoiFormFieldType.Radio:
                field.set_checked_value(params.get(name, None))
            elif field_type == GacoiFormFieldType.DateTime:
                field.set_value(Format.to_datetime(params.get(name, None)))
            elif field_type == GacoiFormFieldType.Date:
                field.set_value(Format.to_date(params.get(name, None)))
            elif field_type == GacoiFormFieldType.Time:
                field.set_value(Format.to_time(params.get(name, None)))
            elif field.is_multi_choices():
                values = params.getlist(name, None)
                if field_type == GacoiFormFieldType.Number:
                    for i in range(len(values)):
                        values[i] = Util.to_int(values[i])
                field.set_multi_choices_selected_values(values)

            if field.is_search():
                # Search value
                search_field_name = "search_{0}".format(name)
                search_key = params.get(search_field_name, None)
                if search_key is None:
                    if field.is_drop_down_list_all_value() is not None and not field.is_drop_down_list_all_value():
                        search_keep_field_name = "search_{0}_keep".format(name)
                        search_key = params.get(search_keep_field_name,None)
                        if search_key is None:
                            search_key = field.get_search_value()

                field.set_search_value(search_key)
                if field_type == GacoiFormFieldType.DateTime:
                    field.set_search_value(Format.to_datetime(params.get(search_field_name, None)))
                elif field_type == GacoiFormFieldType.Date:
                    field.set_search_value(Format.to_date(params.get(search_field_name, None)))
                elif field_type == GacoiFormFieldType.Time:
                    field.set_search_value(Format.to_time(params.get(search_field_name, None)))
                elif field.is_multi_choices():
                    values = params.getlist(search_field_name, None)
                    if field_type == GacoiFormFieldType.Number:
                        for i in range(len(values)):
                            values[i] = Util.to_int(values[i])
                    field.set_search_value(values)

        # Get action
        self.action = params.get(self.name + "_action", None)
        self.order_type = params.get(self.name + "_order_type", None)
        self.next_page_index = int(params.get(self.name + "_next_page_index", 1))

        self.order_field = params.get(self.name + "_order_field", None)
        if self.order_field == '':
            self.order_field = None
        if self.order_field:
            self.get_field(self.order_field).set_order(self.order_type)

        self.inline_user_button_return_value = params.get(self.name + "_inline_user_button_return_value", None)
        self.header_link_return_value = params.get(self.name + "_header_link_return_value", None)
        self.current_menu_state = params.get("current_menu_state",1)

        if self.inline_user_button_return_value == '':
            self.inline_user_button_return_value = None

        if self.header_link_return_value == '':
            self.header_link_return_value = None

        if self.action is not None and self.action.isdigit():
            self.action = GacoiFormAction(int(self.action))

        # Selected row
        self.selectedRow = params.get(self.name + "_selected_row", None)
        if self.selectedRow == '':
            self.selectedRow = None
        if self.selectedRow is not None and self.selectedRow.isdigit():
            self.selectedRow = int(self.selectedRow)

    def set_form_data(self, data, model=None):
        """
        Set form data
        @param data: list of dict or Django query set
        @param model:
        @return:
        """

        self.form_data = data
        if model is not None:
            for name, field in self.fields.items():
                meta_field = None
                try:
                    meta_field = model._meta.get_field(name)
                except:
                    pass
                if meta_field:
                    field.set_caption(meta_field.verbose_name.title())

    def get_current_page_form_data(self):
        model = self.form_data_model
        data = self.form_data
        if self.get_paging_value() is None:
            self.set_paging_value(data.count())
        start_index = (self.next_page_index - 1) * self.get_paging_value()
        to_index = start_index + self.get_paging_value()

        if self.form_data_model != None:
            ids = list(data[start_index:to_index].values('id').values_list(flat=True))
            # ids = data.values_list('id',flat=True)[start_index:self.get_paging_value()]
            data = model.objects.filter(id__in=ids)
        else:
                ids = [i.id for i in data[start_index:to_index]]
                data = data.filter(id__in=ids)

        return data

    def set_form_model(self,model):
        self.form_data_model = model

    def set_search_default_value(self):
        for name, field in self.fields.items():
            if field.is_drop_down_list_all_value() is not None and not field.is_drop_down_list_all_value() :
                values = field.get_drop_down_list_values()
                my_list = [elem for elem in values.keys()]
                if len(my_list) > 0:
                    field.set_search_value(str(my_list[0]))
                    print("1")

    def set_view_type(self, view_type):
        """
        Form type. Tabular or grid
        @type view_type: GacoiFormViewType
        @param view_type:
        @return:
        """
        self.viewType = view_type

    def get_field(self, name, auto_create=True):
        """
        Get form's field
        @param name:
        @param auto_create:
        @return:
        @rtype: GacoiField
        """
        if name not in self.fields:
            if auto_create:
                self.fields[name] = GacoiField(name)
            else:
                return None
        return self.fields[name]

    def set(self, field_names, attribute, value):
        """
        Set attribute for list of field
        @param field_names: string, list of field separated by commas
        @param attribute:
        @param value:
        @return:
        """
        fields = field_names.split(",")
        for field in fields:
            field = field.strip()
            self.get_field(field).set(attribute, value)

    def set_column_width(self, obj):
        for key, value in obj.items():
            self.get_field(key).set_column_width(value)

    def set_caption(self, obj):
        """
        Set fields's caption
        @param obj:
        @return:
        """
        if isinstance(obj, list):
            if len(obj) < 2:
                return
            fields = obj[0].split(",")
            values = obj[1].split(",")
            for i in range(len(fields)):
                if i < len(values):
                    self.get_field(fields[i].strip()).set_caption(values[i].strip())

        elif isinstance(obj, dict):
            for key, value in obj.items():
                self.get_field(key).set_caption(value)
        else:
            for name, field in self.fields.items():
                meta_field = None
                try:
                    meta_field = obj._meta.get_field(name)
                except:
                    pass
                if meta_field:
                    field.set_caption(meta_field.verbose_name.title())

    def set_type(self, field_names, value):
        """
        Set fields's type
        @param field_names:
        @param value:
        @return:
        """
        self.set(field_names, "type", value)

    def set_required(self, field_names, value=True):
        """
        Set fields's required or not
        @param field_names:
        @param value:
        @return:
        """
        self.set(field_names, "required", value)

    def set_update(self, field_names, value=True):
        """
        Set fields's updatable or not
        @param field_names:
        @param value:
        @return:
        """
        self.set(field_names, "update", value)

    def set_view(self, field_names, value=True):
        """
        Set fields's viewable or not
        @param field_names:
        @param value:
        @return:
        """
        self.set(field_names, "view", value)

    def set_search(self, field_names, value=True):
        """
        Set fields's searchable or not
        @param field_names:
        @param value:
        @return:
        """
        self.is_search = True
        self.set(field_names, "search", value)

    def set_order(self, field_names, value=True):
        """
        Set fields's sortable or not
        @param field_names:
        @param value:
        @return:
        """
        self.set(field_names, "order", value)

    def set_insert(self, field_names, value=True):

        self.set(field_names, "insert", value)

    def set_key(self, field_names, value=True):
        self.set(field_names, "key", value)

    def set_default(self, field_names, value=True):
        self.set(field_names, "default", value)

    def set_summary(self, field_names, value=True):
        self.set(field_names, "summary", value)

    def set_nowrap(self, field_names, value=True):
        self.set(field_names, "nowrap", value)

    def is_action(self, action):
        return self.action == action

    def set_action(self, action):
        self.action = action

    def add_user_button(self, button):
        """
        Add user button
        @type button:UserButton
        @param button:
        @return:
        """
        if not self.userButtons:
            self.userButtons = []
        self.userButtons.append(button)

    def add_inline_user_button(self, button):
        """
        Add inline user button
        @type button: InlineUserButton
        @param button:
        @return:
        """
        if not self.inlineUserButtons:
            self.inlineUserButtons = []
        self.inlineUserButtons.append(button)

    @staticmethod
    def save_upload_file(request, file_field, path):
        """
        Save upploaded file
        @param request:
        @param file_field:
        @param path:
        @return:
        """
        file = request.FILES.get(file_field, None)
        if file:
            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return file.name
        return None

    def set_option_update_in_form_view(self, value=True):
        """
        Force that open tabular form when update data in grid form
        @param value:
        @return:
        """
        self.option_update_in_form_view = value

    def get_option_update_in_form_view(self):
        """
        Force that open tabular form when update data in grid form
        @return:
        """
        return self.option_update_in_form_view

    def set_option_form_label_col(self, value=2):
        """
        Width of label in tabular form. It show as percentage. Default is 2 mean 20 %
        @param value:
        @return:
        """
        self.option_form_label_col = value

    def get_option_form_label_col(self):
        """
        Width of label in tabular form. It show as percentage. Default is 2 mean 20 %
        @return:
        """
        return self.option_form_label_col

    def set_option_deletable(self, value=True):
        """
        Show delete button or not
        @param value:
        @return:
        """
        self.option_deletable = value

    def get_option_deletable(self):
        """
        Show delete button or not
        @return:
        """
        return self.option_deletable

    def get_inline_user_button_return_value(self):
        """
        Return value after inline button clicked.
        @return:
        """
        return self.inline_user_button_return_value

    def get_header_link_return_value(self):
        """
        Return value after header link clicked
        @return:
        """
        return self.header_link_return_value

    def apply_search_condition(self, query_set, field_names):
        """
        Apply search input to query set
        @param query_set:
        @param field_names:
        @return:
        """
        fields = field_names.split(",")
        for field_name in fields:
            field_name = field_name.strip()
            field = self.get_field(field_name)
            search = field.get_search_value()
            if search is not None and search != '':
                field_type = field.get_type()
                dropdown = field.get_drop_down_list_values()
                if dropdown is not None or field_type == GacoiFormFieldType.Number \
                        or field_type == GacoiFormFieldType.DateTime \
                        or field_type == GacoiFormFieldType.Date:
                    query_set = query_set.filter(**{"{0}".format(field_name): search})
                elif field_type == GacoiFormFieldType.Boolean:
                    query_set = query_set.filter(**{"{0}".format(field_name): True})
                else:
                    query_set = query_set.filter(**{"{0}__contains".format(field_name): search})
        return query_set





class Util:
    @staticmethod
    def to_int(value, default=0):
        """
        Convert string to int
        @param value:
        @param default:
        @return:
        """
        if isinstance(value, int):
            return value
        if value is None:
            return default
        if value.isdigit():
            return int(value)
        return default

    @staticmethod
    def enum_to_dict(enum_class, first_blank=False):
        """
        Convert enum to a dict.
        For python <3.0, you need to specify an __order__ attribute:
         __order__ = 'vanilla chocolate cookies mint'
        @type enum_class: Enum
        @param enum_class:
        @param first_blank
        @return:
        """
        ret = OrderedDict()
        if first_blank:
            ret[''] = ''

        for item in enum_class:
            if isinstance(item.value, tuple) or isinstance(item.value, list):
                ret[item.value[0]] = item.value[1]
            else:
                ret[item.value] = str(item.value)
        return ret

    @staticmethod
    def model_list_to_list(list_object, value_field):
        """
        Convert Django QuerySet to list of dict
        @param list_object:
        @param value_field:
        @return:
        """
        ret = list()
        for o in list_object:
            if isinstance(o, dict):
                ret.append(o[value_field])
            else:
                ret.append(o.__dict__[value_field])
        return ret

    @staticmethod
    def get_list_from_record_set(items):
        list = []
        for item in items:
            list.append(item[0])
        return list

    @staticmethod
    def model_list_to_dict(model_list, key_field, value_field, first_blank=False):
        """
        Convert Django QuerySet to dict
        @param model_list:
        @param key_field:
        @param value_field:
        @param first_blank:
        @return:
        """
        ret = OrderedDict()
        if first_blank:
            ret[''] = ''

        for item in model_list:
            ret[item.__dict__[key_field]] = item.__dict__[value_field]

        return ret

    @staticmethod
    def is_date(string):
        """
        Check if string is date
        @param string:
        @return:
        """
        from dateutil.parser import parse
        try:
            parse(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def to_date(string):
        """
        Convert to date
        @param string:
        @return:
        """
        from dateutil.parser import parse
        try:
            return parse(string)
        except ValueError:
            return None

    @staticmethod
    def get_data_map(objects, id_field, value_field):
        """
        Like as model_list_to_dict method
        """
        ret = dict()
        for o in objects:
            ret[o.__dict__[id_field]] = o.__dict__[value_field]
        return ret

    @staticmethod
    def create_wizard_menu(wizard_step, wizard_items):
        """
        Create html of wizard menu
        @param wizard_step: Wizard step
        @type wizard_step: int
        @type wizard_items: list
        @param wizard_items: Wizard items
        @rtype: str
        @return:
        """
        sb = StringBuilder()
        sb.append('<div class="widget-body">\n')
        sb.append('    <div class="widget-main">\n')
        sb.append('        <div id="fuelux-wizard-container">\n')
        sb.append('            <div>\n')
        sb.append('                <ul class="steps">\n')

        for i in range(len(wizard_items)):
            step = i + 1
            if wizard_step == step:
                sb.append('<li data-step="{0}" class="active">\n'.format(step))
            elif wizard_step > step:
                sb.append('<li data-step="{0}" class="complete">\n'.format(step))
            else:
                sb.append('<li data-step="{0}">\n'.format(step))
            sb.append('<span class="step">{0}</span>\n'.format(step))
            sb.append('<span class="title">{0}</span>\n'.format(wizard_items[i]))
            sb.append('</li>\n')

        sb.append('                </ul>\n')
        sb.append('            </div>\n')
        sb.append('        </div>\n')
        sb.append('    </div>\n')
        sb.append('</div>    \n')

        return str(sb)

    # @staticmethod
    # def convert_prospect_type_to_account(prospect_type):
    #     """
    #     @type prospect_type: int
    #     @param prospect_type:
    #     @return:
    #     """
    #     from default.config.config_common import prospect_type_account_id_map
    #     if prospect_type in prospect_type_account_id_map:
    #         return prospect_type_account_id_map[prospect_type]
    #     else:
    #         return prospect_type
    #
    # @staticmethod
    # def convert_account_to_prospect_type(account_id):
    #     """
    #     @type account_id: int
    #     @param account_id:
    #     @return:
    #     """
    #     from default.config.config_common import account_id_prospect_type_map
    #
    #     if account_id in account_id_prospect_type_map:
    #         return account_id_prospect_type_map[account_id]
    #     else:
    #         return account_id
    #
    # @staticmethod
    # def get_parent_account_id(child_id):
    #     """
    #     @type child_id: int
    #     @param child_id:
    #     @return:
    #     """
    #     from default.config.config_common import InternalAccountParentMap
    #     for account_parent in InternalAccountParentMap:
    #         if child_id in account_parent.value[1]:
    #             return account_parent.value[0]
    #     return child_id
    #

class DbAgent:
    """
    Database manipulating class
    """
    database = DatabaseRouter.data_database

    @staticmethod
    def get_data_map(query, params=None, first_blank=False, database=None):
        """
        Get dict of data. Key is first field's value, value is second field's value of the query
        @param query:
        @param params:
        @param first_blank:
        @param database:
        @return:
        """
        if database is None:
            database = DatabaseRouter.data_database
        from django.db import connections
        connection = connections[database]
        ret = {}
        if first_blank:
            ret[''] = ''

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rs = cursor.fetchall()
            for rec in rs:
                ret[rec[0]] = rec[1]
        return ret

    @staticmethod
    def get_data_list(query, params=None, database=None):
        """
        Get list of data. Values is first field's value of query
        @param query:
        @param params:
        @param database:
        @return:
        """
        if database is None:
            database = DatabaseRouter.data_database
        from django.db import connections
        connection = connections[database]
        ret = []

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rs = cursor.fetchall()
            for rec in rs:
                ret.append(rec[0])
        return ret

    @staticmethod
    def get_record_set(query, params=None, database=None):
        """
        Get record set of data (list of dict)
        @param query:
        @param params:
        @param database:
        @return:
        """
        if database is None:
            database = DatabaseRouter.data_database
        from django.db import connections
        connection = connections[database]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

    @staticmethod
    def get_record(query, params=None, database=None):
        """
        Get first record. Its a dict
        @param query:
        @param params:
        @param database:
        @return:
        """
        if database is None:
            database = DatabaseRouter.data_database
        from django.db import connections
        connection = connections[database]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    @staticmethod
    def get_value(query, params=None, database=None):
        """
        Get value of first field's value of query of first record
        @param query:
        @param params:
        @param database:
        @return:
        """
        rec = DbAgent.get_record(query, params, database)
        if rec:
            return rec[0]
        return None

    @staticmethod
    def execute_query(query, params=None, database=None):
        """
        Execute query
        @param query:
        @param params:
        @param database:
        @return:
        """
        if database is None:
            database = DatabaseRouter.data_database
        from django.db import connections
        connection = connections[database]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid


class Util:
    @staticmethod
    def to_int(value, default=0):
        """
        Convert string to int
        @param value:
        @param default:
        @return:
        """
        if isinstance(value, int):
            return value
        if value is None:
            return default
        if value.isdigit():
            return int(value)
        return default

    @staticmethod
    def enum_to_dict(enum_class, first_blank=False):
        """
        Convert enum to a dict.
        For python <3.0, you need to specify an __order__ attribute:
         __order__ = 'vanilla chocolate cookies mint'
        @type enum_class: Enum
        @param enum_class:
        @param first_blank
        @return:
        """
        ret = OrderedDict()
        if first_blank:
            ret[''] = ''

        for item in enum_class:
            if isinstance(item.value, tuple) or isinstance(item.value, list):
                ret[item.value[0]] = item.value[1]
            else:
                ret[item.value] = str(item.value)
        return ret

    @staticmethod
    def model_list_to_list(list_object, value_field):
        """
        Convert Django QuerySet to list of dict
        @param list_object:
        @param value_field:
        @return:
        """
        ret = list()
        for o in list_object:
            if isinstance(o, dict):
                ret.append(o[value_field])
            else:
                ret.append(o.__dict__[value_field])
        return ret

    @staticmethod
    def model_list_to_dict(model_list, key_field, value_field, first_blank=False):
        """
        Convert Django QuerySet to dict
        @param model_list:
        @param key_field:
        @param value_field:
        @param first_blank:
        @return:
        """
        ret = OrderedDict()
        if first_blank:
            ret[''] = ''

        for item in model_list:
            ret[item.__dict__[key_field]] = item.__dict__[value_field]

        return ret

    @staticmethod
    def is_date(string):
        """
        Check if string is date
        @param string:
        @return:
        """
        from dateutil.parser import parse
        try:
            parse(string)
            return True
        except ValueError:
            return False

    @staticmethod
    def to_date(string):
        """
        Convert to date
        @param string:
        @return:
        """
        from dateutil.parser import parse
        try:
            return parse(string)
        except ValueError:
            return None

    @staticmethod
    def get_data_map(objects, id_field, value_field):
        """
        Like as model_list_to_dict method
        """
        ret = dict()
        for o in objects:
            ret[o.__dict__[id_field]] = o.__dict__[value_field]
        return ret

    @staticmethod
    def create_wizard_menu(wizard_step, wizard_items):
        """
        Create html of wizard menu
        @param wizard_step: Wizard step
        @type wizard_step: int
        @type wizard_items: list
        @param wizard_items: Wizard items
        @rtype: str
        @return:
        """
        sb = StringBuilder()
        sb.append('<div class="widget-body">\n')
        sb.append('    <div class="widget-main">\n')
        sb.append('        <div id="fuelux-wizard-container">\n')
        sb.append('            <div>\n')
        sb.append('                <ul class="steps">\n')

        for i in range(len(wizard_items)):
            step = i + 1
            if wizard_step == step:
                sb.append('<li data-step="{0}" class="active">\n'.format(step))
            elif wizard_step > step:
                sb.append('<li data-step="{0}" class="complete">\n'.format(step))
            else:
                sb.append('<li data-step="{0}">\n'.format(step))
            sb.append('<span class="step">{0}</span>\n'.format(step))
            sb.append('<span class="title">{0}</span>\n'.format(wizard_items[i]))
            sb.append('</li>\n')

        sb.append('                </ul>\n')
        sb.append('            </div>\n')
        sb.append('        </div>\n')
        sb.append('    </div>\n')
        sb.append('</div>    \n')

        return str(sb)

    @staticmethod
    def convert_prospect_type_to_account(prospect_type):
        """
        @type prospect_type: int
        @param prospect_type:
        @return:
        """
        from default.config.config_common import prospect_type_account_id_map
        if prospect_type in prospect_type_account_id_map:
            return prospect_type_account_id_map[prospect_type]
        else:
            return prospect_type

    @staticmethod
    def convert_account_to_prospect_type(account_id):
        """
        @type account_id: int
        @param account_id:
        @return:
        """
        from default.config.config_common import account_id_prospect_type_map

        if account_id in account_id_prospect_type_map:
            return account_id_prospect_type_map[account_id]
        else:
            return account_id

    @staticmethod
    def get_parent_account_id(child_id):
        """
        @type child_id: int
        @param child_id:
        @return:
        """
        from default.config.config_common import InternalAccountParentMap
        for account_parent in InternalAccountParentMap:
            if child_id in account_parent.value[1]:
                return account_parent.value[0]
        return child_id


class NotExceptedTimeException(Exception):
    pass



class Format:
    """
    Date format class.
    Support 和暦.

    """
    ERA_JP = (
        ("M", "明治"),
        ("T", "大正"),
        ("S", "昭和"),
        ("H", "平成"),
    )

    @staticmethod
    def _convert_from_era(x):
        y = int(x.group(2))
        n = x.group(1)

        if (n == "平成" or n == "H") and y > 0:
            s = y + 1988
        elif (n == "昭和" or n == "S") and (y > 0) and (y <= 64):
            s = y + 1925
        elif (n == "大正" or n == "T") and (y > 0) and (y <= 15):
            s = y + 1911
        elif (n == "明治" or n == "M") and (y > 0) and (y <= 45):
            s = y + 1867
        else:
            s = 0

        return str(s)

    @staticmethod
    def _prepare_parse_object(o):
        o = o.replace(LocalizeFormat.MeridianPM.value, "PM")
        o = o.replace(LocalizeFormat.MeridianAM.value, "AM")
        # ERA
        o = re.sub(r"(H|S|T|M|平成|昭和|明治|大正)\.?([0-9]+)", lambda x: Format._convert_from_era(x), o)
        return o

    @staticmethod
    def _prepare_parse_format(o):
        o = o.replace("%o%E", "%Y")
        o = o.replace("%O%E", "%Y")
        o = o.replace("%o.%E", "%Y")
        o = o.replace("%O.%E", "%Y")
        return o

    @staticmethod
    def _format_datetime(o, format_string, default=""):
        if o is None:
            return default
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date) or isinstance(o, datetime.time):
            if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
                if isinstance(o, datetime.datetime):
                    y1868 = datetime.datetime(1868, 9, 8)
                    y1912 = datetime.datetime(1912, 7, 30)
                    y1926 = datetime.datetime(1926, 12, 25)
                    y1989 = datetime.datetime(1989, 1, 8)
                else:
                    y1868 = datetime.date(1868, 9, 8)
                    y1912 = datetime.date(1912, 7, 30)
                    y1926 = datetime.date(1926, 12, 25)
                    y1989 = datetime.date(1989, 1, 8)

                era_year, era, era_ch = None, None, None
                if o < y1868:
                    pass
                    # raise NotExceptedTimeException("time is expected later than 1868.09.08.")
                elif o < y1912:
                    era_year = o.year - 1867
                    era, era_ch = Format.ERA_JP[0]
                elif o < y1926:
                    era_year = o.year - 1911
                    era, era_ch = Format.ERA_JP[1]
                elif o < y1989:
                    era_year = o.year - 1925
                    era, era_ch = Format.ERA_JP[2]
                else:
                    era_year = o.year - 1988
                    era, era_ch = Format.ERA_JP[3]
                if era_year == 1 and format.find("EE") > -1:
                    era_year = "元"
                else:
                    era_year = text_type(era_year)
                format_string = format_string.replace("%o", era).replace("%O", era_ch).replace("%E", era_year)

            if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
                pm = False
                if o.hour > 12:
                    pm = True
                format_string = format_string.replace("%p",
                                                      LocalizeFormat.MeridianPM.value
                                                      if pm else LocalizeFormat.MeridianAM.value)

            if PY2:
                return o.strftime(format_string.encode("utf-8")).decode("utf-8")
            else:
                return o.strftime(format_string)
        else:
            return str(o)

    @staticmethod
    def format_date(o, format_string=None):
        if format_string is None:
            format_string = LocalizeFormat.PythonDateFormat.value
        return Format._format_datetime(o, format_string)

    @staticmethod
    def format_datetime(o, format_string=None):
        if format_string is None:
            format_string = LocalizeFormat.PythonDateTimeFormat.value
        return Format._format_datetime(o, format_string)

    @staticmethod
    def format_time(o):
        return Format._format_datetime(o, LocalizeFormat.PythonTimeFormat.value)

    @staticmethod
    def format_number(o, decimal_point=0):
        if isinstance(o, numbers.Number):
            return "{:,}".format(o)
        return o

    @staticmethod
    def to_date(o, date_format=None):
        if date_format is None:
            date_format = LocalizeFormat.PythonDateFormat.value
        if o is None or o == "":
            return None
        if not isinstance(o, str):
            return None

        o = Format._prepare_parse_object(o)
        format_string = Format._prepare_parse_format(date_format)
        try:
            return datetime.datetime.strptime(o, format_string).date()
        except ValueError:
            return None

    @staticmethod
    def to_time(o):
        if o is None or o == "":
            return None
        o = Format._prepare_parse_object(o)
        format_string = Format._prepare_parse_format(LocalizeFormat.PythonTimeFormat.value)

        return datetime.datetime.strptime(o, format_string).time()

    @staticmethod
    def to_number(o):
        return o

    @staticmethod
    def to_datetime(o):
        if o is None or o == "":
            return None
        o = Format._prepare_parse_object(o)
        format_string = Format._prepare_parse_format(LocalizeFormat.PythonDateTimeFormat.value)

        return datetime.datetime.strptime(o, format_string)
