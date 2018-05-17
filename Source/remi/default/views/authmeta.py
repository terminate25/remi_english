# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from default.logic.metalogic import *
from django.shortcuts import render

from default.config.config_menu import ScreenName
from default.logic.user_logic import LoginUser
from default.views.authen import check_login
from helper.util import *

checkbox_values = []
his_info_id = None


@check_login
def courses_list(request):
    """
    Global variable:
        1. checkbox_values: used to store source meta_type records
        2. his_info_id: load info_form after merging
    Create form:
        1. type_form [main_tab]: meta_type table
        2. info_form [detail_tab]: meta_info table
        3. merge_form: merging meta_type
    Form action:
        1. Insert/Update/Delete: using QuerySet
        2. Merge: using QuerySet
    Return:
        Context format (JSON)
    @param request:
    @return:
    """
    user = LoginUser.get_login_user(request)
    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    meta_type_id = params.get('meta_type_id', '')

    if meta_type_id and meta_type_id.isdigit():
        meta_type_id = int(meta_type_id)
    else:
        meta_type_id = -1

    type_form = GacoiForm("type_form", "/meta/", "POST")
    type_form.set_view("id, meta_type, disp, created_datetime")  # , grouping_target, restriction
    type_form.set_key("id")
    if user.is_update_right():
        type_form.set_update("meta_type, disp")
    if user.is_add_right():
        type_form.set_insert("meta_type, disp")
    if user.is_delete_right():
        type_form.set_option_deletable(True)
    type_form.set_hidden("meta_type_id", meta_type_id)
    type_form.set_required("meta_type, disp")
    type_form.get_field("id").set_link("?meta_type_id=[id]&tab_index=1")
    type_form.set_type("created_datetime", GacoiFormFieldType.Date)
    type_form.set_order('id, meta_type, disp, created_datetime, grouping_target, restriction')
    type_form.set_caption({'id': 'ID', 'meta_type': 'メタデータ種別', 'disp': 'メタデータ名',
                           'created_datetime': '登録日'})
    type_form.init(request)

    course_data = {
        'video_link': 'https://www.youtube.com/embed/m6TXPNybrmk',


    }

    context = {
        'course_data': course_data,
        'user': user,
        'screen_name': ScreenName.Course,
    }

    return render(request, 'courses_list.html', context)
