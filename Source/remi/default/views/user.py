# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

from default.logic.log_logic import *
from default.logic.user_logic import *
from .authen import check_login
from django.db.models import ObjectDoesNotExist
from helper.lagform import *


@check_login
def user(request):
    """ 
    The function to render user view  
    - Show user list  
    - Create/Update/Delete the user information  
    @param request:  
    """
    logging_user = LoginUser.get_login_user()
    if not logging_user.is_view_right():
        return
    auth_type = None
    type_form = GacoiForm("typeForm", "/user/", "POST")

    keu_form = LagForm()
    keu_form.set_title("User List")
    type_form.set_view("id,user_name,login_name,address,phone,email,"
                       "course,gender,roles,teacher_id")
    type_form.set_key("id")

    if logging_user.is_add_right():
        type_form.set_insert("user_name,login_name,address, phone,course,"
                             "email,gender,roles,teacher_id")
    if logging_user.is_update_right():
        type_form.set_update("user_name,login_name,address, phone,course,"
                             "email,gender,roles,teacher_id")
    if logging_user.is_delete_right():
        type_form.set_option_deletable(True)

    type_form.set_type('password', GacoiFormFieldType.Password)
    type_form.set_required('user_name,login_name')
    type_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
    type_form.set_type('created_datetime', GacoiFormFieldType.DateTime)

    dept_id = AuthMetaTypeDefine.Department.code
    genders = UserLogic.get_genders_dict()
    teachers = UserLogic.get_teachers_dict()
    roles = UserLogic.get_roles_dict()
    type_form.get_field("gender").set_drop_down_list_values(genders)
    type_form.get_field("teacher_id").set_drop_down_list_values(teachers)
    type_form.get_field("roles").set_drop_down_list_values(roles)
    type_form.get_field("course").set_multi_choices(
        "select id,name from course id",
        "select c.id from course c inner join base_user_course u "
        "on u.course_id = c.id where u.user_id = [id]", 1)

    type_form.set_search('user_name,login_name, address,gender,'
                         'roles,teacher_id')
    type_form.set_order('id,user_name,login_name,address,teacher_id,roles')
    type_form.init(request)

    if logging_user.is_update_right():
        type_form.add_inline_user_button(InlineUserButton(
            "Change password", "change_password",
            action="do_change_password([id])")
        )

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

    # Check type_form.get_inline_user_button_return_value() return change_password button to open modal
    if logging_user.is_update_right():
        if "change_password" == \
                type_form.get_inline_user_button_return_value():
            reset_id = type_form.get_key_value("id")
            reset_password = True

    # call to edit in form view, if not: edit in grid view
    # type_form.set_option_update_in_form_view(True)

    if type_form.is_action(GacoiFormAction.DeleteDone):
        if logging_user.is_delete_right():
            try:
                user_deleted = User.objects.get(
                    pk=type_form.get_key_value("id")
                )
                user_deleted.delete()
                LogOperation.log(LogModule.User, LogType.Delete,
                                 LogResult.Success,
                                 type_form.get_key_value("id"))
            except ObjectDoesNotExist:
                LogOperation.log(LogModule.User, LogType.Delete,
                                 LogResult.Fail,
                                 type_form.get_key_value("id"))
    insert = False
    update = False
    if type_form.is_action(GacoiFormAction.InsertStart):
        keu_form.set_title("Create New User")
        insert = True
    if type_form.is_action(GacoiFormAction.UpdateStart):
        update = True
    # Insert
    if type_form.is_action(GacoiFormAction.InsertDone):
        try:
            User.objects.get(login_name=type_form.get_field(
                'login_name').get_value_blank2none()
                             )
            error_message = "The login user is exist!"
            type_form.set_action(GacoiFormAction.InsertStart)
            type_form.set_error_message(error_message)
            LogOperation.log(LogModule.User, LogType.Insert, LogResult.Fail)
        except ObjectDoesNotExist:
            # transaction.set_autocommit(False)
            try:
                role = type_form.get_field('roles').get_value_blank2none()
                teacher_id = type_form.get_field(
                    'teacher_id'
                ).get_value_blank2none()
                user_courses = type_form.get_field(
                    'course').get_multi_choices_selected_values()
                if int(role) != UserRoles.Student.code:
                    teacher_id = None
                user_new = UserLogic.create_user(
                    type_form.get_field('user_name').get_value_blank2none(),
                    type_form.get_field('login_name').get_value_blank2none(),
                    type_form.get_field('gender').get_value_blank2none(),
                    role,
                    type_form.get_field('phone').get_value_blank2none(),
                    type_form.get_field('email').get_value_blank2none(),
                    type_form.get_field('address').get_value_blank2none(),
                    teacher_id,
                    password=type_form.get_field(
                        'password').get_value_blank2none())
                UserLogic.store_user_courses(user_new.id, user_courses)
                type_form.set_action(1000)

            except ObjectDoesNotExist as e:

                # transaction.rollback()
                LogOperation.log(LogModule.User, LogType.Insert, LogResult.Fail, None, e)

            # transaction.commit()
            insert = False
            return HttpResponseRedirect("/user")

    if type_form.is_action(GacoiFormAction.UpdateDone):
        today = datetime.datetime.today()
        # transaction.set_autocommit(False)
        try:
            user_updated = User.objects.get(id=type_form.get_key_value('id'))
            print(user_updated.login_name)
            new_user_name = type_form.get_field(
                'user_name').get_value_blank2none()
            new_login_name = type_form.get_field(
                'login_name').get_value_blank2none()
            user_updated.user_name = new_user_name
            user_updated.login_name = new_login_name
            user_updated.updated_datetime = today
            role = type_form.get_field('roles').get_value_blank2none()
            teacher_id = type_form.get_field('teacher_id')\
                .get_value_blank2none()
            user_courses = type_form.get_field('course')\
                .get_multi_choices_selected_values()
            if int(role) != UserRoles.Student.code:
                teacher_id = None
            user_updated.gender = type_form.get_field('gender')\
                .get_value_blank2none()
            user_updated.roles = role
            user_updated.phone = type_form.get_field('phone')\
                .get_value_blank2none()
            user_updated.email = type_form.get_field('email')\
                .get_value_blank2none()
            user_updated.address = type_form.get_field('address')\
                .get_value_blank2none()
            user_updated.teacher_id = teacher_id

            type_form.get_field('roles').get_value_blank2none()
            user_updated.save()
            UserLogic.update_user_courses(user_updated.id, user_courses)

            LogOperation.log(LogModule.User, LogType.Update,
                             LogResult.Success,
                             type_form.get_key_value('id'))
        except ObjectDoesNotExist:
            # transaction.rollback()
            LogOperation.log(LogModule.User, LogType.Update, LogResult.Fail)
        # transaction.commit()
        update = False
    type_form.set_paging_value(10)

    # data = User.objects.all().values_list('id',flat=False)
    data = User.objects.all()
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
        l = list(User.objects.filter(
            roles__in=search).values_list('id', flat=True))
        data = data.filter(id__in=l)
    search = type_form.get_field("gender").get_search_value()
    if search:
        l = list(User.objects.filter(gender__in=search).values_list('id', flat=True))
        data = data.filter(id__in=l)

    type_form.set_form_data(data)
    # type_form.set_form_model(User)
    type_form.set_caption(["id,user_name,login_name,address,"
                           "phone,email,gender,roles, teacher_id, course",
                           "ID,Username,Login name,Address, "
                           "Phone, Email, Gender,Roles, Teacher, Course"])
    info_form = None
    context = {  # "select id,name,email,password from user"
        'authType': auth_type,
        'user': logging_user,
        'infoForm': info_form,
        'typeForm': type_form,
        'keuForm': keu_form,
        'screen_name': ScreenName.User,
        'reset_password': reset_password,
        'update': update,
        'insert': insert,
        'reset_id': reset_id,
    }

    return render(request, 'user.html', context)
