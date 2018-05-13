# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from default.logic.userlogic import LoginUser, UserRoles, UserLogic
from django.db.models import ObjectDoesNotExist
from default.models.models import User



def signup(request):
    """
    Login
    @param request: 
    @return: 
    """

    params = request.POST
    new_password = params.get('new-password', '')
    confirm_password = params.get('confirm-password', '')
    notify = ''
    error_message = ''
    current_state = None
    if new_password != confirm_password:
        error_message = "Password confirm wrong!"
        current_state = 2
    else:

        email = params.get('email', '')
        username = params.get('username', '')
        login_name = params.get('login_name','')
        gender = 1
        phone = ""

        try:
            User.objects.get(login_name=login_name)
            error_message = "The login user is exist!"
            current_state = 2
            # LogOperation.log(LogModule.User, LogType.Insert, LogResult.Fail)
        except ObjectDoesNotExist:
            # transaction.set_autocommit(False)
            try:
                role = UserRoles.Student.code
                teacher_id = None
                user_new = UserLogic.create_user(username,
                                                 login_name,
                                                 gender,
                                                 role,
                                                 phone,
                                                 email,
                                                 "",
                                                 teacher_id,
                                                 password=new_password)
                UserLogic.store_user_courses(user_new.id, [])
                current_state = 1

            except ObjectDoesNotExist as e:
                print(1)

                # transaction.rollback()
                # LogOperation.log(LogModule.User, LogType.Insert, LogResult.Fail, None, e)

            # transaction.commit()
            notify = "Đăng ký tài khoản thành công. Vui lòng đăng nhập để tiếp tục!"

    context = {
        'notify' : notify,
        'signupErrorMessage': error_message,
        'current_state': current_state
    }

    return render(request, 'login.html', context)

