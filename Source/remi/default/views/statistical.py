# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

from default.logic.log_logic import *
from default.logic.user_logic import *
from .authen import check_login
from django.db.models import ObjectDoesNotExist
from helper.lagform import *


@check_login
def statistical(request):
    """
    The function to render user view
    - Show user list
    - Create/Update/Delete the user information
    @param request:
    """
    logging_user = LoginUser.get_login_user()

    auth_type = None
    type_form = GacoiForm("typeForm", "/statistical/", "POST")

    keu_form = LagForm()
    keu_form.set_title("Statistical")
    type_form.set_view("id,user_name,login_name,teacher_id,"
                       "address,phone,current_lesson,email,gender,roles")
    type_form.set_key("id")

    type_form.set_type('password', GacoiFormFieldType.Password)
    type_form.set_required('user_name,login_name')
    type_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
    type_form.set_type('created_datetime', GacoiFormFieldType.DateTime)

    genders = UserLogic.get_genders_dict()
    teachers = UserLogic.get_teachers_dict()
    roles = UserLogic.get_roles_dict()
    type_form.get_field("gender").set_drop_down_list_values(genders)
    type_form.get_field("teacher_id").set_drop_down_list_values(teachers)
    type_form.get_field("roles").set_drop_down_list_values(roles)
    type_form.set_search('user_name,login_name, '
                         'address, gender,roles,teacher_id')
    type_form.set_order('id,user_name,login_name,address,teacher_id,roles')

    type_form.init(request)
    type_form.set_paging_value(15)
    reset_id = None
    reset_password = False

    # Check request
    # if typeForm_action = reset_password ->  handle request password
    params = request.POST

    if params.get('typeForm_action') == 'reset_password':
        reset_id = params.get('reset_id')
        # transaction.set_autocommit(False)
        try:
            user_changed = User.objects.get(id=reset_id)
            user_changed.password = UserLogic.hash_password(
                params.get('new_password', None)
            )
            user_changed.save()
            reset_password = False
        except ObjectDoesNotExist:
            # transaction.rollback()
            print("aaa")

        # transaction.commit()
    if logging_user.roles[0] == UserRoles.Admin.code:
        data = User.objects.all()
    else:
        data = User.objects.filter(Q(teacher_id=logging_user.id)
                                   & Q(roles=UserRoles.Student.code))
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
        l = list(User.objects.filter(roles__in=search)
                 .values_list('id', flat=True))
        data = data.filter(id__in=l)
    search = type_form.get_field("gender")\
        .get_search_value()
    if search:
        l = list(User.objects.filter(gender__in=search)
                 .values_list('id', flat=True))
        data = data.filter(id__in=l)

    type_form.set_form_data(data)
    type_form.set_caption(["id,user_name,login_name,address,phone,"
                           "email,gender,roles, current_lesson, teacher_id",
                           "ID,Username,Login name,Address, Phone,"
                           " Email, Gender,Roles,Current Lesson ,Teacher"])
    info_form = None
    context = {
        'authType': auth_type,
        'user': logging_user,
        'infoForm': info_form,
        'typeForm': type_form,
        'keuForm': keu_form,
        'screen_name': ScreenName.Statistical,
        'reset_password': reset_password,
        'reset_id': reset_id,
    }

    return render(request, 'statistical.html', context)
