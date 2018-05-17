# -*- coding: utf-8 -*-
from django.shortcuts import render
from default.config.config_menu import ScreenName
from default.logic.user_logic import (UserLogic,
                                      User, LoginUser,
                                      UserRoles)
from default.views.authen import check_login
from helper.lagform import (LagForm,
                            GacoiFormFieldType,
                            GacoiForm)
from django.core.exceptions import ObjectDoesNotExist


@check_login
def managestatistical(request):
    # check view privilege
    logging_user = LoginUser.get_login_user(request)

    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    teacher_id = params.get('teacher_id', '')
    if teacher_id and teacher_id.isdigit():
        teacher_id = int(teacher_id)
    else:
        teacher_id = -1

    type_form = GacoiForm('manage_statistical', '/manage_statistical/', 'POST')

    keu_form = LagForm()
    keu_form.set_title("Statistical")
    type_form.set_view(
        "id,user_name,login_name,teacher_id,address,phone,"
        "current_lesson,email,gender,roles")
    type_form.set_key("id")

    type_form.set_type('password', GacoiFormFieldType.Password)
    type_form.set_required('user_name,login_name')
    type_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
    type_form.set_type('created_datetime', GacoiFormFieldType.DateTime)

    type_form.set_hidden('teacher_id', teacher_id)
    type_form.get_field('id').set_link('?teacher_id=[id]&tab_index=1')

    genders = UserLogic.get_genders_dict()
    teachers = UserLogic.get_teachers_dict()
    roles = UserLogic.get_roles_dict()
    type_form.get_field("gender").set_drop_down_list_values(genders)
    type_form.get_field("teacher_id").set_drop_down_list_values(teachers)
    type_form.get_field("roles").set_drop_down_list_values(roles)
    type_form.set_search(
        'user_name,login_name, address, gender,roles,teacher_id')
    type_form.set_order('id,user_name,login_name,address,teacher_id,roles')

    type_form.init(request)

    if params.get('typeForm_action') == 'reset_password':
        reset_id = params.get('reset_id')
        try:
            user_changed = User.objects.get(id=reset_id)
            user_changed.password = UserLogic.hash_password(
                params.get('new_password', None))
            user_changed.save()
            reset_password = False
        except ObjectDoesNotExist:
            # transaction.rollback()
            print("aaa")

            # transaction.commit()

    data = User.objects.filter(roles=UserRoles.Teacher.code)
    for dt in data:
        dt.current_lesson = UserLogic.get_current_user_lesson(dt.id)
    # Order
    if type_form.order_field:
        if type_form.order_type == 'desc':
            data = data.order_by("-" + type_form.order_field)
        else:
            data = data.order_by(type_form.order_field)

    # Search user_name,login_name
    search = type_form.get_field("user_name").get_search_value()
    if search is not None and search != '':
        data = data.filter(user_name__contains=search)
    search = type_form.get_field("login_name").get_search_value()
    if search is not None and search != '':
        data = data.filter(login_name__contains=search)
    search = type_form.get_field("roles").get_search_value()
    if search:
        l = list(
            User.objects.filter(roles__in=search).values_list('id', flat=True))
        data = data.filter(id__in=l)
    search = type_form.get_field("gender").get_search_value()
    if search:
        l = list(User.objects.filter(gender__in=search).values_list('id',
                                                                    flat=True))
        data = data.filter(id__in=l)

    type_form.set_form_data(data)
    type_form.set_caption([
        "id,user_name,login_name,address,phone,email,gender,roles, "
        "current_lesson, teacher_id",
        "ID,Username,Login name,Address, Phone, Email, Gender,Roles,"
        "Current Lesson ,Teacher"])

    period_form = None
    fiscal_term = None

    tab_index = params.get("tab_index", '')
    tab_active1 = 'active'
    tab_active2 = ''
    if tab_index == '1':
        tab_active2 = 'active'
        tab_active1 = ''

    if teacher_id > 0:
        try:
            fiscal_term = User.objects.get(id=teacher_id)
        except ObjectDoesNotExist:
            fiscal_term = None
        period_form = GacoiForm('manage_statisticalxxx',
                                '/manage_statistical/', 'POST')
        period_form.set_view(
            "id,user_name,login_name,teacher_id,address,phone,"
            "current_lesson,email,gender,roles")
        period_form.set_key("id")

        period_form.set_type('password', GacoiFormFieldType.Password)
        period_form.set_required('user_name,login_name')
        period_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
        period_form.set_type('created_datetime', GacoiFormFieldType.DateTime)

        genders = UserLogic.get_genders_dict()
        teachers = UserLogic.get_teachers_dict()
        roles = UserLogic.get_roles_dict()
        period_form.get_field("gender").set_drop_down_list_values(genders)
        period_form.get_field("teacher_id").set_drop_down_list_values(teachers)
        period_form.set_hidden('teacher_id', teacher_id)
        # period_form.get_field('id').set_link('?teacher_id=[id]&tab_index=2')
        period_form.set_search(
            'user_name,login_name, address, gender,roles,teacher_id')
        period_form.set_order(
            'id,user_name,login_name,address,teacher_id,roles')
        period_form.get_field("roles").set_drop_down_list_values(roles)
        data = User.objects.filter(teacher_id=teacher_id)
        period_form.set_paging_value(15)
        period_form.init(request)
        if period_form.order_field:
            if period_form.order_type == 'desc':
                data = data.order_by("-" + period_form.order_field)
            else:
                data = data.order_by(period_form.order_field)

                # Search user_name,login_name
        search = period_form.get_field("user_name").get_search_value()
        if search is not None and search != '':
            data = data.filter(user_name__contains=search)
        search = period_form.get_field("login_name").get_search_value()
        if search is not None and search != '':
            data = data.filter(login_name__contains=search)
        search = period_form.get_field("roles").get_search_value()
        if search:
            l = list(User.objects.filter(roles__in=search).values_list('id',
                                                                       flat=True))
            data = data.filter(id__in=l)
        search = period_form.get_field("gender").get_search_value()
        if search:
            l = list(User.objects.filter(gender__in=search).values_list('id',
                                                                        flat=True))
            data = data.filter(id__in=l)

        period_form.set_form_data(data)
        period_form.set_caption([
            "id,user_name,login_name,address,phone,email,"
            "gender,roles, current_lesson, teacher_id",
            "ID,Username,Login name,Address, Phone, Email, "
            "Gender,Roles,Current Lesson ,Teacher"])

        period_form.set_form_data(data)
        tab_active2 = 'active'
        tab_active1 = ''

    context = {
        'user': logging_user,
        'screen_name': ScreenName.ManagerStastical,
        'fiscal_term': fiscal_term,
        'term_form': type_form,
        'period_form': period_form,
        'tab1': tab_active1,
        'tab2': tab_active2,
    }

    return render(request, 'managestatistical.html', context)
