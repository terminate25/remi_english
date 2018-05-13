# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from default.logic.userlogic import LoginUser


def login(request):
    """
    Login
    @param request: 
    @return: 
    """
    next = request.POST.get('next', '')
    if next == '':
        next = request.GET.get('next', '')

    user = request.POST.get('user', '')
    password = request.POST.get('password', '')
    notify = ''
    remember_me = (request.POST.get('remember_me', '') == 'true')

    error_message = ''

    if user != '' and password != '':
        if LoginUser.do_login(request, user, password, remember_me):
            if next != '' and next is not None:
                return redirect(next)
            return redirect("/course_list")
        else:
            error_message = 'The username or password was incorrect.'

    context = {
        'next': next,
        'errorMessage': error_message,
        'current_state': 1,
        'notify': notify
    }

    return render(request, 'login.html', context)


def logout(request):
    """
    Logout and go to Login page
    @param request: 
    @return: 
    """
    LoginUser.do_logout(request)
    return redirect("/login")
